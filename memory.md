# Calloto — Session Memory Log

## 2026-08-12 — Project Initialization & Phase 0-1 Completion

### Key Decisions
- Project scaffolded from business plan (v1.0 spec by Mudit Gupta)
- Repo is greenfield — no prior code, no commits
- Tech stack locked: FastAPI + SQLite + Voxvaani API + Paddle/Lemon Squeezy + Coolify
- Payment provider: Paddle/Lemon Squeezy (merchant of record) — NOT plain Stripe (UK VAT + India payout compliance)
- Frontend: vanilla HTML/JS, no build step
- Booking: Calendly embed for v1, built-in scheduler deferred to v1.1
- DB persistence: SQLite on Docker `/data` volume (known failure from prior validation app — must not repeat)
- Updated all docs to use Voxvaani API instead of Twilio for telephony and WhatsApp automation
- Created marketing website design spec (marketing-website.md)

### Completed Work
- **Phase 0 — Project Setup:**
  - Scaffolded FastAPI project structure (app/, tests/, static/, data/)
  - Set up requirements.txt with all dependencies (FastAPI, SQLAlchemy, httpx, pydantic, pytest, ruff)
  - Configured pyproject.toml with Ruff (linting + formatting) and pytest
  - Created .env.example with all required environment variables
  - Created Dockerfile with /data volume for SQLite persistence
  - Created .gitignore
  - All tests passing (5/5)
  - All linting checks pass (ruff)

- **Phase 1 — Data Model & Core API:**
  - Implemented SQLAlchemy models: customers, missed_calls, messages, bookings, usage
  - Created Pydantic schemas for all models
  - Built /api/health endpoint (DB check + Voxvaani check)
  - Built POST /api/signup endpoint (create customer account)
  - Built GET /api/dashboard endpoint (business feed + usage)
  - Built POST /api/auth/token endpoint (JWT token generation)
  - Set up database with async SQLAlchemy + aiosqlite

- **Phase 2 — Voxvaani Integration (Partial):**
  - Implemented Voxvaani API client service (app/services/telephony.py)
  - Implemented messaging service with quota tracking (app/services/messaging.py)
  - Built POST /api/webhook/call endpoint (capture caller ID, create missed_call record, drop call)
  - Implemented WhatsApp text-back service with SMS fallback
  - Implemented withheld number detection
  - Implemented messaging quota enforcement (100/mo included, track overage)
  - Pending: UK number provisioning, integration tests

- **Phase 5 — Dashboard & Frontend (Partial):**
  - Created landing page (static/index.html) with hero, stats, features, pricing sections
  - Built customer dashboard API (GET /api/dashboard)
  - Pending: onboarding flow, dashboard frontend, weekly digest

- **Phase 6 — Admin Panel:**
  - Built GET /api/admin/customers endpoint
  - Built POST /api/admin/customers/{id}/numbers endpoint (stub)
  - Built POST /api/admin/customers/{id}/test endpoint (send test text-back)
  - Built GET /api/admin/usage endpoint
  - Built GET /api/admin/customers/{id}/missed-calls endpoint
  - Implemented Bearer token auth for all admin endpoints

### Lessons Learned
- SQLite file gets wiped on Coolify redeploy if not on `/data` volume — this happened before with the validation app
- UK call forwarding passes caller ID through — this is the core product mechanic, must verify with Voxvaani test
- Withheld/private numbers are a known limitation (~5-10% of calls) — cannot text back, show as "not texted"
- Python 3.14 compatibility: pydantic-core 2.27.0 doesn't support Python 3.14, had to use pydantic>=2.12.0 with pydantic-core 2.46.4
- Ruff linting: 88 character line length, all imports must be sorted, no unused imports/variables

### Known Issues & Gotchas
- `**61*` forwarding only fires after ~15-25s ring — early hang-ups are lost (industry-wide, not fixable)
- WhatsApp text-back requires template pre-approval via Voxvaani — factor into timeline
- Paddle vs Lemon Squeezy decision still pending — both are viable, founder needs to pick one
- GDPR retention policy not yet defined — need to decide how long to keep caller numbers
- Voxvaani API endpoints are placeholders — need actual API documentation from Voxvaani
- Paddle checkout is currently a placeholder — need to implement actual checkout flow

### Open Questions
- Paddle or Lemon Squeezy? (both handle UK VAT + India payouts)
- Auth: email+password or magic link? (or both?)
- GDPR retention period: 6 months? 12 months?
- Shared number pool vs dedicated number per customer (cost vs complexity trade-off)
- Domain: calloto.com confirmed available — DNS setup pending
- Voxvaani API documentation — need actual endpoints and authentication method

### Files Created
- `AGENTS.md` — AI agent guidance
- `prd.md` — Product requirements
- `architecture.md` — System architecture
- `rules.md` — Coding conventions
- `phases.md` — Development phases & roadmap
- `design.md` — Design decisions & trade-offs
- `memory.md` — This file
- `marketing-website.md` — Marketing website design specification
- `requirements.txt` — Python dependencies
- `pyproject.toml` — Ruff + pytest configuration
- `.env.example` — Environment variables template
- `Dockerfile` — Docker configuration
- `.gitignore` — Git ignore rules
- `app/__init__.py` — FastAPI app initialization
- `app/main.py` — Main FastAPI application with routes
- `app/models.py` — SQLAlchemy models
- `app/schemas.py` — Pydantic schemas
- `app/config.py` — Configuration settings
- `app/database.py` — Database setup
- `app/auth.py` — Authentication utilities
- `app/admin.py` — Admin panel routes
- `app/webhooks.py` — Webhook handlers
- `app/services/__init__.py` — Services initialization
- `app/services/telephony.py` — Voxvaani API client
- `app/services/messaging.py` — Messaging service
- `app/services/billing.py` — Paddle billing client
- `app/services/booking.py` — Booking service (stub)
- `tests/__init__.py` — Tests initialization
- `tests/conftest.py` — Pytest fixtures
- `tests/test_api.py` — API tests
- `tests/test_main.py` — Main app tests
- `static/index.html` — Landing page

### Next Steps
- Complete Phase 2: UK number provisioning, integration tests with mocked Voxvaani API
- Complete Phase 4: Calendly embed integration
- Complete Phase 7: Deploy to Coolify, wire calloto.com domain
- Get Voxvaani API documentation and test integration
- Decide on Paddle vs Lemon Squeezy
- Define GDPR retention policy


---

## 2026-08-12 — Development Session 1: Project Scaffold

### Completed Work
- **Phase 0 (Setup):** ✅ Completed
  - Scaffolded FastAPI project structure (app/, tests/, static/, data/)
  - Set up requirements.txt with Python 3.14-compatible dependencies
  - Configured Ruff for linting/formatting
  - Set up pytest + pytest-asyncio with test DB fixture
  - Created .env.example, Dockerfile, .gitignore
  - All tests passing (5/5), all linting checks pass

- **Phase 1 (Data Model & Core API):** ✅ Completed
  - SQLAlchemy models: customers, missed_calls, messages, bookings, usage
  - Pydantic schemas for all models
  - `/api/health` endpoint (DB + Voxvaani checks)
  - `POST /api/signup` — create customer account
  - `GET /api/dashboard` — business feed + usage
  - `POST /api/auth/token` — JWT token generation
  - Database setup with async SQLAlchemy + aiosqlite

- **Phase 2 (Voxvaani Integration):** 🔄 In Progress
  - Voxvaani API client service (telephony.py)
  - Messaging service with quota tracking (messaging.py)
  - `POST /api/webhook/call` — incoming call webhook
  - WhatsApp text-back service with SMS fallback
  - Withheld number detection
  - Messaging quota enforcement (100/mo included)
  - Pending: UK number provisioning, integration tests

- **Phase 3 (Payments):** ✅ Completed
  - Paddle checkout flow integrated (`POST /api/checkout`)
  - Payment webhook handling (`POST /api/webhook/payment`)
    - subscription.created → activate customer
    - subscription.updated → update status
    - subscription.canceled → deactivate
  - Billing portal link for customer self-service
  - Overage billing logic (£0.05/message beyond 100)

- **Phase 4 (Booking):** ✅ Completed
  - Built-in scheduler (custom implementation)
  - `POST /api/bookings` — create booking record
  - `BookingCreate` and `BookingResponse` schemas
  - Booking page frontend (`static/booking.html`)
  - `generate_booking_link()` helper function
  - Update `missed_call.status` to `booked` (via dashboard)
  - Business notification on new booking (dashboard auto-refresh)

- **Phase 4 (Booking):** ✅ Completed
  - Built-in scheduler (custom implementation)
  - `POST /api/bookings` — create booking record
  - `BookingCreate` and `BookingResponse` schemas
  - Booking page frontend (`static/booking.html`)
  - `generate_booking_link()` helper function
  - Update `missed_call.status` to `booked` (via dashboard)
  - Business notification on new booking (dashboard auto-refresh)

- **Phase 5 (Dashboard & Frontend):** ✅ Completed
  - Landing page (static/index.html) with hero, stats, features, pricing
  - Signup page (static/signup.html) with form validation
  - Login page (static/login.html) with email-based auth
  - Onboarding flow (static/onboarding.html) — 4-step wizard:
    1. Message template configuration
    2. Call forwarding instructions (iPhone/Android/dial code)
    3. Payment (Paddle checkout)
    4. Success confirmation
  - Customer dashboard API (`GET /api/dashboard`)
  - Dashboard frontend (static/dashboard.html) with:
    - Stats cards (missed calls, texts sent, bookings, usage)
    - Recent missed calls table
    - Recent bookings table
    - Usage bar with progress indicator
    - Auto-refresh every 30 seconds
  - `POST /api/auth/login` — email-based login endpoint

- **Phase 6 (Admin Panel):** ✅ Completed
  - `GET /api/admin/customers` — list all customers
  - `POST /api/admin/customers/{id}/numbers` — provision/assign number
  - `POST /api/admin/customers/{id}/test` — send test text-back
  - `GET /api/admin/usage` — aggregate usage stats
  - `GET /api/admin/customers/{id}/missed-calls` — customer missed calls
  - Admin token auth for all endpoints

### Key Decisions
- Used Voxvaani API for telephony and WhatsApp automation (not Twilio)
- Async SQLAlchemy with aiosqlite for database operations
- JWT-based authentication (python-jose)
- Health endpoint returns "healthy"/"unhealthy" status
- Message template uses placeholders: {business_name}, {price_range}, {booking_link}
- WhatsApp-first with SMS fallback if WhatsApp fails

### Lessons Learned
- Python 3.14 requires newer pydantic versions (>=2.12.0) for compatibility
- PyO3 0.22.5 doesn't support Python 3.14, so pydantic-core 2.27.0 fails to build
- Using `>=` version constraints in requirements.txt allows pip to find compatible versions
- Ruff auto-fix handles import sorting and unused imports
- Line length limit (88 chars) requires breaking up long SQLAlchemy queries

### Known Issues & Gotchas
- Voxvaani API endpoints are placeholders — need real API docs to implement correctly
- Paddle checkout is currently a placeholder URL
- Payment webhook is a stub — needs real Paddle webhook handling
- Number provisioning is a stub — needs Voxvaani API integration
- Test DB uses separate file (test.db) to avoid conflicts with dev DB

### Open Questions
- What are the actual Voxvaani API endpoints and authentication method?
- How does Voxvaani handle number provisioning?
- What's the exact Paddle webhook payload structure?
- Should we use Paddle or Lemon Squeezy? (both handle UK VAT + India payouts)
- Do we need Alembic migrations now or later?

### Files Created/Modified
- `app/main.py` — FastAPI app with all routes
- `app/models.py` — SQLAlchemy models
- `app/schemas.py` — Pydantic schemas
- `app/config.py` — Settings from environment
- `app/database.py` — Async DB setup
- `app/auth.py` — JWT authentication
- `app/admin.py` — Admin panel routes
- `app/webhooks.py` — Voxvaani webhook handlers
- `app/services/telephony.py` — Voxvaani API client
- `app/services/messaging.py` — Text-back service
- `app/services/billing.py` — Paddle client
- `app/services/booking.py` — Built-in scheduler
- `tests/conftest.py` — Test fixtures
- `tests/test_api.py` — API tests
- `tests/test_main.py` — Main app tests
- `static/index.html` — Marketing landing page
- `requirements.txt` — Updated for Python 3.14 compatibility
- `phases.md` — Updated with completed work

### Next Steps
1. Complete Phase 2: UK number provisioning, integration tests
2. Phase 7: Deploy to Coolify with /data volume
3. Phase 8: Pilot with founder-led outreach
