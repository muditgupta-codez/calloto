from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    trade_vertical: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, default="GB")
    calloto_number: Mapped[str | None] = mapped_column(String)
    message_template: Mapped[str | None] = mapped_column(String)
    price_range: Mapped[str | None] = mapped_column(String)
    paddle_customer_id: Mapped[str | None] = mapped_column(String)
    subscription_status: Mapped[str] = mapped_column(String, default="inactive")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class MissedCall(Base):
    __tablename__ = "missed_calls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    caller_number: Mapped[str] = mapped_column(String, nullable=False)
    call_sid: Mapped[str | None] = mapped_column(String)
    called_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default="texted")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    missed_call_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("missed_calls.id")
    )
    channel: Mapped[str] = mapped_column(String, nullable=False)
    direction: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    provider_msg_id: Mapped[str | None] = mapped_column(String)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[str] = mapped_column(String, default="sent")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    missed_call_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("missed_calls.id")
    )
    cal_link: Mapped[str | None] = mapped_column(String)
    slot_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Usage(Base):
    __tablename__ = "usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    month: Mapped[str] = mapped_column(String, nullable=False)
    messages_sent: Mapped[int] = mapped_column(Integer, default=0)
    overage_units: Mapped[int] = mapped_column(Integer, default=0)
