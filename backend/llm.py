from dotenv import load_dotenv
import openai, os
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_with_context(query: str, chunks: list) -> dict:
    context = "\n\n".join([
        f"[Source: {c['source']}, Page {c['page']}]\n{c['content']}"
        for c in chunks
    ])

    system_prompt = """Answer only from the context provided.
If the answer is not in the context, say
'I don't have enough information.'
Always cite the source and page number."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [{"source": c["source"], "page": c["page"]} for c in chunks]
    }