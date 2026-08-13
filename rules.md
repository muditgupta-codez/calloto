# Calloto — Project Rules & Conventions

## Code Style
- **Language:** Python 3.11+
- **Formatter:** Ruff (replaces black + isort + flake8)
- **Type hints:** Required on all function signatures
- **Line length:** 88 characters (Ruff default)
- **Quotes:** Double quotes for strings, single quotes only inside f-strings
- **Imports:** Absolute imports, sorted by Ruff (stdlib → third-party → local)
- **Async:** Use `async def` for all route handlers and I/O-bound service methods

## Naming Conventions
- **Files/modules:** `snake_case` (e.g., `messaging.py`, `telephony.py`)
- **Classes:** `PascalCase` (e.g., `MissedCall`, `CustomerService`)
- **Functions/variables:** `snake_case` (e.g., `get_customer`, `caller_number`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_FREE_MESSAGES = 100`)
- **API routes:** `kebab-case` segments (e.g., `/api/webhook/call`, `/api/admin/customers`)
- **DB columns:** `snake_case` (e.g., `caller_number`, `created_at`)
- **Env vars:** `UPPER_SNAKE_CASE` (e.g., `VOXVAANI_API_KEY`, `DATABASE_URL`)

## Directory Structure
```
app/                    — All Python source code
  services/             — Business logic, external integrations
static/                 — Frontend HTML/JS/CSS (served as-is)
tests/                  — pytest tests, mirrors app/ structure
data/                   — SQLite DB file (Docker /data volume mount)
```
- One module per responsibility — no god-files
- Service modules are stateless functions, not classes (unless state is genuinely needed)
- Keep route handlers thin — delegate to service layer

## Database Rules
- Use SQLAlchemy 2.0 style (`select()`, not `session.query()`)
- All models must have `id`, `created_at` at minimum
- Use `server_default` for DB-side defaults, `default` for Python-side
- Never use SQLite-specific types — keep schema Postgres-compatible
- All migrations via Alembic — no manual schema changes
- Foreign keys with `ondelete="CASCADE"` where appropriate

## API Rules
- All routes prefixed with `/api/`
- Webhook endpoints: `/api/webhook/` namespace
- Return Pydantic models, not raw dicts
- Use HTTP status codes correctly: 200, 201, 400, 401, 403, 404, 422, 500
- Validate all webhook signatures before processing
- Never expose internal IDs in public responses — use UUIDs or opaque tokens

## Security Rules
- **No secrets in code** — all credentials via environment variables
- **No plain Stripe** for UK B2C — use Paddle/Lemon Squeezy (merchant of record)
- **Validate all webhooks** — Voxvaani signature, Paddle/LS signature
- **Caller numbers are PII** — treat as GDPR personal data
- **Minimal data storage** — only store what's needed for the product
- **HTTPS only** — no HTTP endpoints in production

## Git & Commit Conventions
- **Branch naming:** `feat/`, `fix/`, `chore/`, `docs/` prefix (e.g., `feat/voxvaani-webhook`)
- **Commit messages:** Conventional Commits format:
  - `feat: add Voxvaani call webhook handler`
  - `fix: correct message quota calculation`
  - `chore: update dependencies`
- **One logical change per commit** — don't mix unrelated changes
- **No merge commits** — rebase onto main
- **Never commit:** `.env`, `data/*.db`, credentials, API keys

## Do's
- Write tests for all service-layer functions
- Use structured logging (`structlog` or `logging` with JSON formatter)
- Handle Voxvaani API errors explicitly (rate limits, invalid numbers)
- Log all webhook payloads for debugging (redact PII)
- Use Pydantic v2 for all request/response validation
- Keep the frontend simple — vanilla JS or Alpine.js, no React/Vue build step

## Don'ts
- Don't answer Voxvaani calls — capture caller ID and hang up immediately
- Don't store more caller data than necessary (GDPR)
- Don't use Stripe directly for UK B2C subscriptions (VAT compliance)
- Don't hardcode Voxvaani/Paddle credentials
- Don't deploy without `/data` volume mount for DB persistence
- Don't use `print()` for logging — use `logging` module
- Don't block the event loop — use `asyncio.to_thread()` for sync I/O
- Don't use raw SQL — use SQLAlchemy ORM or `text()` for complex queries only
- Don't add frontend build tools (webpack, vite) — keep it simple

## Testing
- **Framework:** pytest + pytest-asyncio
- **Coverage target:** 80%+ on service layer
- **Test structure:** `tests/test_<module>.py` mirrors `app/<module>.py`
- **Fixtures:** Use `conftest.py` for shared fixtures (test DB, mock Voxvaani client)
- **Mock external services:** Never hit Voxvaani/Paddle in tests — use `httpx` mocks or `unittest.mock`
- **Run:** `pytest` (all), `pytest tests/test_telephony.py` (single module)

## Environment Variables
Required (document in `.env.example`):
```
VOXVAANI_API_KEY=
VOXVAANI_API_SECRET=
DATABASE_URL=sqlite+aiosqlite:///./data/calloto.db
SECRET_KEY=
ADMIN_TOKEN=
PADDLE_VENDOR_ID=
PADDLE_API_KEY=
APP_ENV=development|production
```

## Linting & Checks
```bash
ruff check .              # Lint
ruff format --check .     # Format check
pytest                    # Tests
```
Run all three before committing. CI will enforce.
