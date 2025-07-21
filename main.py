from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

context_store: Dict[str, Dict] = {}

class ContextUpdate(BaseModel):
    session_id: str
    context: Dict

@app.get("/context/{session_id}")
def get_context(session_id: str):
    return context_store.get(session_id, {
        "system_prompt": "You are a helpful assistant.",
        "user_profile": {"name": "Keerthana", "language": "English"},
        "preferences": ["detailed", "technical"],
        "memory": {},
        "tools": [],
        "conversation_history": []
    })

@app.post("/context")
def update_context(update: ContextUpdate):
    session = context_store.get(update.session_id, {
        "system_prompt": "You are a helpful assistant.",
        "conversation_history": [],
        "memory": {},
        "tools": []
    })

    for key, value in update.context.items():
        if key == "conversation_history":
            session["conversation_history"].extend(value)
        else:
            session[key] = value

    context_store[update.session_id] = session
    return {"message": "Context updated successfully"}

