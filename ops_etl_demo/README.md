# ops_etl_demo (Python + Postgres)

Minimal production-style ETL demo: raw -> mart, with run traceability and data quality checks.

## What this repo demonstrates
- ETL/ELT: load CSV -> upsert into raw -> build mart KPI table
- Traceability: run_id, input hash, row counts, status (meta.runs)
- Data Quality: schema/completeness/reconciliation checks recorded (meta.dq_results)
- CI: GitHub Actions starts Postgres service and runs tests

## Quickstart (local)

### 1) Start Postgres
```bash
docker compose up -d
docker compose exec -T postgres psql -U app -d ops < sql/00_init.sql
```

### 2) Install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Run ETL
```bash
python -m src.run_etl
```

### 4) Run Data Quality checks
Replace RUN_ID with printed id:
```bash
python -c "from src.dq_checks import run_checks; run_checks('RUN_ID')"
```

## Verify results
```bash
docker compose exec -T postgres psql -U app -d ops -c "select * from mart.kpi_daily order by kpi_date, plant;"
docker compose exec -T postgres psql -U app -d ops -c "select * from meta.runs order by started_at desc limit 5;"
docker compose exec -T postgres psql -U app -d ops -c "select run_id, check_name, passed from meta.dq_results order by created_at desc limit 20;"
```

