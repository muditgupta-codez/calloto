import hashlib
import hmac
import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin import router as admin_router
from app.auth import create_access_token
from app.config import settings
from app.database import async_session, engine, get_db
from app.models import Base, Booking, Customer, Message, MissedCall, Usage
from app.schemas import (
    BookingCreate,
    BookingResponse,
    CustomerCreate,
    CustomerResponse,
    DashboardResponse,
    HealthResponse,
    MissedCallResponse,
)
from app.services.telephony import voxvaani_client
from app.webhooks import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        result = await conn.execute(
            text("PRAGMA table_info(customers)")
        )
        columns = [row[1] for row in result.fetchall()]
        if "trial_ends_at" not in columns:
            await conn.execute(
                text("ALTER TABLE customers ADD COLUMN trial_ends_at DATETIME")
            )
    yield


app = FastAPI(title="Calloto", lifespan=lifespan)


@app.middleware("http")
async def prevent_stale_frontend(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

app.include_router(webhook_router)
app.include_router(admin_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


def _serve_static(name: str) -> HTMLResponse:
    with open(f"static/{name}", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return _serve_static("terms.html")


@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return _serve_static("privacy.html")


@app.get("/refund-policy", response_class=HTMLResponse)
async def refund_policy():
    return _serve_static("refund-policy.html")


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    db_status = "healthy"
    try:
        async with async_session() as session:
            await session.execute(select(1))
    except Exception:
        db_status = "unhealthy"

    voxvaani_status = "healthy" if await voxvaani_client.health_check() else "unhealthy"

    return HealthResponse(
        status="healthy" if db_status == "healthy" else "unhealthy",
        database=db_status,
        voxvaani=voxvaani_status,
    )


@app.post("/api/signup", response_model=CustomerResponse)
async def signup(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Customer).where(Customer.email == customer.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_customer = Customer(
        email=customer.email,
        name=customer.name,
        phone=customer.phone,
        trade_vertical=customer.trade_vertical,
        message_template=(
            "Hi! {business_name} missed your call. "
            "Rough price {price_range}. "
            "Book your job here: {booking_link}"
        ),
        subscription_status="trial",
        trial_ends_at=datetime.now() + timedelta(days=14),
    )
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer


@app.post("/api/checkout")
async def checkout(
    customer_id: int, db: AsyncSession = Depends(get_db)
):
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {
        "client_token": settings.paddle_client_token,
        "price_id": settings.paddle_price_id,
        "customer_email": customer.email,
        "customer_id": customer.id,
        "success_url": f"{settings.app_url}/static/dashboard.html?upgraded=1",
    }


async def _find_customer_by_custom_id(
    custom_data: dict | None, db: AsyncSession
) -> Customer | None:
    if not custom_data or not custom_data.get("customer_id"):
        return None
    try:
        customer_db_id = int(custom_data["customer_id"])
    except (TypeError, ValueError):
        return None
    return await db.get(Customer, customer_db_id)


@app.post("/api/webhook/payment")
async def payment_webhook(
    request: Request, db: AsyncSession = Depends(get_db)
):
    body = await request.body()
    signature = request.headers.get("paddle-signature", "")
    if not _verify_paddle_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = json.loads(body)
    event_type = payload.get("event_type")
    event_data = payload.get("data", {})

    if event_type == "transaction.completed":
        customer = await _find_customer_by_custom_id(
            event_data.get("custom_data"), db
        )
        if customer:
            customer.subscription_status = "active"
            customer.paddle_customer_id = event_data.get("customer_id")
            await db.commit()

    elif event_type == "subscription.activated":
        customer = await _find_customer_by_custom_id(
            event_data.get("custom_data"), db
        )
        if customer:
            customer.subscription_status = "active"
            customer.paddle_customer_id = event_data.get("customer_id")
            await db.commit()

    elif event_type == "subscription.cancelled":
        customer = await _find_customer_by_custom_id(
            event_data.get("custom_data"), db
        )
        if customer:
            customer.subscription_status = "cancelled"
            await db.commit()

    elif event_type == "subscription.updated":
        customer = await _find_customer_by_custom_id(
            event_data.get("custom_data"), db
        )
        status = event_data.get("status")
        if customer and status:
            customer.subscription_status = status
            await db.commit()

    return {"status": "ok"}


def _verify_paddle_signature(payload: bytes, signature: str) -> bool:
    if not settings.paddle_webhook_secret:
        return settings.app_env == "development"
    parts = dict(item.split("=", 1) for item in signature.split(";") if "=" in item)
    timestamp = parts.get("ts")
    signature_value = parts.get("h1")
    if not timestamp or not signature_value:
        return False
    signed_payload = f"{timestamp}:{payload.decode()}".encode()
    expected = hmac.new(
        settings.paddle_webhook_secret.encode(), signed_payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_value)


@app.get("/api/dashboard", response_model=DashboardResponse)
async def dashboard(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer_result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = customer_result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    calls_result = await db.execute(
        select(MissedCall)
        .where(MissedCall.customer_id == customer_id)
        .order_by(MissedCall.called_at.desc())
        .limit(50)
    )
    missed_calls = calls_result.scalars().all()

    messages_result = await db.execute(
        select(Message)
        .where(Message.customer_id == customer_id)
        .order_by(Message.sent_at.desc())
        .limit(50)
    )
    messages = messages_result.scalars().all()

    bookings_result = await db.execute(
        select(Booking)
        .where(Booking.customer_id == customer_id)
        .order_by(Booking.created_at.desc())
        .limit(50)
    )
    bookings = bookings_result.scalars().all()

    current_month = datetime.now().strftime("%Y-%m")
    usage_result = await db.execute(
        select(Usage).where(
            Usage.customer_id == customer_id,
            Usage.month == current_month,
        )
    )
    usage = usage_result.scalar_one_or_none()

    return DashboardResponse(
        customer=CustomerResponse.model_validate(customer),
        missed_calls=[MissedCallResponse.model_validate(mc) for mc in missed_calls],
        messages=messages,
        bookings=bookings,
        usage=usage,
    )


@app.post("/api/bookings")
async def create_booking(
    booking: BookingCreate, db: AsyncSession = Depends(get_db)
):
    customer = await db.get(Customer, booking.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    slot_time = datetime.strptime(
        f"{booking.date} {booking.time}", "%Y-%m-%d %H:%M"
    )

    new_booking = Booking(
        customer_id=booking.customer_id,
        slot_time=slot_time,
        source="scheduler",
    )
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)

    return BookingResponse.model_validate(new_booking)


@app.post("/api/auth/login")
async def login(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == email))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    token = create_access_token(data={"sub": customer.id})
    return {"customer_id": customer.id, "access_token": token}


@app.post("/api/auth/token")
async def get_token(customer_id: int):
    token = create_access_token(data={"sub": customer_id})
    return {"access_token": token, "token_type": "bearer"}
