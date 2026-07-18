import type { Analysis, Booking } from "../../domain/types";
import { Button } from "./Button";

export function DispatcherPanel({ analysis, booking, onCreate, onStatus, loading, mode }: { analysis: Analysis; booking: Booking | null; onCreate: () => void; onStatus: (status: Booking["status"]) => void; loading: boolean; mode: "demo" | "live" }) {
  return <aside className="dispatcher-panel">
    <div className="panel-top"><div><span className="eyebrow">DISPATCH CONSOLE</span><h2>Ready for a decision</h2></div><span className="mode-chip compact"><i aria-hidden="true" />{mode === "live" ? "Live" : "Demo"}</span></div>
    <div className="summary-box"><span>AI HANDOFF</span><p>{analysis.dispatcher_summary}</p></div>
    {analysis.follow_up && <div className="followup"><span>Suggested reply</span><p>“{analysis.follow_up}”</p></div>}
    {!booking ? <Button onClick={onCreate} disabled={loading} className="primary-action">{loading ? "Creating draft…" : "Create pending booking"}</Button> : <div className="approval-state"><p>Booking is <b>{booking.status.replace(/_/g, " ")}</b></p>{booking.status === "pending_approval" && <div className="actions"><Button onClick={() => onStatus("approved")} disabled={loading} className="approve">Approve & assign</Button><Button onClick={() => onStatus("rejected")} disabled={loading} className="reject">Reject</Button></div>}</div>}
    <p className="panel-footnote">Human approval required before a chauffeur is assigned.</p>
  </aside>;
}
