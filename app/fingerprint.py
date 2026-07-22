import hashlib


def make_fingerprint(name: str, dob: str, account_last4: str) -> str:
    """One-way hash of identity fields. Irreversible — the raw fields
    never leave this function, only the resulting hash does."""
    raw = f"{name.strip().lower()}|{dob.strip()}|{account_last4.strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()