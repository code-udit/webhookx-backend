from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Webhook, User
from routers.auth import get_current_user
import secrets

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

    # ✅ Generate secure random secret
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

    webhooks = db.query(Webhook).filter(Webhook.user_id == user.id).all()

    return webhooks


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

    db.delete(webhook)
    db.commit()

    return {"message": "Webhook deleted"}