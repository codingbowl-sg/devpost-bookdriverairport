export interface NetworkErrorEntry {
  id: number;
  time: string;
  method: string;
  path: string;
  message: string;
  status?: number;
}

let entries: NetworkErrorEntry[] = [];
const listeners = new Set<(entries: NetworkErrorEntry[]) => void>();

function notify() {
  const snapshot = [...entries];
  listeners.forEach((listener) => listener(snapshot));
}

export const networkLog = {
  getEntries: () => entries,
  subscribe(listener: (nextEntries: NetworkErrorEntry[]) => void) {
    listeners.add(listener);
    return () => { listeners.delete(listener); };
  },
  add(entry: Omit<NetworkErrorEntry, "id" | "time">) {
    entries = [{ ...entry, id: Date.now(), time: new Date().toLocaleTimeString() }, ...entries].slice(0, 10);
    notify();
  },
  clear() {
    entries = [];
    notify();
  },
};
