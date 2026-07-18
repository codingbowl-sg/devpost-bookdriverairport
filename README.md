# DispatchAI

An AI Operations Agent that turns customer WhatsApp messages into validated, human-approved chauffeur booking drafts.

## Demo flow

1. Paste or use the pre-filled customer request in the WhatsApp intake.
2. Click **Analyze request** to extract booking fields, validate locations, look up the mock flight, and create a dispatcher handoff.
3. Create a pending booking, then approve or reject it in the dispatch console.

The default demo works without credentials using deterministic fixtures. This keeps the 2-minute demo reliable while preserving clean integration seams for production services.

## Run locally

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
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

Set `OPENAI_API_KEY`, `ONEMAP_ACCESS_TOKEN`, and Supabase credentials in `.env`. OneMap Search API tokens expire after three days and should be stored server-side. When `OPENAI_API_KEY` is configured, extraction uses the OpenAI Responses API with `OPENAI_MODEL`; when `SUPABASE_URL` and `SUPABASE_KEY` are configured, bookings persist to Supabase. The application falls back to its deterministic demo services only when a provider is not configured.

OneMap remains the source of truth for real address validation and a flight provider remains the source of truth for flight status. The reasoning model must not invent either data source.

For an existing Supabase project created from an earlier schema revision, run `supabase/migrations/20260714_add_booking_flight.sql` in the Supabase SQL Editor before enabling live persistence.

## API

- `POST /api/analyze` — accepts `{ "message": "..." }`, returns extraction, validations, risks, summary, confidence.
- `GET /api/mock-flight/{flightNumber}` — mock authoritative flight lookup.
- `POST /api/bookings` — persists an analyzed booking as `pending_approval`.
- `GET /api/bookings` — returns persisted bookings.
- `PATCH /api/bookings/{id}/status?status=approved` — dispatcher decision.
