from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

CHROMA_PATH = "data/chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

def ingest_document(file_path: str) -> dict:
    # Step 1 — Load PDF and extract text
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")

    # Step 2 — Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Step 3 — Create embeddings (runs locally, no API needed)
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Step 4 — Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Stored in ChromaDB at {CHROMA_PATH}")

    return {
        "pages_loaded": len(documents),
        "chunks_created": len(chunks),
        "source": file_path
    }


# Quick test — run this file directly to test
if __name__ == "__main__":
    # Put any PDF in data/uploads/ and test here
    result = ingest_document("data/uploads/test.pdf")
    print(f"Done: {result}")