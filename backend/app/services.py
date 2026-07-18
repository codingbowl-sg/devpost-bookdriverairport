import re
import json

import httpx
from openai import OpenAI

from .models import AnalysisResult, BookingDraft, FlightInfo
from .settings import settings


KNOWN_LOCATIONS = {
    "changi airport": "Singapore Changi Airport",
    "marina bay sands": "Marina Bay Sands, 10 Bayfront Avenue",
    "raffles hotel": "Raffles Hotel Singapore, 1 Beach Road",
    "orchard road": "Orchard Road, Singapore",
    "sentosa": "Sentosa, Singapore",
}

MOCK_FLIGHTS = {
    "SQ231": FlightInfo(number="SQ231", status="Landed", arrival_time="18:35", terminal="T3", gate="B5"),
    "BA15": FlightInfo(number="BA15", status="On time", arrival_time="17:55", terminal="T1", gate="D42"),
}


def normalize_location(value: str | None) -> tuple[str | None, bool]:
    if not value:
        return None, False
    canonical = KNOWN_LOCATIONS.get(value.strip().lower())
    return canonical or value.strip(), bool(canonical or len(value.strip()) > 8)


class MockFlightService:
    def get(self, flight_number: str | None) -> FlightInfo | None:
        if not flight_number:
            return None
        return MOCK_FLIGHTS.get(flight_number.upper())


class OneMapAddressService:
    """Uses OneMap as the authority whenever an access token is configured."""

    endpoint = "https://www.onemap.gov.sg/api/common/elastic/search"

    def validate(self, value: str | None) -> tuple[str | None, bool, str | None]:
        if not value:
            return None, False, None
        if not settings.has_onemap:
            normalized, valid = normalize_location(value)
            print(f"Validating address '{value}' without OneMap (normalized to '{normalized}')...")
            return normalized, valid, None
        try:
            response = httpx.get(
                self.endpoint,
                params={"searchVal": value, "returnGeom": "N", "getAddrDetails": "Y", "pageNum": 1},
                headers={"Authorization": settings.onemap_access_token},
                timeout=8.0,
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            if not results:
                return value, False, f"OneMap could not validate '{value}'."
            address = results[0].get("ADDRESS") or results[0].get("SEARCHVAL") or value
            print(f"Validating address '{value}' with OneMap...")
        
            return address.title(), True, None
        except httpx.HTTPError:
            return value, False, "OneMap validation is temporarily unavailable."


def build_analysis(draft: BookingDraft, address_service: OneMapAddressService) -> AnalysisResult:
    pickup, pickup_valid, pickup_warning = address_service.validate(draft.pickup)
    destination, destination_valid, destination_warning = address_service.validate(draft.destination)
    draft = draft.model_copy(update={"pickup": pickup, "destination": destination})
    flight = MockFlightService().get(draft.flight_number)
    missing = [label for label, value in (("pickup time", draft.pickup_time), ("destination", draft.destination), ("passenger count", draft.passengers)) if value is None]
    warnings = [warning for warning in (pickup_warning, destination_warning) if warning]
    if draft.flight_number and not flight:
        warnings.append(f"Flight {draft.flight_number} could not be confirmed by the flight service.")
    if draft.passengers and draft.passengers > 6:
        warnings.append("Large party: dispatcher should confirm vehicle allocation.")
    confidence = max(42, 96 - len(missing) * 15 - len(warnings) * 8)
    follow_up = f"Could you please confirm the {missing[0]}?" if missing else None
    flight_line = f" Flight {flight.number} is {flight.status}, terminal {flight.terminal}, gate {flight.gate}." if flight else ""
    summary = f"{draft.booking_type.replace('_', ' ').title()} for {draft.customer_name or 'customer'} from {draft.pickup or 'TBC'} to {draft.destination or 'TBC'} on {draft.booking_date or 'date TBC'}, {draft.pickup_time or 'time TBC'}.{flight_line}"
    return AnalysisResult(draft=draft, address_validations={"pickup": pickup_valid, "destination": destination_valid}, flight=flight, follow_up=follow_up, warnings=warnings, dispatcher_summary=summary, confidence=confidence)


class RuleBasedOrchestrator:
    """Offline demo fallback. Swap with OpenAI structured output in production."""

    def analyze(self, message: str) -> AnalysisResult:
        lowered = message.lower()
        flight_match = re.search(r"\b([A-Z]{2}\s?\d{1,4})\b", message, re.I)
        flight_number = flight_match.group(1).replace(" ", "").upper() if flight_match else None
        passenger_match = re.search(r"(\d+)\s*(?:pax|passengers?|people)", lowered)
        luggage_match = re.search(r"(\d+)\s*(?:bags?|luggage|suitcases?)", lowered)
        time_match = re.search(r"\b(?:at\s*)?(\d{1,2}(?::\d{2})?\s?(?:am|pm))\b", lowered)
        date_match = re.search(r"\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*)\b", lowered)
        name_match = re.search(r"(?:i(?:'m| am)|this is|name is)\s+([A-Z][a-z]+)", message)

        pickup = "Singapore Changi Airport" if "changi" in lowered else "Marina Bay Sands" if "marina" in lowered else None
        destination = "Raffles Hotel" if "raffles" in lowered else "Orchard Road" if "orchard" in lowered else "Sentosa" if "sentosa" in lowered else None
        booking_type = "airport_arrival" if flight_number or "land" in lowered or "arrival" in lowered else "airport_departure" if "airport" in lowered else "point_to_point"
        draft = BookingDraft(
            customer_name=name_match.group(1) if name_match else None,
            booking_date=date_match.group(1).title() if date_match else None,
            pickup_time=time_match.group(1).upper() if time_match else None,
            pickup=pickup,
            destination=destination,
            flight_number=flight_number,
            passengers=int(passenger_match.group(1)) if passenger_match else None,
            luggage=int(luggage_match.group(1)) if luggage_match else None,
            booking_type=booking_type,
        )
        return build_analysis(draft, OneMapAddressService())


class OpenAIOrchestrator:
    """Extracts booking fields only; address and flight facts remain external authorities."""

    instructions = """Extract a chauffeur booking from the customer message into JSON.
Return only these keys: customer_name, booking_date, pickup_time, pickup, destination,
flight_number, passengers, luggage, booking_type. Use null for unknown values. Booking type
must be one of airport_arrival, airport_departure, point_to_point, hourly_charter. Do not
invent addresses, flight status, terminals, gates, dates, or missing facts."""

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def analyze(self, message: str) -> AnalysisResult:
        # Force the word 'json' into the user message/input string
        message = message + " Respond strictly with a json object."

        response = self.client.responses.create(
            model=settings.openai_model,
            instructions=self.instructions,
            input=message,
            text={"format": {"type": "json_object"}},
        )
        draft = BookingDraft.model_validate(json.loads(response.output_text))
        print(f"OpenAI extracted draft: {draft.json()}")
        return build_analysis(draft, OneMapAddressService())


def get_orchestrator(mode: str) -> OpenAIOrchestrator | RuleBasedOrchestrator:
    if mode == "demo":
        return RuleBasedOrchestrator()
    if not settings.has_openai:
        raise RuntimeError("Live mode requires OPENAI_API_KEY to be configured on the FastAPI server.")
    return OpenAIOrchestrator()
