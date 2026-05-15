from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event, Webhook, Delivery
from tasks import send_webhook
from pydantic import BaseModel

router = APIRouter()


class EventRequest(BaseModel):
    event_type: str
    payload: dict


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_event(data: EventRequest, db: Session = Depends(get_db)):

    # 1. Save event
    event = Event(
        event_type=data.event_type,
        payload=data.payload
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # 2. Find matching webhooks
    webhooks = db.query(Webhook).filter(
        Webhook.event_type == data.event_type
    ).all()

    # 3. Create delivery jobs + trigger async webhook
    for webhook in webhooks:
        delivery = Delivery(
            webhook_id=webhook.id,
            event_id=event.id,
            status="pending"
        )
        db.add(delivery)

        db.flush()
        send_webhook.delay(webhook.target_url, data.payload, delivery.id)

    db.commit()

    return {
        "message": "Event processed",
        "matched_webhooks": len(webhooks)
    }