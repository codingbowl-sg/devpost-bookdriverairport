from datetime import datetime, timezone
from uuid import uuid4

from supabase import Client, create_client

from .models import AnalysisResult, Booking, BookingStatus, Message, MessageSender
from .settings import settings


class BookingRepository:
    """In-memory demo store; replace methods with Supabase queries when configured."""

    def __init__(self) -> None:
        self._bookings: dict[str, Booking] = {}
        self._messages: dict[str, list[Message]] = {}
        self._client: Client | None = create_client(settings.supabase_url, settings.supabase_key) if settings.has_supabase else None

    def create_from_analysis(self, analysis: AnalysisResult, customer_message: str, mode: str) -> Booking:
        if mode == "live" and self._client:
            payload = analysis.draft.model_dump()
            payload.update({"status": "pending_approval", "confidence": analysis.confidence, "dispatcher_summary": analysis.dispatcher_summary, "flight": analysis.flight.model_dump() if analysis.flight else None})
            result = self._client.table("bookings").insert(payload).execute()
            booking = Booking.model_validate(result.data[0])
        else:
            booking = Booking(id=str(uuid4()), status="pending_approval", created_at=datetime.now(timezone.utc), confidence=analysis.confidence, dispatcher_summary=analysis.dispatcher_summary, flight=analysis.flight, **analysis.draft.model_dump())
            self._bookings[booking.id] = booking
        self.add_message(booking.id, "customer", customer_message, mode)
        if analysis.follow_up:
            self.add_message(booking.id, "agent", analysis.follow_up, mode)
        return booking

    def list_bookings(self) -> list[Booking]:
        if self._client:
            result = self._client.table("bookings").select("*").order("created_at", desc=True).execute()
            return [Booking.model_validate(row) for row in result.data]
        return sorted(self._bookings.values(), key=lambda booking: booking.created_at, reverse=True)

    def set_status(self, booking_id: str, status: BookingStatus, mode: str) -> Booking | None:
        if mode == "live" and self._client:
            result = self._client.table("bookings").update({"status": status}).eq("id", booking_id).execute()
            booking = Booking.model_validate(result.data[0]) if result.data else None
        else:
            booking = self._bookings.get(booking_id)
            if booking:
                booking.status = status
        if booking:
            self.add_message(booking.id, "dispatcher", f"Booking {status.replace('_', ' ')}.", mode)
        return booking

    def add_message(self, booking_id: str, sender: MessageSender, content: str, mode: str) -> Message:
        if mode == "live" and self._client:
            result = self._client.table("messages").insert({"booking_id": booking_id, "sender": sender, "content": content}).execute()
            return Message.model_validate(result.data[0])
        message = Message(id=str(uuid4()), booking_id=booking_id, sender=sender, content=content, created_at=datetime.now(timezone.utc))
        self._messages.setdefault(booking_id, []).append(message)
        return message

    def list_messages(self, booking_id: str, mode: str) -> list[Message]:
        if mode == "live" and self._client:
            result = self._client.table("messages").select("*").eq("booking_id", booking_id).order("created_at").execute()
            return [Message.model_validate(row) for row in result.data]
        return self._messages.get(booking_id, [])

    def list_all_messages(self, mode: str) -> list[Message]:
        if mode == "live" and self._client:
            result = self._client.table("messages").select("*").order("created_at", desc=True).execute()
            return [Message.model_validate(row) for row in result.data]
        return sorted((message for messages in self._messages.values() for message in messages), key=lambda message: message.created_at, reverse=True)


repository = BookingRepository()
