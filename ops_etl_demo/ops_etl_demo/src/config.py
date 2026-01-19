import os

DB_URL = os.getenv("DB_URL", "postgresql://app:app@localhost:5433/ops")
DATA_PATH = os.getenv("DATA_PATH", "data/orders.csv")
