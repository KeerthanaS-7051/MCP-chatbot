import requests

MCP_URL = "http://localhost:8000/context"
session_id = "user123"

data = {
    "session_id": session_id,
    "context": {
        "system_prompt": "You are an assistant that answers in a clear and concise way.",
        "user_profile": {
            "name": "Keerthana",
            "language": "English",
            "preferences": ["tech", "simple language", "examples"]
        }
    }
}

res = requests.post(MCP_URL, json=data)
print(res.json())
