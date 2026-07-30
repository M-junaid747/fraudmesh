from typing import Optional
from pydantic import BaseModel


class TransactionIn(BaseModel):
    name: str
    dob: str
    account_last4: str
    amount: float
    device_id: Optional[str] = None


class TransactionOut(BaseModel):
    id: int
    amount: float
    flagged: bool
    reason: Optional[str] = None
    fingerprint: Optional[str] = None

    class Config:
        from_attributes = True


class BankIn(BaseModel):
    bank_id: str
    display_name: Optional[str] = None