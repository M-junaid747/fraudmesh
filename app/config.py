import os

BANKS = ["bank_a", "bank_b", "bank_c"]
AMOUNT_THRESHOLD = float(os.getenv("AMOUNT_THRESHOLD", 5000))