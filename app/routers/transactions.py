from fastapi import APIRouter, HTTPException
from app.bank_registry import bank_exists
from app.database import get_bank_session
from app.models import Transaction
from app.schemas import TransactionIn, TransactionOut
from app.rules import evaluate_rules
from app.fingerprint import make_fingerprint
from app.watchlist_service import process_fingerprint

router = APIRouter(prefix="/banks/{bank_id}/transactions", tags=["transactions"])


def _validate_bank(bank_id: str):
    if not bank_exists(bank_id):
        raise HTTPException(status_code=404, detail=f"Unknown bank '{bank_id}'")


@router.get("")
def list_transactions(bank_id: str, limit: int = 25):
    _validate_bank(bank_id)
    session = get_bank_session(bank_id)
    txns = (
        session.query(Transaction)
        .order_by(Transaction.timestamp.desc())
        .limit(limit)
        .all()
    )
    session.close()
    return [
        {
            "id": t.id,
            "name": t.name,
            "account_last4": t.account_last4,
            "amount": t.amount,
            "flagged": t.flagged,
            "reason": t.reason,
            "timestamp": t.timestamp,
        }
        for t in txns
    ]


@router.post("", response_model=TransactionOut)
def create_transaction(bank_id: str, payload: TransactionIn):
    _validate_bank(bank_id)
    session = get_bank_session(bank_id)

    flagged, reason = evaluate_rules(payload.amount, payload.device_id)
    fingerprint = None
    if flagged:
        fingerprint = make_fingerprint(payload.name, payload.dob, payload.account_last4)

    txn = Transaction(
        name=payload.name,
        dob=payload.dob,
        account_last4=payload.account_last4,
        amount=payload.amount,
        device_id=payload.device_id,
        flagged=flagged,
        reason=reason,
        fingerprint=fingerprint,
    )
    session.add(txn)
    session.commit()
    session.refresh(txn)
    session.close()

    if flagged:
        process_fingerprint(fingerprint, bank_id)

    return txn