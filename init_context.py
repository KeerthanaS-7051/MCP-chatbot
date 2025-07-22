import requests

MCP_URL = "http://localhost:8000/context"
session_id = input("Enter session ID (or leave blank to generate): ")
if not session_id:
    session_id = str(uuid.uuid4())
    print("Generated session_id:", session_id)

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
