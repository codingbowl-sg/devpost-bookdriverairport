export function SignalPill({ label, tone = "neutral" }: { label: string; tone?: "success" | "warning" | "neutral" }) {
  return <span className={`signal signal-${tone}`}><i />{label}</span>;
}
