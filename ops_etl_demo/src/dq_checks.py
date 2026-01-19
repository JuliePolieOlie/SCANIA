import json
import pandas as pd
import psycopg2

from src.config import DB_URL, DATA_PATH

REQUIRED_COLS = ["order_id", "order_date", "qty", "plant"]

def write_result(cur, run_id: str, check_name: str, passed: bool, details: dict):
    cur.execute(
        "insert into meta.dq_results(run_id, check_name, passed, details) values (,,,)",
        (run_id, check_name, passed, json.dumps(details)),
    )

def run_checks(run_id: str):
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        df = pd.read_csv(DATA_PATH)

        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        passed_schema = (len(missing) == 0)
        write_result(cur, run_id, "schema_required_columns", passed_schema, {"missing": missing})

        null_rates = {c: float(df[c].isna().mean()) for c in REQUIRED_COLS if c in df.columns}
        passed_complete = all(v <= 0.0 for v in null_rates.values())
        write_result(cur, run_id, "completeness_null_rate", passed_complete, {"null_rates": null_rates})

        cur.execute("select count(*) from raw.orders")
        raw_count = int(cur.fetchone()[0])
        file_count = int(len(df))
        passed_recon = (raw_count >= file_count)
        write_result(cur, run_id, "reconciliation_rowcount", passed_recon, {"file_rows": file_count, "raw_rows": raw_count})

        conn.commit()
        print("DQ checks recorded for run_id =", run_id)

    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
