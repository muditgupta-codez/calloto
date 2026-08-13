# AGENTS.md — Calloto

## Project Overview
Calloto is a missed-call text-back SaaS for UK tradespeople. When a business misses a call, Calloto instantly texts the caller back with a booking link. £19/month self-serve subscription.

## Tech Stack
- **Backend:** FastAPI (Python)
- **DB:** SQLite (validation stage), Postgres-ready schema
- **Telephony & WhatsApp:** Voxvaani API (call handling, call webhooks, WhatsApp automation)
- **Payments:** Paddle or Lemon Squeezy (merchant of record for UK VAT)
- **Booking:** Calendly embed (v1), built-in scheduler (v1.1)
- **Frontend:** Single-page HTML/JS served by FastAPI
- **Hosting:** Coolify (Docker) — DB must persist on `/data` volume

## Key Commands
```bash
# TODO: Add once project is scaffolded
# uvicorn app.main:app --reload
# pytest
# ruff check .
```

## Critical Context for AI Agents
- **Do NOT use plain Stripe for UK B2C** — use Paddle/Lemon Squeezy as merchant of record (handles UK VAT + India payouts)
- **DB persistence:** SQLite file MUST live on `/data` volume in Docker — it gets wiped on redeploy otherwise
- **Voxvaani call webhook:** Drop the call immediately after capturing caller ID (no need to answer)
- **Caller ID passthrough:** UK network-level call forwarding passes real caller number — this is the whole product
- **Withheld numbers:** Cannot be texted back; show as "not texted" in dashboard
- **Messaging quota:** 100 messages/month included in £19, £0.05/message overage
- **GDPR:** Caller numbers are personal data — minimal storage, documented retention policy
- **PECR:** Text-backs are transactional (triggered by caller's inbound call), not marketing

## Data Model (core tables)
- `customers` — business accounts, subscription state, message template, Calloto number
- `missed_calls` — caller number, timestamp, status (texted/replied/booked/ignored/withheld)
- `messages` — channel (sms/whatsapp), direction, body, provider_msg_id, status
- `bookings` — slot time, source (calendly/scheduler/reply)
- `usage` — monthly message counts and overage

## API Endpoints
```
POST /api/signup          — account creation + checkout
POST /api/checkout        — payment checkout URL
POST /api/webhook/payment — payment provider webhook
POST /api/webhook/call    — Voxvaani incoming call webhook
POST /api/webhook/message — Voxvaani inbound message webhook
GET  /api/dashboard       — (auth) business feed + usage
GET  /api/health          — health check
```

## File Structure (planned)
```
app/
  main.py              — FastAPI app, routes
  models.py            — SQLAlchemy models
  schemas.py           — Pydantic schemas
  services/
    telephony.py       — Voxvaani API integration
    messaging.py       — SMS/WhatsApp text-back
    billing.py         — Paddle/Stripe integration
    booking.py         — Calendly/scheduler integration
  webhooks.py          — Voxvaani + payment webhooks
  auth.py              — customer auth
  admin.py             — admin panel routes
static/                — HTML/JS frontend
templates/             — Jinja templates (if needed)
tests/
data/                  — SQLite DB (Docker /data volume mount)
```

## Do NOT
- Do not answer Voxvaani calls — just capture caller ID via webhook and hang up
- Do not store more caller data than necessary (GDPR)
- Do not use Stripe directly for UK B2C subscriptions (VAT compliance)
- Do not hardcode Voxvaani credentials — use environment variables
- Do not deploy without `/data` volume mount for DB persistence
