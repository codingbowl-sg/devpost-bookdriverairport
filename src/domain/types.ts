export type BookingType = "airport_arrival" | "airport_departure" | "point_to_point" | "hourly_charter";

export interface FlightInfo { number: string; status: string; arrival_time: string; terminal: string; gate: string }
export interface BookingDraft { customer_name: string | null; booking_date: string | null; pickup_time: string | null; pickup: string | null; destination: string | null; flight_number: string | null; passengers: number | null; luggage: number | null; booking_type: BookingType }
export interface Analysis { draft: BookingDraft; address_validations: Record<string, boolean>; flight: FlightInfo | null; follow_up: string | null; warnings: string[]; dispatcher_summary: string; confidence: number }
export interface Booking extends BookingDraft { id: string; status: "pending_approval" | "approved" | "rejected"; confidence: number; dispatcher_summary: string; flight: FlightInfo | null; created_at: string }
