from fastapi import APIRouter, HTTPException
from app.bank_registry import bank_exists
from app.database import get_shared_session
from app.models import WatchlistEntry

router = APIRouter(prefix="/banks/{bank_id}/watchlist", tags=["watchlist"])


@router.get("")
def get_watchlist(bank_id: str):
    if not bank_exists(bank_id):
        raise HTTPException(status_code=404, detail=f"Unknown bank '{bank_id}'")

    session = get_shared_session()
    entries = session.query(WatchlistEntry).all()
    session.close()

    return [
        {
            "fingerprint": e.fingerprint,
            "source_bank": e.source_bank,
            "first_seen": e.first_seen,
            "match_count": e.match_count,
        }
        for e in entries
    ]