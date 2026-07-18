create type booking_status as enum ('pending_approval', 'approved', 'rejected');

create table bookings (
  id uuid primary key default gen_random_uuid(),
  customer_name text,
  booking_date text,
  pickup_time text,
  pickup text,
  destination text,
  flight_number text,
  passengers integer,
  luggage integer,
  booking_type text not null,
  status booking_status not null default 'pending_approval',
  confidence integer not null,
  dispatcher_summary text not null,
  flight jsonb,
  created_at timestamptz not null default now()
);

create table messages (
  id uuid primary key default gen_random_uuid(),
  booking_id uuid references bookings(id) on delete cascade,
  sender text not null check (sender in ('customer', 'agent', 'dispatcher')),
  content text not null,
  created_at timestamptz not null default now()
);
