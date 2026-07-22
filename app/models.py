from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import BankBase


class Transaction(BankBase):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    account_last4 = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    device_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    flagged = Column(Boolean, default=False)
    reason = Column(String, nullable=True)