from fastapi import APIRouter, HTTPException
from app.config import BANKS
from app.database import get_bank_session
from app.models import Transaction
from app.schemas import TransactionIn, TransactionOut
from app.rules import evaluate_rules

router = APIRouter(prefix="/banks/{bank_id}/transactions", tags=["transactions"])


def _validate_bank(bank_id: str):
    if bank_id not in BANKS:
        raise HTTPException(status_code=404, detail=f"Unknown bank '{bank_id}'")


@router.post("", response_model=TransactionOut)
def create_transaction(bank_id: str, payload: TransactionIn):
    _validate_bank(bank_id)
    session = get_bank_session(bank_id)

    flagged, reason = evaluate_rules(payload.amount, payload.device_id)

    txn = Transaction(
        name=payload.name,
        dob=payload.dob,
        account_last4=payload.account_last4,
        amount=payload.amount,
        device_id=payload.device_id,
        flagged=flagged,
        reason=reason,
    )
    session.add(txn)
    session.commit()
    session.refresh(txn)
    session.close()

    return txn