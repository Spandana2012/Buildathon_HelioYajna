import os
import random
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any


app = FastAPI()

API_KEY = os.getenv("API_KEY", "changeme")


# -------------------------
# GUVI Request Format Model
# -------------------------
class MessageModel(BaseModel):
    sender: str
    text: str
    timestamp: int


class HoneypotRequestModel(BaseModel):
    sessionId: str
    message: MessageModel
    conversationHistory: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}


# -------------------------
# Dynamic Honeypot Reply Generator
# -------------------------
def generate_reply(text: str, conversation_history: list) -> str:
    msg = text.lower()

    # Count how many times scammer asked OTP
    otp_count = 0
    for item in conversation_history:
        if isinstance(item, dict) and "text" in item:
            if "otp" in str(item["text"]).lower():
                otp_count += 1

    # OTP Handling
    if "otp" in msg:
        otp_replies = [
            "I received an OTP message. Should I share it here?",
            "Sir I am not receiving OTP. Can you resend it?",
            "OTP came but it got expired. Can you send again?",
            "Wait sir, my phone is not showing OTP properly. Give me 2 minutes.",
            "I got OTP but my family said OTP should not be shared. Is it safe?",
            "Sir my phone network is very weak. I will send OTP once it comes.",
            "OTP message came but it disappeared quickly. Please resend."
        ]

        # If scammer repeats OTP many times, act more confused
        if otp_count >= 2:
            return random.choice([
                "Sir you are asking OTP again and again. Why is it needed so many times?",
                "I already told you OTP is not coming. Please wait some time.",
                "I feel suspicious sir. Can you confirm your employee ID first?"
            ])

        return random.choice(otp_replies)

    # UPI PIN / PIN Handling
    if "upi pin" in msg or "pin" in msg:
        return random.choice([
            "UPI PIN? I thought PIN should never be shared. Why do you need it?",
            "Sir I forgot my UPI PIN. Can you guide me how to reset it?",
            "I don’t remember my PIN. Should I open Google Pay to check?",
            "Sir my UPI app is locked. What should I do now?"
        ])

    # Account blocked / suspended
    if "blocked" in msg or "suspended" in msg:
        return random.choice([
            "Oh no 😟 why is my account being blocked? I have important money inside.",
            "Sir please help me, my salary is in that account. What should I do?",
            "Why is my account suspended suddenly? I didn’t do anything wrong."
        ])

    # Bank account number request
    if "account number" in msg or "account no" in msg:
        return random.choice([
            "My passbook is inside my bag. Can you wait 2 minutes?",
            "Okay sir, I will share account number. Please don’t block my account.",
            "Sir should I share full account number or last 4 digits?"
        ])

    # Links / click
    if "link" in msg or "click" in msg:
        return random.choice([
            "Okay sir, should I open the link now? It looks suspicious.",
            "I clicked but it is asking for my PIN. Is it safe?",
            "Sir this link is not opening. Can you send again?"
        ])

    # Money transfer
    if "send" in msg or "pay" in msg or "transfer" in msg:
        return random.choice([
            "Okay sir, I will transfer now. Please confirm the amount again.",
            "Sir I am trying to send money but it shows error. What should I do?",
            "Okay, should I send money through UPI or net banking?"
        ])

    # Default reply
    return random.choice([
        "Sorry sir, I didn’t understand properly. Can you explain again?",
        "Okay sir, what should I do now?",
        "Please help me, I am worried about my account."
    ])


# -------------------------
# Main Honeypot Endpoint (GUVI Compatible)
# -------------------------
@app.post("/honeypot")
async def honeypot(payload: HoneypotRequestModel, x_api_key: str = Header(None)):

    # API Key validation
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "reply": "Unauthorized"
            }
        )

    scam_text = payload.message.text
    history = payload.conversationHistory

    reply = generate_reply(scam_text, history)

    # GUVI expected response format
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "reply": reply
        }
    )
