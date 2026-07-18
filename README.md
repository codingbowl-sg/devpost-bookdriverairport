# DispatchAI

An AI Operations Agent that turns customer WhatsApp messages into validated, human-approved chauffeur booking drafts.

## Demo flow

1. Paste or use the pre-filled customer request in the WhatsApp intake.
2. Click **Analyze request** to extract booking fields, validate locations, look up the mock flight, and create a dispatcher handoff.
3. Create a pending booking, then approve or reject it in the dispatch console.

Both modes use the FastAPI API. Demo mode selects deterministic fixtures on the server; Live mode selects the OpenAI-powered extractor and production integrations. This keeps the frontend and backend behavior aligned.

## Run locally
Note: Run /api/health to check its health status.
It should show: {"status":"ok","modes":["demo","live"]}

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

```bash
# Copy the file
cp .env.example .env

# Create the virtual environment
python3 -m venv .venv
# Activate the virtual environment
source .venv/bin/activate
# Install dependencies
pip install -r backend/requirements.txt
# Run the application
uvicorn app.main:app --reload --app-dir backend
```

In a second terminal:

```powershell
npm install
npm run dev
```

Open `http://localhost:5173`.

## Architecture

- `src/presentation`: React UI components and view state.
- `src/domain`: shared frontend domain types.
- `src/data`: frontend HTTP client.
- `backend/app/main.py`: FastAPI routes and API contract.
- `backend/app/services.py`: AI orchestration and authoritative flight/address adapter seam.
- `backend/app/repository.py`: persistence abstraction; in-memory demo store today, Supabase replacement seam for deployment.
- `supabase/schema.sql`: production database schema for bookings and messages.

## Production integration notes

Set `OPENAI_API_KEY`, `ONEMAP_ACCESS_TOKEN`, and Supabase credentials in `.env`. OneMap Search API tokens expire after three days and should be stored server-side. Demo requests always use deterministic server-side fixtures and an in-memory booking store. Live requests require `OPENAI_API_KEY` and use the OpenAI Responses API with `OPENAI_MODEL`; when `SUPABASE_URL` and `SUPABASE_KEY` are configured, live bookings persist to Supabase. A Live request without an OpenAI key returns a clear 503 configuration error.

OneMap remains the source of truth for real address validation and a flight provider remains the source of truth for flight status. The reasoning model must not invent either data source.

For an existing Supabase project created from an earlier schema revision, run `supabase/migrations/20260714_add_booking_flight.sql` in the Supabase SQL Editor before enabling live persistence.

## API

- `POST /api/analyze` — accepts `{ "message": "..." }` and an `X-Dispatch-Mode: demo|live` header; returns extraction, validations, risks, summary, confidence.
- `GET /api/mock-flight/{flightNumber}` — mock authoritative flight lookup.
- `POST /api/bookings` — persists an analyzed booking and its customer message as `pending_approval`.
- `GET /api/bookings` — returns persisted bookings.
- `GET /api/messages` — returns all messages for the selected mode, newest first.
- `PATCH /api/bookings/{id}/status?status=approved` — dispatcher decision.
- `GET /api/bookings/{id}/messages` — returns the customer, agent, and dispatcher messages for a booking.
