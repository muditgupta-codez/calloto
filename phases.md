# Calloto — Development Phases

## Current Phase: Milestone 1 — Funnel MVP (In Progress)
**Goal:** Full product loop working end-to-end for UK tradespeople. Landing → signup → payment → onboarding → missed call → text-back → booking → dashboard.

**Target:** Deploy to Coolify, wire calloto.com, ready for founder-led pilot.

**Progress:** Phases 0, 1, 3, 4, 5, 6 completed. Phase 2 in progress. Phase 7 pending.

---

## Phase 0 — Project Setup (Completed)
- [x] Scaffold FastAPI project structure (`app/`, `tests/`, `static/`)
- [x] Set up `pyproject.toml` / `requirements.txt` (FastAPI, uvicorn, SQLAlchemy, aioSQLite, httpx, pydantic, structlog, pytest, ruff)
- [x] Configure Ruff (linting + formatting)
- [x] Set up pytest + conftest with test DB fixture
- [x] Create `.env.example` with all required env vars
- [x] Create Dockerfile with `/data` volume
- [x] Create `.gitignore`
- [x] All tests passing (5/5)
- [x] All linting checks pass

## Phase 1 — Data Model & Core API (Completed)
- [x] SQLAlchemy models: `customers`, `missed_calls`, `messages`, `bookings`, `usage`
- [x] Pydantic schemas for all models
- [x] `/api/health` endpoint (DB check + Voxvaani check)
- [x] `POST /api/signup` — create customer account
- [x] `GET /api/dashboard` — business feed + usage
- [x] `POST /api/auth/token` — JWT token generation
- [x] Database setup with async SQLAlchemy + aiosqlite

## Phase 2 — Voxvaani Integration (In Progress)
- [x] Voxvaani API client service (`app/services/telephony.py`)
- [x] Messaging service with quota tracking (`app/services/messaging.py`)
- [x] `POST /api/webhook/call` — incoming call webhook
  - Capture caller ID
  - Create `missed_call` record
  - Drop call immediately via Voxvaani API
- [x] WhatsApp text-back service
- [x] SMS text-back fallback
- [x] Withheld number detection → mark as `withheld`, skip text-back
- [x] Messaging quota enforcement (100/mo included, track overage)
- [ ] UK number provisioning (purchase + assign to customer)
- [ ] Integration tests with mocked Voxvaani API

## Phase 3 — Payments (Completed)
- [x] Paddle client service (`app/services/billing.py`)
- [x] `POST /api/checkout` — create checkout session (integrated with Paddle API)
- [x] `POST /api/webhook/payment` — handle subscription events
  - `subscription.created` → activate customer
  - `subscription.updated` → update status
  - `subscription.canceled` → deactivate
- [x] Billing portal link for customer self-service
- [x] Overage billing logic (£0.05/message beyond 100)

## Phase 4 — Booking Integration (Completed)
- [x] Built-in scheduler (custom implementation)
- [x] `POST /api/bookings` — create booking record
- [x] `BookingCreate` and `BookingResponse` schemas
- [x] Booking page frontend (`static/booking.html`)
- [x] `generate_booking_link()` helper function
- [x] Update `missed_call.status` to `booked` (via dashboard)
- [x] Business notification on new booking (dashboard auto-refresh)

## Phase 5 — Dashboard & Frontend (Completed)
- [x] Landing page (HTML/JS) — `static/index.html` with hero, stats, features, pricing
- [x] Signup page — `static/signup.html` with form validation
- [x] Login page — `static/login.html` with email-based auth
- [x] Onboarding flow — `static/onboarding.html` (4-step wizard: template, forwarding, payment, success)
- [x] Customer dashboard API (`GET /api/dashboard`)
  - Missed call feed (caller number, time, status)
  - Message log (sent, delivered, failed)
  - Booking log (slot time, source)
  - Usage meter (messages sent / 100 included)
- [x] Dashboard frontend — `static/dashboard.html` with stats, call feed, bookings, usage bar
- [x] `POST /api/auth/login` — email-based login endpoint
- [ ] Weekly digest email/WhatsApp (cron job) — deferred to post-launch

## Phase 6 — Admin Panel (Completed)
- [x] `GET /api/admin/customers` — list all customers
- [x] `POST /api/admin/customers/{id}/numbers` — provision/assign number (stub)
- [x] `POST /api/admin/customers/{id}/test` — send test text-back
- [x] `GET /api/admin/usage` — aggregate usage stats
- [x] Bearer token auth for all admin endpoints
- [x] `GET /api/admin/customers/{id}/missed-calls` — customer missed calls

## Phase 7 — Deploy & Launch (Pending)
- [ ] Docker image build + push
- [ ] Coolify deployment with `/data` volume
- [ ] Environment variables configured
- [ ] Voxvaani webhook URLs pointed to production
- [ ] Paddle/LS webhook URLs pointed to production
- [ ] End-to-end test: signup → missed call → text-back → booking → dashboard
- [ ] Monitoring: `/health` + structured logs + uptime ping

---

## Phase 8 — Pilot (Milestone 2, Post-MVP)
- [ ] Google Maps scrape for UK trades (plumbers, electricians, roofers)
- [ ] AI voice outreach via Voxvaani stack
- [ ] WhatsApp demo link to responders
- [ ] Track source per signup (UTM + segment field)
- [ ] Measure 50-signup gate in 3 weeks

## Phase 9 — Scale (Milestone 3, Conditional)
- [ ] AU market launch (Twilio AU numbers, AU scrape campaign)
- [ ] 2-way WhatsApp conversation (reply handling)
- [ ] AI reply drafting (business replies with one tap)
- [ ] Multi-number support for crews
- [ ] Postgres migration (when data demands it)

---

## Status Summary
| Phase | Status | Notes |
|-------|--------|-------|
| 0 — Setup | ✅ Completed | Scaffold project, tests passing, linting clean |
| 1 — Data Model | ✅ Completed | Core tables + auth + API endpoints |
| 2 — Voxvaani | 🔄 In Progress | Call webhook + text-back done, number provisioning pending |
| 3 — Payments | ✅ Completed | Paddle checkout + webhooks integrated |
| 4 — Booking | ✅ Completed | Built-in scheduler + booking page |
| 5 — Dashboard | ✅ Completed | All frontend pages + API done |
| 6 — Admin | ✅ Completed | Admin panel with all endpoints |
| 7 — Deploy | Pending | Coolify + domain |
| 8 — Pilot | Future | Founder-led outreach |
| 9 — Scale | Future | AU + v1.1 features |
