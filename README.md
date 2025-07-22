MCP Chatbot - Intelligent Data Query Assistant



This is an AI-powered chatbot built using the Model Context Protocol (MCP) architecture. It enables users to ask natural language questions and receive intelligent responses based on backend data using LangChain, LLaMA, and Streamlit.



---



Features



\- Conversational AI using LLaMA 3 (via Ollama/Together AI)

\- Memory-powered chat with context awareness

\- Connects to structured databases (like SQLite)

\- Built using LangChain for prompt engineering and chaining

\- FastAPI backend + Streamlit frontend

\- Model Context Protocol (MCP) for context isolation and memory



---
How to Run

\-Ensure LLaMA is running

\-In terminal run the MCP server
cd yourFileLocation
venv\Scripts\activate
uvicorn main:app --reload

\-Run the streamlit application (or) chatbot directly in terminal
cd yourFileLocation
streamlit run streamlit_app.py
(or)
python run chatbot.py




