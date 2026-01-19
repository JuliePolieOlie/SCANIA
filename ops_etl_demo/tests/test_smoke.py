import os
import psycopg2

DB_URL = os.getenv("DB_URL", "postgresql://app:app@localhost:5433/ops")

def test_db_connects():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("select 1;")
    assert cur.fetchone()[0] == 1
    cur.close()
    conn.close()
