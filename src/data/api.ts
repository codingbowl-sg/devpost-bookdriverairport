import type { Analysis, Booking } from "../domain/types";

const baseUrl = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, { headers: { "Content-Type": "application/json", ...init?.headers }, ...init });
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail ?? "Something went wrong. Please retry.");
  return response.json() as Promise<T>;
}

export const operationsApi = {
  analyze: (message: string) => request<Analysis>("/api/analyze", { method: "POST", body: JSON.stringify({ message }) }),
  createBooking: (analysis: Analysis) => request<Booking>("/api/bookings", { method: "POST", body: JSON.stringify(analysis) }),
  setStatus: (id: string, status: Booking["status"]) => request<Booking>(`/api/bookings/${id}/status?status=${status}`, { method: "PATCH" }),
};
