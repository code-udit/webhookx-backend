from fastapi import FastAPI
from routers.auth import router as auth_router
from database import Base, engine
from models import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "WebhookX running"}