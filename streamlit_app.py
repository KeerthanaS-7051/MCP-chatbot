import streamlit as st
import requests
import subprocess
import uuid

MCP_URL = "http://localhost:8000"
if "session_id" not in st.session_state:
    st.session_state.session_id = st.text_input("Enter your session ID (or leave blank to auto-generate):")
    if st.session_state.session_id == "":
        st.session_state.session_id = str(uuid.uuid4())
        st.success(f"Generated Session ID: {st.session_state.session_id}")

session_id = st.session_state.session_id

def get_context():
    res = requests.get(f"{MCP_URL}/context/{session_id}")
    return res.json()

def update_context(context):
    requests.post(f"{MCP_URL}/context", json={
        "session_id": session_id,
        "context": context
    })

def build_prompt(context, user_input):
    history = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in context.get("conversation_history", [])
    )
    profile = context.get("user_profile", {})
    name = profile.get("name", "User")
    language = profile.get("language", "English")
    preferences = ", ".join(profile.get("preferences", []))

    return f"""{context['system_prompt']}

User Profile:
Name: {name}
Language: {language}
Preferences: {preferences}

Conversation History:
{history}

User: {user_input}
Assistant:"""

def call_llama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True, text=True
    )
    return result.stdout.strip()

st.title("🤖 MCP Chatbot")

if "context" not in st.session_state:
    st.session_state.context = get_context()

if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.context.get("conversation_history", [])

def handle_submit():
    user_input = st.session_state.input
    if not user_input.strip():
        return

    prompt = build_prompt(st.session_state.context, user_input)
    response = call_llama(prompt)

    new_messages = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response}
    ]

    st.session_state.context["conversation_history"].extend(new_messages)
    update_context({"conversation_history": new_messages})

    st.session_state.input = ""

st.text_input("You:", key="input", on_change=handle_submit)

for msg in st.session_state.messages:
    role = "You" if msg["role"] == "user" else "Assistant"
    st.markdown(f"**{role}:** {msg['content']}")
