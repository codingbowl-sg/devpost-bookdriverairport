from datetime import datetime, timezone
from uuid import uuid4

from supabase import Client, create_client

from .models import AnalysisResult, Booking, BookingStatus
from .settings import settings


class BookingRepository:
    """In-memory demo store; replace methods with Supabase queries when configured."""

    def __init__(self) -> None:
        self._bookings: dict[str, Booking] = {}
        self._client: Client | None = create_client(settings.supabase_url, settings.supabase_key) if settings.has_supabase else None

    def create_from_analysis(self, analysis: AnalysisResult) -> Booking:
        if self._client:
            payload = analysis.draft.model_dump()
            payload.update({"status": "pending_approval", "confidence": analysis.confidence, "dispatcher_summary": analysis.dispatcher_summary, "flight": analysis.flight.model_dump() if analysis.flight else None})
            result = self._client.table("bookings").insert(payload).execute()
            return Booking.model_validate(result.data[0])
        booking = Booking(id=str(uuid4()), status="pending_approval", created_at=datetime.now(timezone.utc), confidence=analysis.confidence, dispatcher_summary=analysis.dispatcher_summary, flight=analysis.flight, **analysis.draft.model_dump())
        self._bookings[booking.id] = booking
        return booking

    def list(self) -> list[Booking]:
        if self._client:
            result = self._client.table("bookings").select("*").order("created_at", desc=True).execute()
            return [Booking.model_validate(row) for row in result.data]
        return sorted(self._bookings.values(), key=lambda booking: booking.created_at, reverse=True)

    def set_status(self, booking_id: str, status: BookingStatus) -> Booking | None:
        if self._client:
            result = self._client.table("bookings").update({"status": status}).eq("id", booking_id).execute()
            return Booking.model_validate(result.data[0]) if result.data else None
        booking = self._bookings.get(booking_id)
        if booking:
            booking.status = status
        return booking


repository = BookingRepository()
