from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Delivery
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
    deliveries = db.query(Delivery).all()
    return deliveries