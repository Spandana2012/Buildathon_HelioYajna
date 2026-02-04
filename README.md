🛡️ Agentic Honey‑Pot for Scam Detection & Intelligence Extraction
This project implements an AI-powered Agentic Honey‑Pot API that detects scam messages and extracts actionable scammer intelligence such as bank account details, UPI IDs, and phishing links.
The system is designed for hackathon evaluation using a public, secured API endpoint.

🚀 Features
Scam intent detection from incoming messages

Secure API access using API key authentication

Multi‑turn conversation tracking

Extraction of scammer‑provided intelligence:

Bank account numbers

UPI IDs

Phishing URLs

Structured JSON response as per evaluation requirements

Deployed as a public REST API

🧰 Tech Stack
Backend: Python, FastAPI

Server: Uvicorn

Deployment: Render (or any public cloud service)

📁 Project Structure
honeypot-api/
│
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── detector.py      # Scam detection logic
│   ├── extractor.py     # Intelligence extraction (regex-based)
│   ├── memory.py        # Conversation tracking
│   └── models.py        # Request & response schemas
│
├── requirements.txt
└── README.md
🔐 API Authentication
All requests must include an API key in the request header.

Header:

x-api-key: YOUR_API_KEY
The API key is configured as an environment variable (API_KEY) in the deployment environment.

📡 API Endpoint
POST /honeypot
Request Body
{
  "conversation_id": "conv_001",
  "message": "Your account is blocked. Click this link to verify."
}
Successful Response
{
  "scam_detected": true,
  "engagement_metrics": {
    "conversation_turns": 1,
    "engagement_duration_seconds": 5
  },
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_links": []
  }
}
🧠 How It Works
Incoming messages are received via a public API endpoint

Messages are analyzed to detect scam intent

Conversation context is tracked using a conversation ID

Scam-related intelligence is extracted from scammer messages

Results are returned in a structured JSON format

⚠️ The system never collects or exposes real user data.
All engagement uses a fake persona to safely interact with scammers.

🛠️ Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload
☁️ Deployment
The application is deployed as a public web service with:

API key authentication

HTTPS endpoint

Stable JSON responses

Deployment platforms supported:

Render (recommended)

Railway

Fly.io

AWS / GCP

🧪 Testing
The endpoint can be tested using:

cURL / Postman

Hackathon Honeypot API Endpoint Tester

🎯 Hackathon Context
This project is built for the Agentic Honey‑Pot for Scam Detection & Intelligence Extraction problem statement.
The API is designed to meet all evaluation requirements related to:

Authentication

Endpoint availability

Response structure

Stability

📌 Notes
This repository focuses on correctness and stability for evaluation

Advanced AI behaviors can be added in later iterations

The current implementation is sufficient for automated testing

👥 Team
Team Name: Helio Yajna
Hackathon: GUVI Buildathon