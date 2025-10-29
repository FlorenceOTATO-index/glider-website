# ingest.py
import os, re, pathlib, json
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
client = OpenAI()

# 1) Read every file under kb/
kb_dir = pathlib.Path("kb")
docs = []
for p in kb_dir.rglob("*"):
    if p.is_file():
        text = p.read_text(errors="ignore")
        # normalize UNIX comments => plain text
        text = re.sub(r"^\s*#.*$", "", text, flags=re.MULTILINE)
        docs.append({"id": str(p), "text": text})

# 2) Chunk
splitter = RecursiveCharacterTextSplitter(
    chunk_size=900, chunk_overlap=120,
    separators=["\n\n", "\n", " ", ""]
)
chunks, metadatas, ids = [], [], []
for d in docs:
    pieces = splitter.split_text(d["text"])
    for i, piece in enumerate(pieces):
        chunks.append(piece)
        metadatas.append({"source": d["id"], "chunk": i})
        ids.append(f"{d['id']}::chunk::{i}")

# 3) Embed
embs = []
for piece in chunks:
    embs.append(
        client.embeddings.create(
            model="text-embedding-3-small",
            input=piece
        ).data[0].embedding
    )

# 4) Store (Chroma persistent)
db = PersistentClient(path="chroma")
coll = db.get_or_create_collection(name="glider-kb")
coll.upsert(ids=ids, embeddings=embs, metadatas=metadatas, documents=chunks)

print(f"Ingested {len(chunks)} chunks into 'glider-kb'")
