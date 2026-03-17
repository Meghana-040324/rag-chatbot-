# RAG Knowledge Base Chatbot
Upload any PDF and chat with it using AI.

## Live Demo
[Coming soon]

## Tech Stack
- LangChain + ChromaDB + OpenAI + FastAPI + Streamlit

## How to run
1. Clone repo
2. pip install -r requirements.txt
3. Add OPENAI_API_KEY to .env
4. cd backend && uvicorn main:app --reload
5. cd frontend && streamlit run app.py
```

Save it, then run:
```
git add README.md
git commit -m "docs: add README"
git push