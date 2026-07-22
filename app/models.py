from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import BankBase, SharedBase


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
    fingerprint = Column(String, nullable=True)

class WatchlistEntry(SharedBase):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True)
    fingerprint = Column(String, unique=True, nullable=False)
    source_bank = Column(String, nullable=False)
    first_seen = Column(DateTime, default=datetime.utcnow)
    match_count = Column(Integer, default=1)


class Alert(SharedBase):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    fingerprint = Column(String, nullable=False)
    banks_involved = Column(String, nullable=False)
    alert_type = Column(String, nullable=False)  # "reactive" or "proactive"
    created_at = Column(DateTime, default=datetime.utcnow)