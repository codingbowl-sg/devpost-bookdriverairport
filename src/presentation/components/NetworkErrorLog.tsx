import { useEffect, useState } from "react";
import { AlertTriangle, ChevronDown, Trash2 } from "lucide-react";
import { networkLog, type NetworkErrorEntry } from "../../data/networkLog";

export function NetworkErrorLog() {
  const [entries, setEntries] = useState<NetworkErrorEntry[]>(networkLog.getEntries);
  const [open, setOpen] = useState(false);

  useEffect(() => networkLog.subscribe(setEntries), []);
  useEffect(() => {
    if (entries.length) setOpen(true);
  }, [entries.length]);

  return <aside className={`network-log ${open ? "is-open" : ""}`} aria-live="polite">
    <div className="network-log-header">
      <button type="button" className="network-log-toggle" onClick={() => setOpen(!open)} aria-expanded={open}>
        <AlertTriangle size={15} /> Network errors <span className="network-log-count">{entries.length}</span><ChevronDown size={15} />
      </button>
      {entries.length > 0 && <button type="button" className="network-log-clear" onClick={() => networkLog.clear()} aria-label="Clear network errors"><Trash2 size={14} /> Clear</button>}
    </div>
    {open && <div className="network-log-body">{entries.length === 0 ? <p>No failed network requests yet.</p> : entries.map((entry) => <div className="network-log-entry" key={entry.id}><div><b>{entry.method} {entry.path}</b><span>{entry.time}{entry.status ? ` · HTTP ${entry.status}` : " · Network failure"}</span></div><p>{entry.message}</p></div>)}</div>}
  </aside>;
}
