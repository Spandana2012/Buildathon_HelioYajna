import os
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from honeypot_api.app.detector import detect_scam
from honeypot_api.app.extractor import extract_intelligence
from honeypot_api.app.memory import update_conversation, get_metrics

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")

@app.api_route("/honeypot", methods=["POST", "GET"])
async def honeypot(request: Request, x_api_key: str = Header(None)):

    # Always return JSON (even for errors)
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"scam_detected": False,
                     "engagement_metrics": {"conversation_turns": 0, "engagement_duration_seconds": 0},
                     "extracted_intelligence": {"bank_accounts": [], "upi_ids": [], "phishing_links": []}}
        )

    # Read body safely
    body = {}
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    conversation_id = str(body.get("conversation_id") or "default")
    message = str(body.get("message") or "")

    # Safe memory
    try:
        update_conversation(conversation_id)
        turns, duration = get_metrics(conversation_id)
    except Exception:
        turns, duration = 1, 0

    # Safe scam detection
    try:
        scam_detected = detect_scam(message)
    except Exception:
        scam_detected = False

    # Safe extraction
    try:
        extracted = extract_intelligence(message)
    except Exception:
        extracted = {"bank_accounts": [], "upi_ids": [], "phishing_links": []}

    # Always JSON output
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
