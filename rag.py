# rag.py
import os
from dotenv import load_dotenv
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI()

# Load local embedder (free, no quota issues)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the persistent Chroma database
db = PersistentClient(path="chroma")
coll = db.get_or_create_collection("glider-kb")

# System instructions
SYSTEM_RULES = (
    "You are a Slocum glider mission assistant. "
    "Your task is to convert human instructions into valid mission files. "
    "There are two main types of files:\n"
    " - `.ma` files (mission arguments): consist only of parameter assignments with `SET`. "
    "   Example: `SET f_max_working_depth = 800`.\n"
    " - `.mi` files (mission instructions): define mission flow. They may include `.ma` files "
    "   and use commands like `goto_waypoint`, `goto_list`, `dive_to`, `hold`, `climb_to_surface`, "
    "`surface_every`, `if ... endif`, `abort_mission`, `report`, and loops.\n"
    "Always use the syntax consistent with the file type. "
    "Never output YAML, JSON, or pseudocode. "
    "If unsure, reply exactly: 'I don’t have information about that in the provided files.'"
)



def retrieve(query: str, k: int = 6):
    """Retrieve top-k most relevant chunks from the knowledge base."""
    q_emb = embedder.encode([query]).tolist()[0]
    res = coll.query(query_embeddings=[q_emb], n_results=k)
    
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    ctx_lines = []
    for d, m in zip(docs, metas):
        src = m.get("source", "unknown")
        chunk = m.get("chunk", 0)
        ctx_lines.append(f"[{src}#{chunk}]\n{d}")

    return "\n\n---\n\n".join(ctx_lines)

def answer(query: str) -> str:
    """Answer a question using retrieved context + LLM."""
    context = retrieve(query)
    messages = [
        {"role": "system", "content": SYSTEM_RULES},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",   # use GPT for answers
        messages=messages,
        temperature=0
    )
    return resp.choices[0].message.content
