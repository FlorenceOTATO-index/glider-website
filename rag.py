# rag.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient

load_dotenv()
client = OpenAI()

db = PersistentClient(path="chroma")
coll = db.get_or_create_collection("glider-kb")

SYSTEM_RULES = (
    "You are a strict domain assistant for Slocum glider conventions. "
    "Answer ONLY from the provided context chunks. "
    "If the answer isn’t in the context, reply exactly: "
    "\"I don’t have information about that in the provided files.\""
)

def retrieve(query: str, k: int = 6):
    q_emb = client.embeddings.create(
        model="text-embedding-3-small", input=query
    ).data[0].embedding
    res = coll.query(query_embeddings=[q_emb], n_results=k)
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    # Format a concise context block
    ctx_lines = []
    for d, m in zip(docs, metas):
        src = m.get("source", "unknown")
        chunk = m.get("chunk", 0)
        ctx_lines.append(f"[{src}#{chunk}]\n{d}")
    return "\n\n---\n\n".join(ctx_lines)

def answer(query: str) -> str:
    context = retrieve(query)
    messages = [
        {"role": "system", "content": SYSTEM_RULES},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )
    return resp.choices[0].message.content
