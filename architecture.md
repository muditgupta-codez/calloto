# Calloto — System Architecture

## System Overview
Calloto is a FastAPI-based web application that integrates with Voxvaani API for telephony and WhatsApp automation, Paddle/Lemon Squeezy for payments, and Calendly for booking. The system captures missed calls via webhooks, sends automated text-backs, and provides a dashboard for businesses to track ROI.

## Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
  - Async support for webhook handling
  - Automatic OpenAPI docs
  - Pydantic for validation
- **ORM:** SQLAlchemy 2.0
  - SQLite for validation stage
  - Postgres-ready schema (use standard SQL types, avoid SQLite-specific features)
- **Database:** SQLite (file on `/data` volume in Docker)
  - Migration path to Postgres when needed
  - Use Alembic for migrations

### External Services
- **Telephony & WhatsApp:** Voxvaani API
  - Call handling and call webhooks (capture caller ID, drop call immediately)
  - WhatsApp automation (text-backs, 2-way messaging)
  - UK number management
- **Payments:** Paddle or Lemon Squeezy (merchant of record)
  - Handles UK VAT compliance
  - Manages payouts to India
  - Subscription billing + webhooks
  - Customer billing portal
- **Booking:** Calendly (v1), built-in scheduler (v1.1)
  - Calendly embed via iframe/JS
  - Built-in scheduler for v1.1 (custom implementation)

### Frontend
- **Tech:** Single-page HTML/JS served by FastAPI
  - No build step (vanilla JS or lightweight framework like Alpine.js)
  - Static files served from `/static` directory
- **Auth:** JWT tokens (email + password or magic link)

### Hosting & Infrastructure
- **Platform:** Coolify (Docker)
  - Single container for FastAPI app
  - SQLite DB file on `/data` volume (persists across redeployments)
  - Environment variables for secrets (Voxvaani, Paddle, etc.)
- **Domain:** calloto.com (primary), calloto.co.uk (redirect)
- **Monitoring:** `/health` endpoint + structured logs + uptime monitoring

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (HTML/JS)                    │
│  - Landing page + signup                                     │
│  - Customer dashboard (missed calls, messages, bookings)     │
│  - Admin panel                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Auth       │  │  Dashboard   │  │   Admin      │      │
│  │   Routes     │  │   Routes     │  │   Routes     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Webhook Handlers                         │  │
│  │  - /api/webhook/call (Voxvaani incoming call)          │  │
│  │  - /api/webhook/message (Voxvaani inbound message)     │  │
│  │  - /api/webhook/payment (Paddle/LS subscription)     │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer                            │  │
│  │  - telephony.py (Voxvaani API integration)               │  │
│  │  - messaging.py (SMS/WhatsApp text-back)             │  │
│  │  - billing.py (Paddle/Lemon Squeezy)                 │  │
│  │  - booking.py (Calendly/scheduler)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Data Layer                               │  │
│  │  - models.py (SQLAlchemy models)                     │  │
│  │  - schemas.py (Pydantic schemas)                     │  │
│  │  - SQLite DB on /data volume                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  - Voxvaani API (telephony, WhatsApp automation)            │
│  - Paddle/Lemon Squeezy (payments, subscriptions)           │
│  - Calendly (booking embed)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Missed Call Flow
```
Customer calls business number
  → Business phone forwards to Calloto number (network-level)
  → Voxvaani receives call, fires webhook to /api/webhook/call
  → FastAPI captures caller ID
  → FastAPI drops call immediately via Voxvaani API
  → Create missed_call record in DB (caller_number, called_at, customer_id)
  → Trigger text-back service
  → Send WhatsApp/SMS via Voxvaani API with business's message template
  → Create message record in DB (channel, direction=out, body, status)
  → Update usage count for the month
```

### 2. Signup & Payment Flow
```
User submits signup form (email, name, phone, vertical)
  → POST /api/signup creates customer record (subscription_status=inactive)
  → POST /api/checkout creates Paddle/LS checkout session
  → User completes payment on Paddle/LS hosted page
  → Paddle/LS fires webhook to /api/webhook/payment (subscription.created)
  → FastAPI updates customer.subscription_status=active
  → FastAPI provisions Voxvaani number (or assigns from pool)
  → FastAPI sends onboarding email with forwarding instructions
```

### 3. Booking Flow
```
Caller receives text-back with booking link
  → Caller taps link (Calendly embed URL or built-in scheduler)
  → Caller selects time slot and confirms
  → For Calendly: Calendly fires webhook (or poll API)
  → For built-in: POST /api/bookings creates booking record
  → Create booking record in DB (customer_id, missed_call_id, slot_time, source)
  → Notify business via WhatsApp/email
  → Update missed_call.status=booked
```

## Data Model

### customers
```sql
id INTEGER PRIMARY KEY
email TEXT UNIQUE NOT NULL
name TEXT NOT NULL
phone TEXT NOT NULL
trade_vertical TEXT NOT NULL
country TEXT DEFAULT 'GB'
  calloto_number TEXT  -- Voxvaani number assigned to this business
message_template TEXT  -- Text-back template with placeholders
price_range TEXT  -- e.g. "£50-150"
paddle_customer_id TEXT  -- or lemon_squeezy_customer_id
subscription_status TEXT DEFAULT 'inactive'  -- active/canceled/past_due
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### missed_calls
```sql
id INTEGER PRIMARY KEY
customer_id INTEGER REFERENCES customers(id)
caller_number TEXT NOT NULL
  call_sid TEXT  -- Voxvaani Call ID
called_at TIMESTAMP NOT NULL
duration INTEGER DEFAULT 0  -- seconds
status TEXT DEFAULT 'texted'  -- texted/replied/booked/ignored/withheld
```

### messages
```sql
id INTEGER PRIMARY KEY
customer_id INTEGER REFERENCES customers(id)
missed_call_id INTEGER REFERENCES missed_calls(id)
channel TEXT NOT NULL  -- sms/whatsapp
direction TEXT NOT NULL  -- out/in
body TEXT NOT NULL
  provider_msg_id TEXT  -- Voxvaani Message ID
sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
status TEXT DEFAULT 'sent'  -- sent/delivered/failed
```

### bookings
```sql
id INTEGER PRIMARY KEY
customer_id INTEGER REFERENCES customers(id)
missed_call_id INTEGER REFERENCES missed_calls(id)
cal_link TEXT  -- Calendly URL or built-in scheduler URL
slot_time TIMESTAMP NOT NULL
source TEXT NOT NULL  -- calendly/scheduler/reply
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### usage
```sql
id INTEGER PRIMARY KEY
customer_id INTEGER REFERENCES customers(id)
month TEXT NOT NULL  -- YYYY-MM format
messages_sent INTEGER DEFAULT 0
overage_units INTEGER DEFAULT 0
```

## API Structure

### Public Endpoints
```
POST /api/signup          — Create account + redirect to checkout
POST /api/checkout        — Generate Paddle/LS checkout URL
POST /api/webhook/payment — Paddle/LS webhook (subscription events)
POST /api/webhook/call    — Voxvaani incoming call webhook
POST /api/webhook/message — Voxvaani inbound message webhook
GET  /api/dashboard       — (auth required) Business feed + usage
GET  /api/health          — Health check (DB, Voxvaani, payment provider)
```

### Admin Endpoints (Bearer token auth)
```
GET    /api/admin/customers              — List all customers
POST   /api/admin/customers/{id}/numbers — Provision/assign Voxvaani number
POST   /api/admin/customers/{id}/test    — Send test text-back
GET    /api/admin/usage                  — Aggregate usage stats
```

## Deployment Architecture

### Docker Setup
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY ./static /app/static

# SQLite DB lives on /data volume
VOLUME ["/data"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Coolify Configuration
- **App type:** Dockerfile
- **Port:** 8000
- **Volume mount:** `/data` → host `/data/calloto` (persists SQLite DB)
- **Environment variables:**
  - `VOXVAANI_API_KEY`
  - `VOXVAANI_API_SECRET`
  - `VOXVAANI_PHONE_NUMBER` (pool or default)
  - `PADDLE_VENDOR_ID`
  - `PADDLE_API_KEY`
  - `DATABASE_URL` (SQLite file path on /data)
  - `SECRET_KEY` (JWT signing)
  - `ADMIN_TOKEN` (admin API auth)

### Critical Deployment Notes
- **DB persistence:** SQLite file MUST be on `/data` volume — it gets wiped on redeploy otherwise
- **Backups:** Daily SQLite backup to external storage (S3/Backblaze)
- **Logs:** Structured JSON logs to stdout (Coolify captures)
- **Health checks:** `/health` endpoint checks DB connectivity + Voxvaani reachability

## Security Considerations
- All webhooks validate signatures (Voxvaani, Paddle/LS)
- JWT tokens for customer auth (short expiry + refresh tokens)
- Bearer token for admin endpoints (long, random, stored in env)
- HTTPS only (enforced by Coolify/Cloudflare)
- Caller numbers are personal data (GDPR) — minimal storage, documented retention
- No secrets in code — all credentials in environment variables

## Scalability Notes
- SQLite is fine for validation stage (up to ~1000 customers)
- Migration to Postgres when needed (schema is Postgres-ready)
- Voxvaani handles telephony scaling
- Paddle/LS handles payment scaling
- Horizontal scaling: stateless FastAPI app (DB is the bottleneck)
- Consider connection pooling + read replicas for Postgres migration
