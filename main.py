from fastapi import FastAPI
from routers.auth import router as auth_router
from database import Base, engine
from models import User
from routers import webhook

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")

app.include_router(webhook.router, prefix="/webhook")

@app.get("/")
def root():
    return {"message": "WebhookX running"}

