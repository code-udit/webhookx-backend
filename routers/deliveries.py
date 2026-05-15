from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Delivery, User, Webhook
from routers.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_deliveries(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.email == current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deliveries = db.query(Delivery, Webhook).join(Webhook).filter(
        Webhook.user_id == user.id
    ).all()
    
    result = []
    
    for d, w in deliveries:
        result.append({
            "id": d.id,
            "status": d.status,
            "attempt_count": d.attempt_count,
            "webhook_url": w.target_url
        })

    return result