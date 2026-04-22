from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL
import time

for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()   # ✅ FORCE connection
        connection.close()
        print("✅ Database connected")
        break
    except Exception as e:
        print("⏳ Waiting for DB...", e)
        time.sleep(2)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()