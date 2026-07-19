# DispatchAI demo narration

**Target duration: 2 minutes 55 seconds.** Move the pointer naturally, pause briefly after each click, and show each caption for three seconds at the matching timestamp in `captions.ass`.

## Demo Mode — 0:00–1:34

**0:00** — "DispatchAI is an AI operations agent for chauffeur booking. It turns an unstructured customer message into a reviewable booking draft while keeping a human dispatcher in control."

**0:08** — "I’m switching to Demo Mode. This uses a deterministic workflow, so the demonstration stays reliable without depending on external services."

**0:16** — "Here is a clean airport-arrival request from Sarah, including the flight, passengers, luggage, pickup, destination, and timing."

**0:28** — "I select Analyze request. The AI reads the natural-language message and prepares the operational fields dispatch needs."

**0:38** — "The resulting draft presents the booking type, customer details, flight, passenger count, luggage, pickup, and destination in a structured format."

**0:48** — "Demo fixtures validate and normalize both Singapore addresses, while the flight signal adds operational context for the dispatcher."

**0:58** — "I create the pending booking draft. At this point, the AI has prepared the work, but no chauffeur has been assigned."

**1:08** — "The dispatcher console is the review point: it summarizes the handoff and clearly separates AI assistance from the human decision."

**1:17** — "The booking is visibly marked Pending Approval, making the operational state clear before any downstream action."

**1:27** — "The dispatcher approves and assigns the booking. Human approval is the final control that completes the Demo Mode workflow."

## Live Mode — 1:35–2:46

**1:35** — "Now I switch to Live Mode, which connects the workflow to OpenAI, OneMap, and Supabase."

**1:45** — "I process the same clean customer request through the live operations path."

**1:55** — "GPT-5.6 extracts the booking details from the message while leaving factual validation to trusted systems."

**2:05** — "OneMap validates the Singapore pickup and destination addresses, returning normalized operational locations."

**2:15** — "Creating the booking saves the live draft to Supabase so it can be retained and reviewed by operations."

**2:25** — "The live Dispatcher Dashboard brings the validated data, flight signal, and approval controls together in one review surface."

**2:36** — "The dispatcher approves the booking, making it ready for operations while preserving a clear human decision point."

## Closing — 2:47–2:55

**2:47** — "DispatchAI combines AI reasoning with trusted external services while keeping humans in control."
