create schema if not exists raw;
create schema if not exists mart;
create schema if not exists meta;

create table if not exists raw.orders (
  order_id text primary key,
  order_date date not null,
  qty int not null,
  plant text not null
);

create table if not exists mart.kpi_daily (
  kpi_date date not null,
  plant text not null,
  orders int not null,
  total_qty int not null,
  primary key (kpi_date, plant)
);

create table if not exists meta.runs (
  run_id text primary key,
  started_at timestamptz not null,
  finished_at timestamptz,
  input_hash text,
  status text,
  rowcount_raw int,
  rowcount_mart int
);

create table if not exists meta.dq_results (
  run_id text not null,
  check_name text not null,
  passed boolean not null,
  details text,
  created_at timestamptz not null default now()
);
