WebhookX Backend — Scalable Webhook Delivery Engine

📌 Overview

WebhookX is a production-style webhook delivery system built with FastAPI, Celery, Redis, and PostgreSQL.

It allows users to:

- Register webhook endpoints
- Send events
- Deliver payloads asynchronously
- Retry failed deliveries
- Track logs and performance metrics

---

🏗️ Architecture

Client → FastAPI → PostgreSQL → Redis Queue → Celery Worker → External Webhook

---

⚙️ Tech Stack

- Backend Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Queue System: Redis
- Worker: Celery
- Auth: JWT + Password Hashing
- Containerization: Docker + Docker Compose

---

✨ Features

🔐 Authentication

- User registration & login
- JWT-based authentication
- Protected routes

🔗 Webhook Management

- Create webhook endpoints
- List user-specific webhooks
- Delete webhooks
- Secret key generation

⚡ Event Processing

- Accept events via API
- Store events in DB
- Match relevant webhooks
- Create delivery jobs

🚚 Async Delivery Engine

- Background processing using Celery
- HTTP POST delivery to webhook URLs
- Latency measurement
- Response tracking

🔄 Retry Mechanism

- Exponential backoff strategy
- Automatic retry on failure
- Max retry limit handling

☠️ Dead Letter Queue (DLQ)

- Failed deliveries marked as “dead”
- Stored for later inspection
- Manual retry support

📊 Logging & Metrics

- Delivery logs stored per attempt
- Tracks:
  - Response status
  - Latency
  - Attempt count
- Ready for analytics dashboards

---

🧩 Database Schema

Main tables:

- "users"
- "webhooks"
- "events"
- "deliveries"
- "delivery_logs"

---

🐳 Docker Setup

Run entire system

docker compose up --build

Services

- API → http://localhost:8000
- Swagger Docs → http://localhost:8000/docs
- PostgreSQL → port 5432
- Redis → port 6379
- Celery Worker → background

---

🧪 Testing the System (Stage-wise Validation)

The backend system was tested incrementally across all development stages to ensure correctness, stability, and production readiness.

---

🧩 Stage B1 — API Startup

✔ Verified FastAPI server runs
✔ Accessible at:

http://localhost:8000/docs

---

🐘 Stage B2 — Database Connection

✔ PostgreSQL container started via Docker
✔ SQLAlchemy successfully connected
✔ Retry mechanism handled delayed DB startup

Expected log:

Database connected

---

🧱 Stage B3 — Models & Tables

✔ Tables created:

- users
- webhooks
- events
- deliveries
- delivery_logs

✔ Verified via DB inspection

---

🔐 Stage B4 — Authentication

✔ Register API tested
✔ Login API returns JWT
✔ Protected routes validated using token

---

🔗 Stage B5 — Webhook Management

✔ Create webhook → success
✔ List user webhooks → correct filtering
✔ Delete webhook → removed from DB

---

⚡ Stage B6 — Event Ingestion

✔ Event API triggered
✔ Event stored in DB
✔ Delivery records created

---

🔁 Stage B7 — Queue + Worker

✔ Redis running
✔ Celery worker connected

Verified using logs:

Connected to redis://redis:6379/0
celery ready

---

🚚 Stage B8 — Delivery Engine

✔ Worker sends POST request to webhook URL
✔ Captured:

- Status code
- Response
- Execution time

Example log:

Sent: https://webhook.site/...
Status: 200

---

🔄 Stage B9 — Retry System

✔ Failed webhook tested using invalid URL
✔ Retry attempts triggered with delay
✔ Status updated correctly

---

☠️ Stage B10 — Dead Letter Queue

✔ Failed deliveries moved to DLQ
✔ Fetch via:

GET /webhook/dlq

✔ Manual retry tested:

POST /webhook/retry/{id}

---

📊 Stage B11 — Logging & Metrics

✔ delivery_logs table populated
✔ Each attempt stored with:

- status
- response
- timestamp

---

🐳 Stage B12 — Dockerization

✔ Entire system runs using:

docker compose up --build

✔ Verified:

- API container
- DB container
- Redis container
- Worker container

✔ Inter-service communication working

---

📦 Stage B13 — Final Integration Test

End-to-end flow tested:

1. Create webhook
2. Trigger event
3. Worker processes task
4. External service receives request

Worker logs confirm:

Task tasks.send_webhook received
Status: 200
Task succeeded

---

✅ Final Outcome

✔ Full system tested stage-by-stage
✔ Async processing verified
✔ Retry + DLQ validated
✔ Docker-based deployment working
✔ Production-ready webhook engine

---

🔁 Retry Flow

If webhook fails:

- Retries automatically with delay
- Updates delivery status
- Moves to DLQ after max retries

---

📦 API Endpoints (Key)

Auth

- POST /auth/register
- POST /auth/login

Webhooks

- POST /webhook/create
- GET /webhook/list
- DELETE /webhook/delete/{id}

Events

- POST /event/create

DLQ

- GET /webhook/dlq
- POST /webhook/retry/{delivery_id}

---

📈 System Flow

1. User creates webhook
2. Event is triggered
3. Matching webhooks are fetched
4. Delivery jobs created
5. Celery worker processes jobs
6. Webhook called
7. Logs stored
8. Retry if failed

---

🧠 Key Learnings

- Async task processing with Celery
- Distributed system design basics
- Retry & fault tolerance patterns
- Docker-based service orchestration
- Real-world backend architecture

