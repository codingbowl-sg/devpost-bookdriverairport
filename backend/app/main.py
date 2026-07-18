from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import AnalyzeRequest, AnalysisResult, Booking, BookingStatus
from .repository import repository
from .services import MOCK_FLIGHTS, get_orchestrator

app = FastAPI(title="DispatchAI API", version="0.1.0", description="AI chauffeur booking operations API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "demo"}


@app.get("/api/mock-flight/{flight_number}")
def mock_flight(flight_number: str):
    flight = MOCK_FLIGHTS.get(flight_number.upper())
    if not flight:
        raise HTTPException(404, "Flight not found")
    return flight


@app.post("/api/analyze", response_model=AnalysisResult)
def analyze(request: AnalyzeRequest) -> AnalysisResult:
    return get_orchestrator().analyze(request.message)


@app.post("/api/bookings", response_model=Booking)
def create_booking(analysis: AnalysisResult) -> Booking:
    return repository.create_from_analysis(analysis)


@app.get("/api/bookings", response_model=list[Booking])
def list_bookings() -> list[Booking]:
    return repository.list()


@app.patch("/api/bookings/{booking_id}/status", response_model=Booking)
def update_booking_status(booking_id: str, status: BookingStatus) -> Booking:
    booking = repository.set_status(booking_id, status)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking
