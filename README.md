# CallCatch — missed-call text-back for UK trades

Never lose a job to a missed call. Missed call → instant text-back with your name, price and booking link.

- Landing: `/` (index.html)
- Waitlist API: FastAPI + SQLite
- Admin endpoints protected by `WAITLIST_ADMIN_TOKEN` (Bearer header)
- DB at `/data/waitlist.db` (mount a volume; container-local otherwise)

Run: `uvicorn api:app --host 0.0.0.0 --port 8000`

## Voxvaani integration (product roadmap)

The eventual product reuses Voxvaani's stack:
1. Missed-call detection (Voxvaani virtual numbers / call logs webhook)
2. Auto text-back via Voxvaani WhatsApp API (DLT-compliant templates) or SMS
3. Booking link via Calendly/own scheduler
4. Missed-call feed dashboard

Validation first: this landing + waitlist. Build only if 50+ real signups in 3 weeks.
