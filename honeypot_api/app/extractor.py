import re

BANK_REGEX = r"\b\d{9,18}\b"
UPI_REGEX = r"\b[\w.-]+@[\w.-]+\b"
URL_REGEX = r"https?://[^\s]+"


def extract_intelligence(message: str):
    if not message:
        return {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }

    bank_accounts = re.findall(BANK_REGEX, message)
    upi_ids = re.findall(UPI_REGEX, message)
    phishing_links = re.findall(URL_REGEX, message)

    return {
        "bank_accounts": bank_accounts,
        "upi_ids": upi_ids,
        "phishing_links": phishing_links
    }
