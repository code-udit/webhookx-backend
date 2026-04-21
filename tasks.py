from celery_app import celery
import requests
import time
from database import SessionLocal
from models import Delivery
from datetime import datetime


@celery.task
def send_webhook(url, payload, delivery_id):
    db = SessionLocal()

    start = time.time()

    try:
        response = requests.post(url, json=payload, timeout=5)

        latency = int((time.time() - start) * 1000)

        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

        if delivery:
            delivery.status = "success"
            delivery.delivered_at = datetime.utcnow()
            db.commit()

        print(f"✅ Sent: {url}")
        print(f"Status: {response.status_code}")
        print(f"Latency: {latency} ms")

    except Exception as e:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

        if delivery:
            delivery.status = "failed"
            db.commit()

        print(f"❌ Failed: {url}")
        print(f"Error: {str(e)}")

    finally:
        db.close()