from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


BookingType = Literal["airport_arrival", "airport_departure", "point_to_point", "hourly_charter"]
BookingStatus = Literal["pending_approval", "approved", "rejected"]
MessageSender = Literal["customer", "agent", "dispatcher"]


class AnalyzeRequest(BaseModel):
    message: str = Field(min_length=8, max_length=2000)


class FlightInfo(BaseModel):
    number: str
    status: str
    arrival_time: str
    terminal: str
    gate: str


class BookingDraft(BaseModel):
    customer_name: str | None = None
    booking_date: str | None = None
    pickup_time: str | None = None
    pickup: str | None = None
    destination: str | None = None
    flight_number: str | None = None
    passengers: int | None = None
    luggage: int | None = None
    booking_type: BookingType = "point_to_point"


class AnalysisResult(BaseModel):
    draft: BookingDraft
    address_validations: dict[str, bool]
    flight: FlightInfo | None = None
    follow_up: str | None = None
    warnings: list[str] = []
    dispatcher_summary: str
    confidence: int = Field(ge=0, le=100)


class CreateBookingRequest(BaseModel):
    analysis: AnalysisResult
    customer_message: str = Field(min_length=1, max_length=2000)


class Booking(BookingDraft):
    id: str
    status: BookingStatus
    created_at: datetime
    confidence: int
    dispatcher_summary: str
    flight: FlightInfo | None = None


class Message(BaseModel):
    id: str
    booking_id: str
    sender: MessageSender
    content: str
    created_at: datetime
