# Calloto — Product Requirements Document

## What It Does
Turns missed phone calls into booked jobs for UK tradespeople. When a business misses a call, Calloto instantly texts the caller back with the business's name, price range, and a booking link.

## Target Users
- **Primary:** UK tradespeople (plumbers, electricians, roofers, builders, locksmiths, HVAC, gardeners)
- **Secondary:** Salons, clinics, estate agents, repair services, dog groomers, cleaning services
- **Profile:** Solo operator or 2-5 person crew, works with hands, phone on silent/in van, high-value per job (£150-500+)

## Core Problem
- UK tradespeople miss ~27% of inbound calls
- 85% of callers who don't get an answer never call back — they call the next business
- A £200-500 job lost per missed call is normal; one recovered job pays for a year of Calloto

## Key Workflows

### 1. Signup & Onboarding (5 minutes)
1. Business signs up: name, email, phone number, trade vertical
2. Pays £19/month via Paddle/Lemon Squeezy
3. Configures text-back message template (pre-filled with name + price range + booking link)
4. Sets mobile to forward unanswered calls to their Calloto UK number
5. Optional: connects booking calendar (Calendly) or uses built-in scheduler
6. Receives test text-back to verify the loop

### 2. The Product Loop (Daily)
1. Customer calls business's existing number
2. Business is busy → call forwards to Calloto UK number (network-level, no app)
3. Calloto receives call → captures caller ID → drops call immediately
4. Calloto sends instant text-back (SMS or WhatsApp) with business branding + booking link
5. Caller taps link → books a slot (Calendly or built-in scheduler) or replies in chat
6. Business gets notified (WhatsApp/email): "New booking from missed call at 14:32"

### 3. Retention Loop (ROI Proof)
1. Dashboard shows: every missed call, every text sent, every reply, every booked job, £ value recovered
2. Weekly digest: "You recovered £480 this month from 24 missed calls — that's 25× your £19 fee"
3. Dashboard is the retention engine — product proves its own ROI

## Core Features (MVP v1.0)
- [ ] Customer accounts (email + password or magic link)
- [ ] Paddle/Lemon Squeezy subscription checkout + webhooks + billing portal
- [ ] Business profile: name, phone, trade vertical, text-back message template, price range
- [ ] UK phone number provisioning (Voxvaani: purchase/assign number per business)
- [ ] Incoming call webhook → missed-call record (caller number, timestamp, duration)
- [ ] Text-back engine: WhatsApp (Voxvaani API) + SMS (fallback)
- [ ] Messaging quota enforcement (100 messages/mo included, overage billed)
- [ ] Booking: Calendly embed + optional simple built-in scheduler
- [ ] Dashboard: missed-call feed, message log, booking log, £ recovered estimate
- [ ] Admin panel: list customers, force-refresh numbers, manual text-back, usage view
- [ ] Health/observability: /health, structured logs, error alerting

## Pricing
- £19/month single business, one number, unlimited missed calls
- Included: 100 text-back messages/month (SMS or WhatsApp combined)
- Overage: £0.05/message beyond 100
- Annual: 2 months free (£190/year)
- No contracts, cancel anytime, self-serve checkout

## Competitive Position
- UK incumbents: £49-297/month (Voco £49, SMB Booster £49-97, TimeToScale £197+, CaptureMyCalls £297)
- Calloto: £19/month, pure self-serve, WhatsApp-native, ROI dashboard
- US players ($97-259/mo) are US-focused; UK/AU WhatsApp-first positioning is the wedge

## Success Metrics
- Validation gate: 50+ real UK business signups in 3 weeks → scale; under 50 → pivot
- Target: 500 customers = £9,500/mo MRR; 1,000 = £19,000/mo MRR
- Gross margin: ~60-75% at £19/mo
