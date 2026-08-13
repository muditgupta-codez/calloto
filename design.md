# Calloto — Design Decisions

## Architecture Decisions

### FastAPI over Django/Flask
- **Why:** Async-native (critical for webhook handling), automatic OpenAPI docs, Pydantic integration, fastest Python framework for I/O-bound work
- **Trade-off:** Smaller ecosystem than Django, but we don't need Django's ORM/admin/auth — we're building lean
- **Alternatives considered:** Flask (no async, would need extra work for webhooks), Django (overkill for validation stage)

### SQLite → Postgres (not Postgres from day one)
- **Why:** Validation stage doesn't need Postgres complexity. SQLite is zero-config, single-file, easy to backup/inspect. Schema is Postgres-ready (standard SQL types, no SQLite-specific features)
- **Trade-off:** Limited concurrency (~1000 customers is the practical limit), but that's fine for validation
- **Migration path:** Alembic migrations work for both. When we hit scale, migrate data + switch `DATABASE_URL`
- **Alternatives considered:** Postgres from day one (unnecessary complexity for 0 users), Supabase (vendor lock-in)

### Paddle/Lemon Squeezy over Stripe
- **Why:** Merchant of record model handles UK VAT (20%) + India payouts with zero compliance burden. Stripe would require us to register for UK VAT, file returns, handle India FEMA compliance
- **Trade-off:** Higher per-transaction fees (~5% vs Stripe's 2.9%), but the VAT/compliance savings are worth it at validation stage
- **Alternatives considered:** Stripe + Stripe Tax (works, but more compliance work), Stripe Atlas (US entity, doesn't solve India payout)

### Voxvaani API for Telephony & WhatsApp
- **Why:** Founder operates the Voxvaani voice/WhatsApp automation stack. Single provider for call handling, call webhooks, and WhatsApp automation — no need to integrate separate telephony + WhatsApp BSP. Existing infrastructure and expertise
- **Trade-off:** Smaller ecosystem than Twilio, but founder has deep Voxvaani experience and the API covers all product needs (call webhooks, WhatsApp messaging, number management)
- **Alternatives considered:** Twilio (more docs/community, but redundant — Voxvaani already handles the same flows), Vonage/Plivo (no advantage over Voxvaani for this use case)

### Single-page HTML/JS over React/Vue
- **Why:** No build step, fast to iterate, simple to deploy (static files served by FastAPI), founder has existing pattern from previous landing pages
- **Trade-off:** Less component reusability, but the dashboard is simple enough that vanilla JS + Alpine.js handles it fine
- **Alternatives considered:** React + Vite (overkill for validation), HTMX (interesting but less familiar to team)

### Calendly embed over built-in scheduler (v1)
- **Why:** Zero build time for booking — Calendly handles timezones, availability, reminders, all the edge cases. Business already knows how to use it
- **Trade-off:** Less control over UX, Calendly branding visible, but it's good enough for validation
- **Migration path:** Built-in scheduler in v1.1 once we validate demand and understand booking patterns

## UI/UX Decisions

### Dashboard as Retention Engine
- **Why:** The product proves its own ROI. Every missed call, text, reply, and booking is visible. The weekly "£ recovered" number makes churn irrational
- **Design:** Feed-style layout (most recent first), clear status badges (texted/replied/booked/withheld), usage meter always visible
- **Trade-off:** More data = more cognitive load, but tradespeople want to see the money, not analytics charts

### Onboarding: 5 Minutes or Less
- **Why:** Self-serve only. If onboarding takes more than 5 minutes, conversion drops. Pre-filled message template + clear forwarding instructions (with screenshots for iPhone/Android)
- **Design:** Step-by-step wizard: profile → message template → call forwarding → test text-back → done
- **Trade-off:** Less flexibility (no custom branding in v1), but speed-to-value matters more

### Text-back Message Template
- **Why:** Consistent, branded, includes booking link. Pre-filled with `{business_name}`, `{price_range}`, `{booking_link}` placeholders
- **Design:** "Hi! {business_name} missed your call. Rough price {price_range}. Book your job here: {booking_link}"
- **Trade-off:** Less personalization, but consistency reduces support burden and ensures compliance (PECR)

### No App, No Login for Callers
- **Why:** The caller experience is: receive text → tap link → book. No app download, no account creation. Friction kills conversion
- **Design:** Text-back → Calendly embed (or built-in scheduler) → confirmation. That's it
- **Trade-off:** Less data capture (no caller email/name), but the booking itself is the goal

## Security & Compliance Decisions

### GDPR: Minimal Data Storage
- **Why:** Caller numbers are personal data. Store only what's needed: number, timestamp, status. No names, no addresses, no call recordings
- **Retention policy:** <!-- TODO: Define retention period (suggest 12 months for missed calls, then archive/delete) -->
- **Trade-off:** Can't build rich caller profiles, but reduces GDPR risk

### PECR: Text-backs are Transactional
- **Why:** Text-backs are triggered by the caller's own inbound call. This is a transactional response, not unsolicited marketing. No opt-in required
- **Trade-off:** Legal interpretation could be challenged, but this is the standard industry position (same as competitors)
- **Mitigation:** Don't use the system for broadcast marketing without consent

### Webhook Signature Validation
- **Why:** Voxvaani and Paddle/LS webhooks must be validated to prevent spoofing. Without validation, attackers could fake missed calls or subscription events
- **Implementation:** Voxvaani webhook signature validation, Paddle/LS webhook signature (HMAC-SHA256)
- **Trade-off:** Adds complexity to webhook handlers, but security is non-negotiable

## Performance Decisions

### Drop Calls Immediately (Don't Answer)
- **Why:** Voxvaani charges per second for answered calls. Dropping the call after capturing caller ID (via webhook) saves money. The caller doesn't hear a ringtone — they just get a text-back
- **Trade-off:** Caller might think the call failed, but the instant text-back compensates
- **Implementation:** Drop call via Voxvaani API immediately after capturing caller ID in webhook

### Async Webhook Handlers
- **Why:** Webhooks are I/O-bound (DB writes, Voxvaani API calls). Async handlers prevent blocking and improve throughput
- **Trade-off:** More complex code (async/await), but FastAPI makes it ergonomic
- **Implementation:** All webhook handlers are `async def`, use `aioSQLite` for DB, `httpx` for Voxvaani API calls

## Cost Optimization Decisions

### Shared Number Pool (Future)
- **Why:** Voxvaani UK numbers cost ~£1/month each. For validation, assign one number per customer. At scale, consider shared pool (route by caller ID → customer mapping)
- **Trade-off:** Shared pool adds routing complexity, but saves £1/customer/month at scale
- **Migration path:** v1.1 or when we hit 500+ customers

### WhatsApp over SMS (When Possible)
- **Why:** WhatsApp messages are cheaper per conversation at volume (~£0.03 vs ~£0.08 for SMS). UK WhatsApp penetration is ~85%, so most callers can receive WhatsApp
- **Trade-off:** WhatsApp requires template approval, less universal than SMS
- **Implementation:** Try WhatsApp first, fall back to SMS if WhatsApp fails (number not on WhatsApp)

## Known Limitations (Accepted)

### Forward-when-unanswered Misses Early Hang-ups
- **Why:** UK call forwarding fires after ~15-25 seconds. Callers who hang up after 2 rings are missed
- **Mitigation:** Document this limitation in onboarding. Dashboard shows it transparently. Same limitation affects all competitors

### Withheld Numbers Can't Be Texted
- **Why:** Private/withheld caller numbers arrive as "withheld" — can't send text-back
- **Mitigation:** Show as "not texted" in dashboard. Message template can tell callers to remove number blocking if they want fast replies

### SQLite Concurrency Limit
- **Why:** SQLite handles ~1000 concurrent writers max. Beyond that, need Postgres
- **Mitigation:** Validation stage won't hit this limit. Migration path is clear (Alembic + Postgres-ready schema)
