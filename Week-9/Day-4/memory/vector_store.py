import faiss
import sqlite3
import os
import numpy as np
from sentence_transformers import SentenceTransformer

from autogen_core.memory import (
    Memory,
    MemoryContent,
    MemoryMimeType,
    MemoryQueryResult,
    UpdateContextResult,
)


class FaissSQLiteMemory(Memory):
    def __init__(self, db_path="memory/long_term.db", k=5, threshold=0.8):
        self.db_path = db_path
        self.k = k
        self.threshold = threshold

        # Embedder
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.embedder.get_sentence_embedding_dimension()

        # FAISS index file
        self.index_file = "memory/faiss.index"
        self.index = faiss.IndexFlatL2(self.dim)

        # SQLite connection
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

        # Loading existing memory
        self._load_existing()

    # Initializing the SQLite and using UNIQUE constraint so that no duplicate question gets saved again in the DB
    def _init_db(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
        """)
        self.conn.commit()

    # Load FAISS index from SQLite if exists otherwise rebuilt it
    def _load_existing(self):

        # Load FAISS index if exists
        if os.path.exists(self.index_file):
            print("Loading FAISS index from disk...")
            self.index = faiss.read_index(self.index_file)
            return

        # Otherwise rebuild from DB
        rows = self.conn.execute("SELECT question, answer FROM memory").fetchall()

        if rows:
            texts = [f"Q: {q}\nA: {a}" for q, a in rows]
            embeddings = self.embedder.encode(texts).astype("float32")
            self.index.add(embeddings)

        print("FAISS rebuilt from SQLite.")

    # Adding memory only if new
    async def add(self, content: str, question: str = ""):

        # Preventing duplicate episodic insert
        existing = self.conn.execute(
            "SELECT id FROM memory WHERE question = ?",
            (question,),
        ).fetchone()

        if existing:
            print("Already stored. Skipping duplicate save.")
            return

        # Inserting into SQLite
        self.conn.execute(
            "INSERT INTO memory (question, answer) VALUES (?, ?)",
            (question, content),
        )
        self.conn.commit()

        # Adding embeddigns in FAISS
        text = f"Q: {question}\nA: {content}"
        emb = self.embedder.encode([text]).astype("float32")
        self.index.add(emb)

        # Updating the FAISS index(Saving into it)
        faiss.write_index(self.index, self.index_file)

        print("Saved to long-term memory.")

    # Query memory (Episodic and Semantic)
    async def query(self, query_str: str):

        # Episodic recall(Exact match)
        row = self.conn.execute(
            "SELECT answer FROM memory WHERE question = ?",
            (query_str,),
        ).fetchone()

        if row:
            return [
                MemoryContent(
                    content=row[0],
                    mime_type=MemoryMimeType.TEXT,
                    metadata={"source": "episodic_exact"},
                )
            ]

        # Semantic recall(FAISS Similarity)
        if self.index.ntotal == 0:
            return []

        q_emb = self.embedder.encode([query_str]).astype("float32")
        distances, indices = self.index.search(q_emb, self.k)

        results = []

        for dist, idx in zip(distances[0], indices[0]):

            # dist smaller = closer
            if dist > self.threshold:
                continue

            row = self.conn.execute(
                "SELECT answer FROM memory WHERE id = ?",
                (idx + 1,),
            ).fetchone()

            if not row:
                continue

            results.append(
                MemoryContent(
                    content=row[0],
                    mime_type=MemoryMimeType.TEXT,
                    metadata={"source": "semantic", "distance": float(dist)},
                )
            )

        return results

    
    async def update_context(self, model_context):

        last_user = None
        for msg in reversed(model_context._messages):
            if msg.source == "user":
                last_user = msg.content
                break

        if not last_user:
            return UpdateContextResult(memories=MemoryQueryResult(results=[]))

        results = await self.query(last_user)

        return UpdateContextResult(
            memories=MemoryQueryResult(results=results)
        )

    async def clear(self):
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()

        self.index.reset()
        faiss.write_index(self.index, self.index_file)

    async def close(self):
        self.conn.close()
