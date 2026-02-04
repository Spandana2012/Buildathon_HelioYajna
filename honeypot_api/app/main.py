from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import os

from honeypot_api.app.detector import detect_scam
from honeypot_api.app.extractor import extract_intelligence
from honeypot_api.app.memory import update_conversation, get_metrics

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")

@app.post("/honeypot", include_in_schema=False)
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # API key check
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    # NEVER force JSON parsing
    body = {}
    if request.headers.get("content-type") == "application/json":
        try:
            body = await request.json()
        except Exception:
            body = {}

    conversation_id = str(body.get("conversation_id", "default"))
    message = str(body.get("message", ""))

    # Safe memory
    try:
        update_conversation(conversation_id)
        turns, duration = get_metrics(conversation_id)
    except Exception:
        turns, duration = 1, 0

    # Safe logic
    try:
        scam_detected = detect_scam(message)
    except Exception:
        scam_detected = False

    try:
        extracted = extract_intelligence(message)
    except Exception:
        extracted = {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_links": []
        }

    # ALWAYS return JSON (tester requirement)
    return JSONResponse(
        status_code=200,
        content={
            "scam_detected": scam_detected,
            "engagement_metrics": {
                "conversation_turns": turns,
                "engagement_duration_seconds": duration
            },
            "extracted_intelligence": extracted
        }
    )
