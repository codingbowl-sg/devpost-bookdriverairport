# DispatchAI demo fallback package

The completed video is [`dispatchai-demo.mp4`](dispatchai-demo.mp4): a 1920 × 1080 H.264 MP4, 2 minutes 55 seconds long, with the timed captions rendered into the picture. The local application was started successfully; this environment's Chromium package is a non-runnable snap stub, so the video is assembled from the clean workflow captures rather than a browser-screen recording.

- `captures/` contains a named screenshot for every planned demo beat used in the video.
- `narration.md` is a 2:55 spoken walkthrough, with natural pauses after each action.
- `captions.ass` contains the exact one-sentence captions, timed for three seconds each and styled for a 1920 x 1080 export with a semi-transparent background.

The existing clean project captures are used as the source material. Several files intentionally reference the same UI state where a single screen makes multiple adjacent points—for example, the pending-approval screen is both the dispatcher review and approval handoff.

Demo Mode QA was executed locally after the reliability adjustment: deterministic extraction, fixture address validation, draft creation, and human approval all passed. The frontend production build also passed.

Live-mode captures document the configured OpenAI, OneMap, and Supabase path. The isolated recording environment cannot reach external services, so Live requests were not executed here; no credentials or terminal output are included in the capture set.

## Capture order

| Time | Screenshot | On-screen caption |
| --- | --- | --- |
| 00:00 | `captures/demo-01-open.png` | DispatchAI – AI Operations Agent for Chauffeur Booking |
| 00:08 | `captures/demo-02-demo-mode.png` | Demo Mode – Deterministic AI workflow for reliable demonstrations |
| 00:16 | `captures/demo-03-customer-request.png` | Customer submits a booking request |
| 00:28 | `captures/demo-04-analyze.png` | AI analyzes the natural-language message |
| 00:38 | `captures/demo-05-structured-details.png` | AI extracts structured booking information |
| 00:48 | `captures/demo-06-address-validation.png` | Address validation using demo data |
| 00:58 | `captures/demo-07-booking-draft.png` | Booking draft created |
| 01:08 | `captures/demo-08-dispatcher-dashboard.png` | Dispatcher reviews the booking |
| 01:17 | `captures/demo-09-pending-approval.png` | Status: Pending Approval |
| 01:27 | `captures/demo-10-human-approval.png` | Human approval completes the booking |
| 01:35 | `captures/live-01-live-mode.png` | Live Mode – OpenAI, OneMap, and Supabase |
| 01:45 | `captures/live-02-real-request.png` | Processing a real booking request |
| 01:55 | `captures/live-03-gpt-extraction.png` | GPT-5.6 extracts booking details |
| 02:05 | `captures/live-04-onemap-validation.png` | OneMap validates Singapore addresses |
| 02:15 | `captures/live-05-supabase-saved.png` | Booking saved to Supabase |
| 02:25 | `captures/live-06-dispatcher-dashboard.png` | Dispatcher reviews the live booking |
| 02:36 | `captures/live-07-human-approval.png` | Booking approved and ready for operations |
| 02:47 | `captures/closing-completed-dashboard.png` | DispatchAI combines AI reasoning with trusted external services while keeping humans in control. |
