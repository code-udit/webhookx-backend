import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL is not set")

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.broker_connection_retry_on_startup = True

import tasks