import os
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")


# GUVI request format model
class MessageModel(BaseModel):
    sender: str
    text: str
    timestamp: int


class HoneypotRequestModel(BaseModel):
    sessionId: str
    message: MessageModel
    conversationHistory: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}


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
async def honeypot(payload: HoneypotRequestModel, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"status": "error", "reply": "Unauthorized"}
        )

    scam_text = payload.message.text
    reply = generate_reply(scam_text)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "reply": reply
        }
    )
