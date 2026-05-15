from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Webhook, User, Delivery, Event
from routers.auth import get_current_user
from tasks import send_webhook
import secrets
from sqlalchemy import text

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_webhook(
    url: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    secret = secrets.token_hex(16)

    webhook = Webhook(
        user_id=user.id,
        target_url=url,
        event_type="default",
        secret_key=secret
    )

    db.add(webhook)
    db.commit()
    db.refresh(webhook)

    return {
        "message": "Webhook created",
        "secret_key": secret
    }


@router.get("/list")
def list_webhooks(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Webhook).filter(Webhook.user_id == user.id).all()



@router.delete("/delete/{webhook_id}")
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == user.id
    ).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    deliveries = db.query(Delivery).filter(
        Delivery.webhook_id == webhook.id
    ).all()

    for delivery in deliveries:
        db.execute(
            text("DELETE FROM delivery_logs WHERE delivery_id = :id"),
            {"id": delivery.id}
        )

    db.query(Delivery).filter(
        Delivery.webhook_id == webhook.id
    ).delete()

    db.delete(webhook)
    db.commit()

    return {"message": "Webhook deleted"}


# 🔥 DLQ — Get dead deliveries
@router.get("/dlq")
def get_dead_deliveries(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dead = db.query(Delivery).join(Webhook).filter(
        Delivery.status == "dead",
        Webhook.user_id == user.id
    ).all()

    return dead


# 🔁 Retry dead delivery
@router.post("/retry/{delivery_id}")
def retry_dead_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

    if not delivery or delivery.status != "dead":
        raise HTTPException(status_code=400, detail="Invalid delivery")

    webhook = db.query(Webhook).filter(Webhook.id == delivery.webhook_id).first()
    event = db.query(Event).filter(Event.id == delivery.event_id).first()

    if not webhook or not event:
        raise HTTPException(status_code=404, detail="Data not found")

    # reset
    delivery.status = "pending"
    delivery.attempt_count = 0
    db.commit()

    # async retry
    send_webhook.delay(webhook.target_url, event.payload, delivery.id)

    return {"message": "Retry triggered"}



@router.get("/test-task")
def test_task():
    send_webhook.delay(
        url="https://webhook.site/test",
        payload={"msg": "hello"},
        delivery_id=1
    )
    return {"message": "triggered"}