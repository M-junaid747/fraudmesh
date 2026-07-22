from datetime import datetime, timedelta
from app.database import get_shared_session
from app.models import WatchlistEntry, Alert

# Independent flags on the same fingerprint within this window count as a reactive match
REACTIVE_WINDOW = timedelta(hours=24)


def process_fingerprint(fingerprint: str, bank_id: str) -> dict:
    """
    Called whenever a bank flags a transaction and produces a fingerprint.

    - Proactive match: fingerprint already exists from a DIFFERENT bank
      -> the fraudster is caught instantly on this new attempt.
    - Reactive match: fingerprint flagged multiple times close together
      -> a pattern consistent with a coordinated fraud ring.

    Always records/updates the fingerprint on the shared watchlist.
    """
    session = get_shared_session()
    result = {"alert": False, "type": None}

    entry = session.query(WatchlistEntry).filter_by(fingerprint=fingerprint).first()

    if entry is None:
        session.add(WatchlistEntry(fingerprint=fingerprint, source_bank=bank_id, match_count=1))
        session.commit()
        session.close()
        return result

    is_new_bank = entry.source_bank != bank_id
    within_window = datetime.utcnow() - entry.first_seen <= REACTIVE_WINDOW

    entry.match_count += 1
    session.add(entry)

    alert_type = None
    if is_new_bank:
        alert_type = "proactive"
    elif within_window and entry.match_count >= 2:
        alert_type = "reactive"

    if alert_type:
        session.add(
            Alert(
                fingerprint=fingerprint,
                banks_involved=f"{entry.source_bank},{bank_id}",
                alert_type=alert_type,
            )
        )
        result = {"alert": True, "type": alert_type}

    session.commit()
    session.close()
    return result