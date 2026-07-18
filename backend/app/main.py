from typing import Literal

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import AnalyzeRequest, AnalysisResult, Booking, BookingStatus, CreateBookingRequest, Message
from .repository import repository
from .services import MOCK_FLIGHTS, get_orchestrator

app = FastAPI(title="DispatchAI API", version="0.1.0", description="AI chauffeur booking operations API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

DispatchMode = Literal["demo", "live"]


@app.get("/api/health")
def health() -> dict[str, object]:
    return {"status": "ok", "modes": ["demo", "live"]}


@app.get("/api/mock-flight/{flight_number}")
def mock_flight(flight_number: str):
    flight = MOCK_FLIGHTS.get(flight_number.upper())
    if not flight:
        raise HTTPException(404, "Flight not found")
    return flight


@app.post("/api/analyze", response_model=AnalysisResult)
def analyze(request: AnalyzeRequest, mode: DispatchMode = Header(default="demo", alias="X-Dispatch-Mode")) -> AnalysisResult:
    try:
        return get_orchestrator(mode).analyze(request.message)
    except RuntimeError as error:
        raise HTTPException(503, str(error)) from error


@app.post("/api/bookings", response_model=Booking)
def create_booking(request: CreateBookingRequest, mode: DispatchMode = Header(default="demo", alias="X-Dispatch-Mode")) -> Booking:
    return repository.create_from_analysis(request.analysis, request.customer_message, mode)


@app.get("/api/bookings", response_model=list[Booking])
def list_bookings() -> list[Booking]:
    return repository.list_bookings()


@app.get("/api/messages", response_model=list[Message])
def list_messages(mode: DispatchMode = Header(default="demo", alias="X-Dispatch-Mode")) -> list[Message]:
    return repository.list_all_messages(mode)


@app.patch("/api/bookings/{booking_id}/status", response_model=Booking)
def update_booking_status(booking_id: str, status: BookingStatus, mode: DispatchMode = Header(default="demo", alias="X-Dispatch-Mode")) -> Booking:
    booking = repository.set_status(booking_id, status, mode)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking


@app.get("/api/bookings/{booking_id}/messages", response_model=list[Message])
def list_booking_messages(booking_id: str, mode: DispatchMode = Header(default="demo", alias="X-Dispatch-Mode")) -> list[Message]:
    return repository.list_messages(booking_id, mode)
