from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os, sys
from dotenv import load_dotenv

load_dotenv()  # add this line

sys.path.append(os.path.dirname(__file__))

from backend.ingest import ingest_document
from backend.retriever import retrieve_chunks
from backend.llm import answer_with_context

app = FastAPI(title="RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    question: str
    k: int = 4


@app.get("/")
async def root():
    return {"status": "RAG API is running"}


@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    os.makedirs("data/uploads", exist_ok=True)
    save_path = f"data/uploads/{file.filename}"

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = ingest_document(save_path)
    return {"status": "success", **result}


@app.post("/chat")
async def chat(req: QueryRequest):
    chunks = retrieve_chunks(req.question, k=req.k)

    if not chunks:
        return {
            "answer": "No documents found. Please upload a PDF first.",
            "sources": [],
            "chunks": []
        }

    result = answer_with_context(req.question, chunks)
    result["chunks"] = chunks
    return result