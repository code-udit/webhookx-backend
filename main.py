from fastapi import FastAPI
from routers.auth import router as auth_router
from database import Base, engine
from models import User
from routers import webhook
from routers import event
from fastapi.middleware.cors import CORSMiddleware
from routers import deliveries


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")

app.include_router(webhook.router, prefix="/webhook")

app.include_router(event.router, prefix="/event")

app.include_router(deliveries.router, prefix="/deliveries")


@app.get("/")
def root():
    return {"message": "WebhookX running"}

