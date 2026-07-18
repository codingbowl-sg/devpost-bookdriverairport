import type { Analysis } from "../../domain/types";
import { SignalPill } from "./SignalPill";

const display = (value: string | number | null) => value ?? "Not captured";

export function BookingDetails({ analysis }: { analysis: Analysis }) {
  const { draft, address_validations, flight } = analysis;
  return <div className="detail-stack">
    <section className="card detail-card">
      <div className="section-kicker">AI BOOKING DRAFT</div>
      <div className="type-row"><strong>{draft.booking_type.replace(/_/g, " ")}</strong><SignalPill label={`${analysis.confidence}% confidence`} tone={analysis.confidence > 80 ? "success" : "warning"} /></div>
      <dl className="details-grid">
        <div><dt>Customer</dt><dd>{display(draft.customer_name)}</dd></div><div><dt>When</dt><dd>{display(draft.booking_date)} · {display(draft.pickup_time)}</dd></div>
        <div><dt>Pickup</dt><dd>{display(draft.pickup)} {draft.pickup && <small className={address_validations.pickup ? "verified" : "unverified"}>{address_validations.pickup ? "✓ verified" : "Needs review"}</small>}</dd></div>
        <div><dt>Destination</dt><dd>{display(draft.destination)} {draft.destination && <small className={address_validations.destination ? "verified" : "unverified"}>{address_validations.destination ? "✓ verified" : "Needs review"}</small>}</dd></div>
        <div><dt>Guests</dt><dd>{display(draft.passengers)} passengers · {display(draft.luggage)} luggage</dd></div><div><dt>Flight</dt><dd>{display(draft.flight_number)}</dd></div>
      </dl>
    </section>
    {flight && <section className="card flight-card"><div><span className="section-kicker">LIVE FLIGHT SIGNAL</span><h3>{flight.number} · {flight.status}</h3></div><div className="flight-meta"><span>ARRIVES <b>{flight.arrival_time}</b></span><span>TERMINAL <b>{flight.terminal}</b></span><span>GATE <b>{flight.gate}</b></span></div></section>}
    {analysis.warnings.length > 0 && <section className="warning-card"><b>Dispatcher attention</b>{analysis.warnings.map((warning) => <p key={warning}>{warning}</p>)}</section>}
  </div>;
}
