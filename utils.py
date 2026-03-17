import os

from constants import PAYMENT_FILE


def get_payment_day():
    day = os.environ.get("PAYMENT_DAY")
    if day:
        return int(day)

    if os.path.exists(PAYMENT_FILE):
        with open(PAYMENT_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)

    return 1