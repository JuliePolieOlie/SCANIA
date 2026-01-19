import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from src.config import DB_URL, DATA_PATH
from src.lineage import new_run_id, utc_now, file_hash

def upsert_raw_orders(cur, df: pd.DataFrame):
    rows = list(df[["order_id", "order_date", "qty", "plant"]].itertuples(index=False, name=None))
    sql = """
    insert into raw.orders(order_id, order_date, qty, plant)
    values 
    on conflict (order_id) do update
      set order_date = excluded.order_date,
          qty = excluded.qty,
          plant = excluded.plant
    """
    execute_values(cur, sql, rows)

def upsert_mart_kpi(cur, kpi: pd.DataFrame):
    rows = list(kpi[["kpi_date", "plant", "orders", "total_qty"]].itertuples(index=False, name=None))
    sql = """
    insert into mart.kpi_daily(kpi_date, plant, orders, total_qty)
    values 
    on conflict (kpi_date, plant) do update
      set orders = excluded.orders,
          total_qty = excluded.total_qty
    """
    execute_values(cur, sql, rows)

def main():
    run_id = new_run_id()
    started_at = utc_now()
    input_sha = file_hash(DATA_PATH)

    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        cur.execute(
            "insert into meta.runs(run_id, started_at, input_hash, status) values (,,,)",
            (run_id, started_at, input_sha, "RUNNING"),
        )

        df = pd.read_csv(DATA_PATH)
        df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
        df["qty"] = df["qty"].astype(int)
        df["plant"] = df["plant"].astype(str)

        upsert_raw_orders(cur, df)

        kpi = (
            df.groupby(["order_date", "plant"])
              .agg(orders=("order_id", "nunique"), total_qty=("qty", "sum"))
              .reset_index()
              .rename(columns={"order_date": "kpi_date"})
        )

        upsert_mart_kpi(cur, kpi)

        finished_at = utc_now()
        cur.execute(
            "update meta.runs set finished_at=, status=, rowcount_raw=, rowcount_mart= where run_id=",
            (finished_at, "SUCCEEDED", len(df), len(kpi), run_id),
        )

        conn.commit()
        print("ETL SUCCEEDED. run_id =", run_id)

    except Exception:
        conn.rollback()
        finished_at = utc_now()
        cur.execute(
            "update meta.runs set finished_at=, status= where run_id=",
            (finished_at, "FAILED", run_id),
        )
        conn.commit()
        raise

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
