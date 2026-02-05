import os
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

from honeypot_api.app.detector import detect_scam
from honeypot_api.app.extractor import extract_intelligence
from honeypot_api.app.memory import add_message, get_metrics, get_conversation

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")


# Generate honeypot reply (simple believable human response)
def generate_reply(message: str) -> str:
    msg = message.lower()

    if "otp" in msg:
        return "Okay sir, I received OTP message. Should I share it here?"
    if "account" in msg and "blocked" in msg:
        return "Oh no 😟 please help me, what should I do now?"
    if "link" in msg or "click" in msg:
        return "Okay, should I open the link now? Is it safe?"
    if "upi" in msg:
        return "I can pay. Please share your UPI ID properly."
    if "bank" in msg:
        return "Okay sir, which bank department are you from?"

    return "Sorry I am confused. Can you explain again?"


@app.api_route("/honeypot", methods=["GET", "POST", "HEAD"])
async def honeypot(request: Request, x_api_key: str = Header(None)):

    # Always validate API key
    if x_api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    # Safe request body handling
    body = {}
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    conversation_id = str(body.get("conversation_id") or "default")
    message = str(body.get("message") or "")

    # Store scammer message
    add_message(conversation_id, "scammer", message)

    # Scam detection + extraction
    scam_detected = detect_scam(message)
    extracted = extract_intelligence(message)

    # Honeypot reply (conversation building)
    reply = generate_reply(message)
    add_message(conversation_id, "honeypot", reply)

    turns, duration = get_metrics(conversation_id)

    return JSONResponse(
        status_code=200,
        content={
            "scam_detected": scam_detected,
            "engagement_metrics": {
                "conversation_turns": turns,
                "engagement_duration_seconds": duration
            },
            "extracted_intelligence": extracted,
            "honeypot_reply": reply
        }
    )


@app.get("/conversation/{conversation_id}")
async def show_conversation(conversation_id: str, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    convo = get_conversation(conversation_id)

    if convo is None:
        return JSONResponse(status_code=404, content={"detail": "Conversation not found"})

    return JSONResponse(
        status_code=200,
        content={
            "conversation_id": conversation_id,
            "turns": convo["turns"],
            "history": convo["history"]
        }
    )
