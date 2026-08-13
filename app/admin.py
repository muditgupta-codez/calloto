from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import Customer, MissedCall, Usage
from app.schemas import CustomerResponse, MissedCallResponse, UsageResponse
from app.services.messaging import send_text_back
from app.services.telephony import voxvaani_client

router = APIRouter(prefix="/api/admin")


async def verify_admin_token(x_admin_token: str = Header(...)):
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid admin token")


@router.get("/customers", response_model=list[CustomerResponse])
async def list_customers(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_token),
):
    result = await db.execute(select(Customer).order_by(Customer.created_at.desc()))
    return result.scalars().all()


@router.get("/usage", response_model=list[UsageResponse])
async def list_usage(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_token),
):
    result = await db.execute(select(Usage).order_by(Usage.month.desc()))
    return result.scalars().all()


@router.get(
    "/customers/{customer_id}/missed-calls",
    response_model=list[MissedCallResponse],
)
async def get_customer_missed_calls(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_token),
):
    result = await db.execute(
        select(MissedCall)
        .where(MissedCall.customer_id == customer_id)
        .order_by(MissedCall.called_at.desc())
    )
    return result.scalars().all()


@router.post("/customers/{customer_id}/numbers")
async def provision_number(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_token),
):
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.subscription_status != "active":
        raise HTTPException(
            status_code=400, detail="Customer must have active subscription"
        )

    number = await voxvaani_client.provision_number(customer.country)
    if not number:
        raise HTTPException(status_code=500, detail="Failed to provision number")

    customer.calloto_number = number
    await db.commit()
    await db.refresh(customer)

    return {"status": "ok", "number": number}


@router.post("/customers/{customer_id}/test")
async def send_test_text_back(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_admin_token),
):
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if not customer.calloto_number:
        raise HTTPException(status_code=400, detail="No Calloto number assigned")

    test_message = f"Hi! This is a test from {customer.name}. Calloto is working!"
    message = await send_text_back(
        db=db,
        customer_id=customer.id,
        missed_call_id=0,
        to_number=customer.phone,
        channel="whatsapp",
        body=test_message,
        from_number=customer.calloto_number,
    )

    return {"status": "ok", "message_id": message.id if message else None}
