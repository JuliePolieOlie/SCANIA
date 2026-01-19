Minimal production-style ETL demo: raw -> mart, with run traceability and data quality checks.

## What this repo demonstrates
- ETL/ELT pattern: load CSV -> upsert into raw -> build mart KPI table
- Traceability: each run has a run_id, input hash, row counts, status (meta.runs)
- Data Quality checks: schema/completeness/reconciliation results recorded (meta.dq_results)
- CI: GitHub Actions starts Postgres service and runs tests

## Architecture
Postgres schemas:
- raw: raw.orders
- mart: mart.kpi_daily
- meta: meta.runs, meta.dq_results

[200~cd ..
git add ops_etl_demo
git commit -m "Add reproducible Python+Postgres ETL demo (ops_etl_demo)"
git push~
