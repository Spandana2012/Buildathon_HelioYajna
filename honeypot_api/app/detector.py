import re

SCAM_KEYWORDS = [
    "blocked", "otp", "urgent", "bank", "upi", "account",
    "kyc", "verification", "click", "link", "compromised",
    "fraud", "suspended", "loan", "reward", "prize"
]

URL_REGEX = r"https?://[^\s]+"
UPI_REGEX = r"\b[\w.-]+@[\w.-]+\b"


def detect_scam(message: str) -> bool:
    if not message:
        return False

    msg = message.lower()

    for keyword in SCAM_KEYWORDS:
        if keyword in msg:
            return True

    if re.search(URL_REGEX, message):
        return True

    if re.search(UPI_REGEX, message):
        return True

    return False
