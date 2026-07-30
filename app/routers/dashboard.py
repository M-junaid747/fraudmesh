from fastapi import APIRouter
from app.bank_registry import get_bank_ids
from app.database import get_shared_session, get_bank_session
from app.models import Alert, WatchlistEntry, Transaction

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/alerts")
def get_alerts():
    session = get_shared_session()
    alerts = session.query(Alert).order_by(Alert.created_at.desc()).all()
    session.close()

    return [
        {
            "fingerprint": a.fingerprint,
            "banks_involved": a.banks_involved.split(","),
            "alert_type": a.alert_type,
            "created_at": a.created_at,
        }
        for a in alerts
    ]


@router.get("/summary")
def get_summary():
    banks_summary = []
    for bank_id in get_bank_ids():
        session = get_bank_session(bank_id)
        total = session.query(Transaction).count()
        flagged = session.query(Transaction).filter_by(flagged=True).count()
        session.close()
        banks_summary.append(
            {"bank_id": bank_id, "total_transactions": total, "flagged": flagged}
        )

    shared = get_shared_session()
    total_alerts = shared.query(Alert).count()
    total_watchlist = shared.query(WatchlistEntry).count()
    shared.close()

    return {
        "banks": banks_summary,
        "total_alerts": total_alerts,
        "total_watchlist_entries": total_watchlist,
    }