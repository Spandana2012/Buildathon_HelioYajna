import time

# In-memory storage
conversations = {}


def init_conversation(conversation_id: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = {
            "start_time": time.time(),
            "turns": 0,
            "history": []
        }


def add_message(conversation_id: str, sender: str, message: str):
    init_conversation(conversation_id)

    conversations[conversation_id]["turns"] += 1
    conversations[conversation_id]["history"].append({
        "sender": sender,
        "message": message,
        "timestamp": int(time.time())
    })


def get_metrics(conversation_id: str):
    init_conversation(conversation_id)

    turns = conversations[conversation_id]["turns"]
    duration = int(time.time() - conversations[conversation_id]["start_time"])

    return turns, duration


def get_conversation(conversation_id: str):
    return conversations.get(conversation_id, None)
