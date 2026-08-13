"""Calloto — waitlist API (validation test).

Self-contained: FastAPI + SQLite. No external deps beyond fastapi/uvicorn.
Endpoints:
  POST /api/waitlist   {email, company?, country?, segment?} -> 201 {id, position}
  GET  /api/waitlist/count -> {count}
  GET  /health -> ok
Admin (Bearer token from WAITLIST_ADMIN_TOKEN):
  GET    /api/waitlist  -> list all entries
  DELETE /api/waitlist  -> clear all entries
"""
import os
import re
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, Field

DB_PATH = Path(os.environ.get("DB_PATH", "/data/waitlist.db"))
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ADMIN_TOKEN = os.environ.get("WAITLIST_ADMIN_TOKEN", "change-me")

app = FastAPI(title="Calloto Waitlist", docs_url=None, redoc_url=None)

@app.middleware("http")
async def _no_cache(request, call_next):
    """Validation landing: never let browsers/WhatsApp webviews cache the page
    (the waitlist counter + copy change often; stale cache caused 'old page'
    reports)."""
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["*"],
)


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS waitlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                company TEXT,
                country TEXT,
                segment TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


class WaitlistEntry(BaseModel):
    email: EmailStr
    company: str | None = Field(default=None, max_length=120)
    country: str | None = Field(default=None, max_length=2)
    segment: str | None = Field(default=None, max_length=60)


@app.on_event("startup")
def _startup() -> None:
    _init_db()


@app.post("/api/waitlist", status_code=201)
def join_waitlist(entry: WaitlistEntry) -> dict:
    email = entry.email.lower().strip()
    if not EMAIL_RE.match(email):
        raise HTTPException(status_code=400, detail="Invalid email address")

    disposable = {"mailinator.com", "yopmail.com", "guerrillamail.com",
                  "tempmail.com", "throwaway.com", "10minutemail.com"}
    if email.split("@")[1] in disposable:
        raise HTTPException(status_code=400, detail="Please use a business email")

    now = datetime.now(timezone.utc).isoformat()
    with _conn() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO waitlist (email, company, country, segment, created_at) VALUES (?,?,?,?,?)",
                (email, entry.company, entry.country, entry.segment, now),
            )
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="You're already on the list")
        row = conn.execute("SELECT COUNT(*) AS c FROM waitlist").fetchone()

    return {"id": cur.lastrowid, "position": row["c"], "created_at": now}


@app.get("/api/waitlist/count")
def waitlist_count() -> dict:
    with _conn() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM waitlist").fetchone()
    return {"count": row["c"]}


def _admin_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Admin token required")
    token = authorization.removeprefix("Bearer ").strip()
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return token


@app.get("/api/waitlist")
def waitlist_list(authorization: str | None = Header(default=None)) -> list[dict]:
    """Admin: list all entries. Requires Authorization: Bearer <ADMIN_TOKEN>."""
    _admin_token(authorization)
    with _conn() as conn:
        rows = conn.execute(
            "SELECT id, email, company, country, segment, created_at FROM waitlist ORDER BY id"
        ).fetchall()
    return [dict(r) for r in rows]


@app.delete("/api/waitlist")
def waitlist_clear(authorization: str | None = Header(default=None)) -> dict:
    """Admin: clear all entries. Requires Authorization: Bearer <ADMIN_TOKEN>."""
    _admin_token(authorization)
    with _conn() as conn:
        conn.execute("DELETE FROM waitlist")
    return {"cleared": True}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "ts": int(time.time())}


@app.get("/")
def landing() -> FileResponse:
    return FileResponse(Path(__file__).parent / "index.html", media_type="text/html")
