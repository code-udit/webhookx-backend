# WebhookX Backend

A scalable webhook delivery engine built with FastAPI, PostgreSQL, Redis, and Celery that supports asynchronous webhook delivery, retry mechanisms, dead letter queues, logging, and real-time monitoring.

---

## 🚀 Overview

WebhookX Backend is the core engine responsible for:

- Managing webhook registrations
- Receiving events
- Processing asynchronous deliveries
- Retrying failed deliveries
- Logging delivery attempts
- Handling dead letter queues
- Providing analytics APIs

The system is designed for reliability, scalability, and production-grade webhook processing.

---

## 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Celery
- Docker
- JWT Authentication
- Python 3.11

---

## 🧱 System Architecture

```text
Client → FastAPI → PostgreSQL
                ↓
             Redis Queue
                ↓
           Celery Workers
                ↓
        External Webhook URLs
````

---

## 📁 Project Structure

```bash
webhookx-backend/
│
├── routers/
│   ├── auth.py
│   ├── webhook.py
│   ├── event.py
│   └── deliveries.py
│
├── celery_app.py
├── config.py
├── database.py
├── models.py
├── tasks.py
├── main.py
├── requirements.txt
└── docker-compose.yml
```

---

## ✨ Features

### 🔐 Authentication

* User Registration
* User Login
* JWT Authentication
* Password Hashing
* Protected APIs

### 🔗 Webhook Management

* Create Webhooks
* Delete Webhooks
* List User Webhooks
* Secret Key Generation

### ⚡ Event Processing

* Event Ingestion API
* Event Storage
* Async Delivery Queue
* Multi-Webhook Dispatching

### 🚚 Delivery Engine

* HTTP POST Delivery
* Background Processing
* Response Tracking
* Latency Measurement

### 🔄 Retry Logic

Exponential Backoff Retry Strategy:

| Attempt | Delay             |
| ------- | ----------------- |
| 1       | 30 Seconds        |
| 2       | 2 Minutes         |
| 3       | 10 Minutes        |
| 4       | 30 Minutes        |
| 5       | Dead Letter Queue |

### ☠️ Dead Letter Queue

* Store Permanently Failed Deliveries
* Retry Failed Jobs Manually
* Failure Tracking

### 📊 Logging & Metrics

* Delivery Logs
* Success Rate
* Failed Deliveries
* Average Latency
* Delivery Analytics

---

## 🗄 Database Schema

### users

| Column        | Type     |
| ------------- | -------- |
| id            | Integer  |
| email         | String   |
| password_hash | String   |
| created_at    | DateTime |

### webhooks

| Column     | Type     |
| ---------- | -------- |
| id         | Integer  |
| user_id    | Integer  |
| target_url | String   |
| event_type | String   |
| secret_key | String   |
| is_active  | Boolean  |
| created_at | DateTime |

### events

| Column     | Type     |
| ---------- | -------- |
| id         | Integer  |
| event_type | String   |
| payload    | JSON     |
| created_at | DateTime |

### deliveries

| Column        | Type     |
| ------------- | -------- |
| id            | Integer  |
| webhook_id    | Integer  |
| event_id      | Integer  |
| status        | String   |
| attempt_count | Integer  |
| next_retry_at | DateTime |
| delivered_at  | DateTime |
| created_at    | DateTime |

### delivery_logs

| Column         | Type     |
| -------------- | -------- |
| id             | Integer  |
| delivery_id    | Integer  |
| attempt_number | Integer  |
| response_code  | Integer  |
| response_body  | Text     |
| latency_ms     | Integer  |
| attempted_at   | DateTime |

---

## ⚙️ Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/webhookx
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379/0
```

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/webhookx-backend.git
cd webhookx-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

### Start FastAPI Server

```bash
uvicorn main:app --reload
```

Application runs on:

```bash
http://localhost:8000
```

---

## ⚡ Run Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

---

## 🐳 Docker Setup

### Run Full System

```bash
docker-compose up --build
```

Services:

* FastAPI
* PostgreSQL
* Redis
* Celery Worker

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint  |
| ------ | --------- |
| POST   | /register |
| POST   | /login    |

### Webhooks

| Method | Endpoint       |
| ------ | -------------- |
| POST   | /webhooks      |
| GET    | /webhooks      |
| DELETE | /webhooks/{id} |

### Events

| Method | Endpoint |
| ------ | -------- |
| POST   | /events  |

### Deliveries

| Method | Endpoint               |
| ------ | ---------------------- |
| GET    | /deliveries            |
| GET    | /deliveries/logs       |
| GET    | /deliveries/dlq        |
| POST   | /deliveries/retry/{id} |

---

## 🔄 Delivery Workflow

1. User registers webhook
2. Event is received
3. Delivery job created
4. Celery worker processes job
5. Webhook POST request sent
6. Response logged
7. Retry scheduled if failed
8. Final failure moved to DLQ

---

## 📈 Future Improvements

* Rate Limiting
* WebSocket Monitoring
* API Key Authentication
* Event Replay
* Batch Deliveries
* Kubernetes Deployment
* Prometheus Metrics
* Grafana Dashboard





