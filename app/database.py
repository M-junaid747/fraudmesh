import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

BankBase = declarative_base()
SharedBase = declarative_base()

_bank_engines = {}
_shared_engine = None


def get_bank_engine(bank_id: str):
    if bank_id not in _bank_engines:
        path = os.path.join(DATA_DIR, f"{bank_id}.db")
        _bank_engines[bank_id] = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
    return _bank_engines[bank_id]


def get_bank_session(bank_id: str):
    engine = get_bank_engine(bank_id)
    BankBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def get_shared_engine():
    global _shared_engine
    if _shared_engine is None:
        path = os.path.join(DATA_DIR, "shared.db")
        _shared_engine = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
    return _shared_engine


def get_shared_session():
    engine = get_shared_engine()
    SharedBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()