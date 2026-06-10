from __future__ import annotations
import hashlib, json, time

def stable_digest(value: object, length: int = 16) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:length]

def stable_id(prefix: str, value: object, length: int = 12) -> str:
    return f"{prefix}-{stable_digest(value, length)}"

def utc_stamp() -> str:
    # deterministic enough for receipts while avoiding timezone dependency
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
