from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Message, Usage
from app.services.telephony import voxvaani_client

MAX_FREE_MESSAGES = 100
OVERAGE_COST_PER_MESSAGE = 0.05


def render_message_template(
    template: str, business_name: str, price_range: str, booking_link: str
) -> str:
    return template.format(
        business_name=business_name,
        price_range=price_range,
        booking_link=booking_link,
    )


async def get_current_usage(db: AsyncSession, customer_id: int) -> Usage | None:
    current_month = datetime.now().strftime("%Y-%m")
    result = await db.execute(
        select(Usage).where(
            Usage.customer_id == customer_id,
            Usage.month == current_month,
        )
    )
    return result.scalar_one_or_none()


async def increment_usage(db: AsyncSession, customer_id: int) -> Usage:
    current_month = datetime.now().strftime("%Y-%m")
    usage = await get_current_usage(db, customer_id)

    if usage is None:
        usage = Usage(
            customer_id=customer_id,
            month=current_month,
            messages_sent=1,
            overage_units=0,
        )
        db.add(usage)
    else:
        usage.messages_sent += 1
        if usage.messages_sent > MAX_FREE_MESSAGES:
            usage.overage_units += 1

    await db.commit()
    await db.refresh(usage)
    return usage


async def send_text_back(
    db: AsyncSession,
    customer_id: int,
    missed_call_id: int,
    to_number: str,
    channel: str,
    body: str,
    from_number: str,
) -> Message | None:
    provider_msg_id = None

    if channel == "whatsapp":
        provider_msg_id = await voxvaani_client.send_whatsapp(
            to_number, body, from_number
        )
        if provider_msg_id is None:
            channel = "sms"
            provider_msg_id = await voxvaani_client.send_sms(
                to_number, body, from_number
            )
    else:
        provider_msg_id = await voxvaani_client.send_sms(
            to_number, body, from_number
        )

    message = Message(
        customer_id=customer_id,
        missed_call_id=missed_call_id,
        channel=channel,
        direction="out",
        body=body,
        provider_msg_id=provider_msg_id,
        status="sent" if provider_msg_id else "failed",
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    await increment_usage(db, customer_id)

    return message
