from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "data/chroma_db"
EMBED_MODEL  = "all-MiniLM-L6-v2"

def retrieve_chunks(query: str, k: int = 4) -> list:
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search_with_score(query, k=k)

    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "page":   doc.metadata.get("page", 0),
            "score":  round(float(score), 3)
        }
        for doc, score in results
    ]


# Quick test — run this file directly
if __name__ == "__main__":
    results = retrieve_chunks("what is this document about?")
    for r in results:
        print(f"Score: {r['score']} | Page: {r['page']}")
        print(r["content"][:100], "...\n")