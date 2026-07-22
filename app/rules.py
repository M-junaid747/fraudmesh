from typing import Optional, Tuple
from app.config import AMOUNT_THRESHOLD


def evaluate_rules(amount: float, device_id: Optional[str]) -> Tuple[bool, Optional[str]]:
    """Rule-based fraud check. Returns (flagged, reason)."""
    if amount >= AMOUNT_THRESHOLD:
        return True, f"amount >= {AMOUNT_THRESHOLD}"
    if device_id and device_id.startswith("unknown"):
        return True, "unrecognized device"
    return False, None