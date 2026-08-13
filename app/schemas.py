from datetime import datetime

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    email: str
    name: str
    phone: str
    trade_vertical: str


class CustomerResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    trade_vertical: str
    country: str
    calloto_number: str | None
    message_template: str | None
    price_range: str | None
    subscription_status: str
    trial_ends_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MissedCallResponse(BaseModel):
    id: int
    customer_id: int
    caller_number: str
    called_at: datetime
    duration: int
    status: str

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: int
    customer_id: int
    missed_call_id: int | None
    channel: str
    direction: str
    body: str
    sent_at: datetime
    status: str

    model_config = {"from_attributes": True}


class BookingCreate(BaseModel):
    customer_id: int
    name: str
    phone: str
    date: str
    time: str


class BookingResponse(BaseModel):
    id: int
    customer_id: int
    missed_call_id: int | None
    cal_link: str | None
    slot_time: datetime
    source: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UsageResponse(BaseModel):
    id: int
    customer_id: int
    month: str
    messages_sent: int
    overage_units: int

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    customer: CustomerResponse
    missed_calls: list[MissedCallResponse]
    messages: list[MessageResponse]
    bookings: list[BookingResponse]
    usage: UsageResponse | None


class HealthResponse(BaseModel):
    status: str
    database: str
    voxvaani: str
