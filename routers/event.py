from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event, Webhook, Delivery
from tasks import send_webhook

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_event(event_type: str, payload: dict, db: Session = Depends(get_db)):

    # 1. Save event
    event = Event(
        event_type=event_type,
        payload=payload
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # 2. Find matching webhooks
    webhooks = db.query(Webhook).filter(
        Webhook.event_type == event_type
    ).all()

    # 3. Create delivery jobs + trigger async webhook
    for webhook in webhooks:
        delivery = Delivery(
            webhook_id=webhook.id,
            event_id=event.id,
            status="pending"
        )
        db.add(delivery)

        db.flush()  # get delivery.id before commit
        send_webhook.delay(webhook.target_url, payload, delivery.id)

    db.commit()

    return {
        "message": "Event processed",
        "matched_webhooks": len(webhooks)
    }