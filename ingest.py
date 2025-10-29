# ingest.py
import pathlib, re
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load local embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 1) Read files
kb_dir = pathlib.Path("kb")
docs = []
for p in kb_dir.rglob("*"):
    if p.is_file():
        text = p.read_text(errors="ignore")
        text = re.sub(r"^\s*#.*$", "", text, flags=re.MULTILINE)
        docs.append({"id": str(p), "text": text})

# 2) Chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
chunks, metadatas, ids = [], [], []
for d in docs:
    pieces = splitter.split_text(d["text"])
    for i, piece in enumerate(pieces):
        chunks.append(piece)
        metadatas.append({"source": d["id"], "chunk": i})
        ids.append(f"{d['id']}::chunk::{i}")

# 3) Embed locally
embs = embedder.encode(chunks).tolist()

# 4) Store
db = PersistentClient(path="chroma")
coll = db.get_or_create_collection(name="glider-kb")
coll.upsert(ids=ids, embeddings=embs, metadatas=metadatas, documents=chunks)

print(f"Ingested {len(chunks)} chunks into 'glider-kb'")
