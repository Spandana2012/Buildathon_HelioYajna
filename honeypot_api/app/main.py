import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from honeypot_api.app.detector import detect_scam
from honeypot_api.app.extractor import extract_intelligence
from honeypot_api.app.memory import update_conversation, get_metrics

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")

@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # 1️⃣ API key validation
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    # 2️⃣ SAFELY read body (tester may send nothing)
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    # 3️⃣ SAFE defaults (CRITICAL)
    conversation_id = str(body.get("conversation_id") or "default")
    message = str(body.get("message") or "")

    # 4️⃣ SAFE memory update
    try:
        update_conversation(conversation_id)
        turns, duration = get_metrics(conversation_id)
    except Exception:
        turns, duration = 1, 0

    # 5️⃣ SAFE scam detection & extraction
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

    # 6️⃣ ALWAYS return valid JSON (no crash possible)
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
