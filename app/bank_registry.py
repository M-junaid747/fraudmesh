from app.database import get_shared_session
from app.models import Bank

DEFAULT_BANKS = [
    ("bank_a", "Bank A"),
    ("bank_b", "Bank B"),
    ("bank_c", "Bank C"),
]


def seed_default_banks():
    """Runs once at startup. If the bank registry is empty (first-ever run,
    fresh deploy, wiped volume), seed it with 3 default banks so the demo
    isn't blank. Never overwrites banks that already exist."""
    session = get_shared_session()
    if session.query(Bank).count() == 0:
        for bank_id, name in DEFAULT_BANKS:
            session.add(Bank(id=bank_id, display_name=name))
        session.commit()
    session.close()


def list_banks():
    """Returns full Bank rows, ordered by creation time."""
    session = get_shared_session()
    banks = session.query(Bank).order_by(Bank.created_at).all()
    session.close()
    return banks


def get_bank_ids():
    return [b.id for b in list_banks()]


def bank_exists(bank_id: str) -> bool:
    return bank_id in get_bank_ids()