import hashlib
import uuid
from datetime import datetime, timezone

def new_run_id() -> str:
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()
