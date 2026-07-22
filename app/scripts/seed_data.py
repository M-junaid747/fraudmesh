"""
Seeds each bank with synthetic transactions over HTTP, including a
deliberate cross-bank fraud ring: the same identity makes a flagged
transaction at two different banks so the matching logic in M3 has
something real to catch. Run the API first, then run this script.
"""
import random
import requests
from faker import Faker

fake = Faker()
BASE_URL = "http://localhost:8000"
BANKS = ["bank_a", "bank_b", "bank_c"]


def random_transaction(flagged_identity=None):
    if flagged_identity:
        name, dob, last4 = flagged_identity
        amount = random.uniform(5000, 10000)  # over threshold -> gets flagged
    else:
        name = fake.name()
        dob = fake.date_of_birth().isoformat()
        last4 = str(random.randint(1000, 9999))
        amount = random.uniform(5, 500)  # normal, won't be flagged

    return {
        "name": name,
        "dob": dob,
        "account_last4": last4,
        "amount": round(amount, 2),
        "device_id": fake.uuid4(),
    }


def seed():
    # normal background traffic at every bank
    for bank in BANKS:
        for _ in range(15):
            requests.post(f"{BASE_URL}/banks/{bank}/transactions", json=random_transaction())

    # the fraud ring: same identity hits bank_a, then bank_b shortly after
    ring_identity = ("Jordan Casey", "1990-04-12", "7781")
    r1 = requests.post(f"{BASE_URL}/banks/bank_a/transactions", json=random_transaction(ring_identity))
    r2 = requests.post(f"{BASE_URL}/banks/bank_b/transactions", json=random_transaction(ring_identity))

    print("Ring transaction @ bank_a:", r1.json())
    print("Ring transaction @ bank_b:", r2.json())


if __name__ == "__main__":
    seed()