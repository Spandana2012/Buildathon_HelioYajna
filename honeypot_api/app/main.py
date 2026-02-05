import os
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")


# Generate believable honeypot reply
def generate_reply(text: str) -> str:
    msg = text.lower()

    if "otp" in msg:
        return "Okay sir, I received OTP message. Should I share it here?"
    if "blocked" in msg or "suspended" in msg:
        return "Why is my account being suspended? I didn’t do anything."
    if "link" in msg or "click" in msg:
        return "Okay, should I open the link now? Please confirm."
    if "upi" in msg:
        return "Sure, please share your UPI ID properly so I can pay."
    if "account number" in msg:
        return "Okay, I can share. Can you confirm your bank officer ID first?"

    return "Sorry, I am confused. Can you explain again?"


@app.post("/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):

    # API key validation
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "reply": "Unauthorized"}
        )

    # Safe JSON parsing
    try:
        body = await request.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        body = {}

    # GUVI format parsing
    session_id = body.get("sessionId", "default")

    message_obj = body.get("message", {})
    if not isinstance(message_obj, dict):
        message_obj = {}

    scam_text = message_obj.get("text", "")

    # Generate reply
    reply = generate_reply(str(scam_text))

    # Must return ONLY this format
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "reply": reply
        }
    )
