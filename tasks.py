from celery_app import celery
import requests
import time
from database import SessionLocal
from models import Delivery, DeliveryLog
from datetime import datetime


@celery.task(bind=True, max_retries=5)
def send_webhook(self, url, payload, delivery_id):
    db = SessionLocal()

    try:
        start = time.time()

        response = requests.post(url, json=payload, timeout=5)

        latency = int((time.time() - start) * 1000)

        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

        if delivery:
            delivery.attempt_count += 1
            delivery.status = "success"
            delivery.delivered_at = datetime.utcnow()
            db.commit()

            # 📊 Log success
            log = DeliveryLog(
                delivery_id=delivery_id,
                attempt_number=delivery.attempt_count,
                response_code=response.status_code,
                response_body=response.text[:200],
                latency_ms=latency
            )
            db.add(log)
            db.commit()

        print("✅ Sent:", url)
        print("Status:", response.status_code)

    except Exception as e:
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

        if delivery:
            delivery.attempt_count += 1
            db.commit()

            # 📊 Log failure
            log = DeliveryLog(
                delivery_id=delivery_id,
                attempt_number=delivery.attempt_count,
                response_code=0,
                response_body=str(e),
                latency_ms=0
            )
            db.add(log)
            db.commit()

        if self.request.retries >= self.max_retries:
            if delivery:
                delivery.status = "dead"
                db.commit()

            print("☠️ Moved to DLQ:", url)
            db.close()
            return

        raise self.retry(exc=e, countdown=10)

    finally:
        db.close()