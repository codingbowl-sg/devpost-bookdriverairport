import type { Analysis, Booking } from "../domain/types";
import { networkLog } from "./networkLog";

const baseUrl = import.meta.env.VITE_API_URL ?? "";
export type DispatchMode = "demo" | "live";

function describeApiError(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map(describeApiError).filter(Boolean).join("; ") || "Request validation failed.";
  if (detail && typeof detail === "object") {
    const value = detail as { msg?: unknown; detail?: unknown };
    if (typeof value.msg === "string") return value.msg;
    if (value.detail !== undefined) return describeApiError(value.detail);
  }
  return "Something went wrong. Please retry.";
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const method = init?.method ?? "GET";
  try {
    const response = await fetch(`${baseUrl}${path}`, { ...init, headers: { "Content-Type": "application/json", ...init?.headers } });
    if (!response.ok) {
      const payload: unknown = await response.json().catch(() => null);
      const message = describeApiError(payload && typeof payload === "object" && "detail" in payload ? payload.detail : payload);
      networkLog.add({ method, path, status: response.status, message });
      throw new Error(message);
    }
    return response.json() as Promise<T>;
  } catch (caught) {
    if (caught instanceof TypeError) networkLog.add({ method, path, message: caught.message || "Unable to reach the server." });
    throw caught;
  }
}

export const operationsApi = {
  analyze: (message: string, mode: DispatchMode) => request<Analysis>("/api/analyze", { method: "POST", headers: { "X-Dispatch-Mode": mode }, body: JSON.stringify({ message }) }),
  createBooking: (analysis: Analysis, customerMessage: string, mode: DispatchMode) => request<Booking>("/api/bookings", { method: "POST", headers: { "X-Dispatch-Mode": mode }, body: JSON.stringify({ analysis, customer_message: customerMessage }) }),
  setStatus: (id: string, status: Booking["status"], mode: DispatchMode) => request<Booking>(`/api/bookings/${id}/status?status=${status}`, { method: "PATCH", headers: { "X-Dispatch-Mode": mode } }),
};
