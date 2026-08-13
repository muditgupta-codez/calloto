from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Customer, MissedCall
from app.services.messaging import render_message_template, send_text_back

router = APIRouter()


@router.post("/api/webhook/call")
async def call_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    caller_number = form.get("From") or form.get("caller_number")
    called_number = form.get("To") or form.get("called_number")
    call_id = form.get("CallSid") or form.get("call_id")

    if not caller_number:
        raise HTTPException(status_code=400, detail="Missing caller number")

    if caller_number.lower() == "withheld" or caller_number.startswith("anonymous"):
        result = await db.execute(
            select(Customer).where(Customer.calloto_number == called_number)
        )
        customer = result.scalar_one_or_none()
        if customer:
            missed_call = MissedCall(
                customer_id=customer.id,
                caller_number="withheld",
                call_sid=call_id,
                called_at=datetime.utcnow(),
                status="withheld",
            )
            db.add(missed_call)
            await db.commit()
        return {"status": "withheld"}

    result = await db.execute(
        select(Customer).where(Customer.calloto_number == called_number)
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=404, detail="Customer not found for this number"
        )

    if customer.subscription_status != "active":
        return {"status": "inactive_customer"}

    missed_call = MissedCall(
        customer_id=customer.id,
        caller_number=caller_number,
        call_sid=call_id,
        called_at=datetime.utcnow(),
        status="texted",
    )
    db.add(missed_call)
    await db.commit()
    await db.refresh(missed_call)

    if customer.message_template and customer.calloto_number:
        booking_link = f"https://caloto.com/book/{customer.id}"
        body = render_message_template(
            customer.message_template,
            customer.name,
            customer.price_range or "",
            booking_link,
        )
        await send_text_back(
            db,
            customer.id,
            missed_call.id,
            caller_number,
            "whatsapp",
            body,
            customer.calloto_number,
        )

    return {"status": "ok", "missed_call_id": missed_call.id}


@router.post("/api/webhook/message")
async def message_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    await request.form()
    return {"status": "ok"}
