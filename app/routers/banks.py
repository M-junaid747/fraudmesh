import re
from fastapi import APIRouter, HTTPException
from app.database import get_shared_session
from app.models import Bank
from app.schemas import BankIn

router = APIRouter(prefix="/banks", tags=["banks"])

# lowercase letters/numbers/underscores, starting with a letter, 2-32 chars.
# Enforced because bank_id doubles as a URL path segment and a SQLite filename.
BANK_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")


@router.get("")
def list_banks_endpoint():
    session = get_shared_session()
    banks = session.query(Bank).order_by(Bank.created_at).all()
    session.close()
    return {
        "banks": [b.id for b in banks],
        "details": [
            {"bank_id": b.id, "display_name": b.display_name, "created_at": b.created_at}
            for b in banks
        ],
    }


@router.post("", status_code=201)
def create_bank(payload: BankIn):
    bank_id = payload.bank_id.strip().lower()
    if not BANK_ID_PATTERN.match(bank_id):
        raise HTTPException(
            status_code=400,
            detail="bank_id must be lowercase letters/numbers/underscores, "
                   "start with a letter, and be 2-32 characters (e.g. 'bank_d').",
        )

    session = get_shared_session()
    if session.query(Bank).filter_by(id=bank_id).first():
        session.close()
        raise HTTPException(status_code=409, detail=f"Bank '{bank_id}' already exists")

    bank = Bank(id=bank_id, display_name=payload.display_name or bank_id)
    session.add(bank)
    session.commit()
    session.close()
    return {"bank_id": bank_id, "display_name": bank.display_name}


@router.delete("/{bank_id}")
def delete_bank(bank_id: str):
    """Removes a bank from the registry. Its historical transaction data
    (its private SQLite file) is left on disk untouched, not deleted —
    this only affects whether it's an active participant in the network."""
    session = get_shared_session()
    bank = session.query(Bank).filter_by(id=bank_id).first()
    if not bank:
        session.close()
        raise HTTPException(status_code=404, detail=f"Bank '{bank_id}' not found")
    session.delete(bank)
    session.commit()
    session.close()
    return {"deleted": bank_id}