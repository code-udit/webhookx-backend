from celery_app import celery


@celery.task
def test_task():
    print("🔥 Task executed successfully")
    return "done"