import { useState } from "react";
import { Bot, ChevronRight, MessageCircle, ShieldCheck, Sparkles } from "lucide-react";
import type { Analysis, Booking } from "../domain/types";
import { operationsApi } from "../data/api";
import { BookingDetails } from "./components/BookingDetails";
import { Button } from "./components/Button";
import { DispatcherPanel } from "./components/DispatcherPanel";

const demoRequest = "Hi, I'm Sarah. My flight SQ231 lands at Changi tomorrow at 6:35pm. Please pick up 3 passengers with 4 bags and take us to Raffles Hotel at 7:15pm.";

export function App() {
  const [message, setMessage] = useState(demoRequest);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [booking, setBooking] = useState<Booking | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function analyze() { setLoading(true); setError(null); setBooking(null); try { setAnalysis(await operationsApi.analyze(message)); } catch (caught) { setError(caught instanceof Error ? caught.message : "Unable to analyze this request."); } finally { setLoading(false); } }
  async function createBooking() { if (!analysis) return; setLoading(true); setError(null); try { setBooking(await operationsApi.createBooking(analysis)); } catch (caught) { setError(caught instanceof Error ? caught.message : "Unable to create booking."); } finally { setLoading(false); } }
  async function setStatus(status: Booking["status"]) { if (!booking) return; setLoading(true); try { setBooking(await operationsApi.setStatus(booking.id, status)); } catch (caught) { setError(caught instanceof Error ? caught.message : "Unable to update booking."); } finally { setLoading(false); } }

  return <main><nav><div className="brand"><span className="brand-mark"><Sparkles size={18} /></span><span>Dispatch<span>AI</span></span></div><div className="nav-status"><ShieldCheck size={16} /> Human-in-the-loop operations</div></nav>
    <section className="hero"><div><p className="eyebrow">AI OPERATIONS AGENT</p><h1>From WhatsApp message<br /><em>to dispatch-ready.</em></h1><p className="hero-copy">DispatchAI turns a messy customer request into a validated chauffeur booking in seconds, with a human always in control.</p></div><div className="workflow"><div><b>01</b> Understand <ChevronRight size={15} /></div><div><b>02</b> Validate <ChevronRight size={15} /></div><div><b>03</b> Approve</div></div></section>
    <section className="workspace"><div className="conversation"><div className="section-heading"><div><span className="eyebrow">CUSTOMER CHANNEL</span><h2><MessageCircle size={20} /> WhatsApp intake</h2></div><span className="demo-chip">Demo mode</span></div><div className="chat-window"><div className="chat-header"><span className="avatar">S</span><div><b>Sarah Lim</b><small>Customer · WhatsApp</small></div><span className="online">● online</span></div><div className="bubble incoming">{message || "Your customer message will appear here."}<small>18:02</small></div><div className="typing-hint"><Bot size={15} /> AI extracts only the fields dispatch needs.</div></div><textarea value={message} onChange={(event) => setMessage(event.target.value)} aria-label="Customer booking message" /><div className="composer-actions"><span>Try the pre-filled airport arrival request</span><Button onClick={analyze} disabled={loading || message.trim().length < 8} className="analyze-button"><Sparkles size={16} />{loading ? "Analyzing…" : "Analyze request"}</Button></div>{error && <div className="error-message">{error}</div>}</div>
      <div className="results">{analysis ? <><BookingDetails analysis={analysis} /><DispatcherPanel analysis={analysis} booking={booking} onCreate={createBooking} onStatus={setStatus} loading={loading} /></> : <div className="empty-state"><div className="empty-icon"><Sparkles /></div><h2>Awaiting a customer request</h2><p>Run the sample conversation to see AI extraction, address validation, flight intelligence, and dispatcher approval in one flow.</p></div>}</div></section>
  </main>;
}
