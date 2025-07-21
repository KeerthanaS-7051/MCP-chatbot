import requests
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MCP_URL = "http://localhost:8000"
session_id = "user123"

def get_context():
    res = requests.get(f"{MCP_URL}/context/{session_id}")
    context = res.json()

    if "system_prompt" not in context:
        print("❌ No valid context found for this session.")
        print("💡 Hint: Run init_context.py or check your session_id.")
        exit()

    return context

def update_context(new_messages):
    update_payload = {
        "session_id": session_id,
        "context": {
            "conversation_history": new_messages
        }
    }
    res = requests.post(f"{MCP_URL}/context", json=update_payload)
    return res.json()

def build_prompt(context, user_input):
    history = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" 
        for msg in context.get("conversation_history", [])
    )

    return f"""{context['system_prompt']}

User Profile:
Name: {context['user_profile']['name']}
Language: {context['user_profile']['language']}
Preferences: {', '.join(context['user_profile']['preferences'])}

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

def chatbot_loop():
    print("🤖 MCP Chatbot (LLaMA 3 + Context + Memory) is ready. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        context = get_context()  
        prompt = build_prompt(context, user_input)
        response = call_llama(prompt)
        
        print(f"\nAssistant: {response}\n")

        # Add memory
        new_messages = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response}
        ]
        update_context(new_messages)

if __name__ == "__main__":
    chatbot_loop()
