import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, db_path="memory/long_term.db"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = 384

        # cosine similarity index
        self.index = faiss.IndexFlatIP(self.dim)
        self.id_map = []  # maps index position > db id

        self.conn = sqlite3.connect(db_path)
        self._init_db()
        self._load_existing()

    def _init_db(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
        """)
        self.conn.commit()

    def _normalize(self, emb: np.ndarray):
        norm = np.linalg.norm(emb, axis=1, keepdims=True)
        return emb / (norm + 1e-10)

    def _load_existing(self):
        rows = self.conn.execute("SELECT id, question FROM memory").fetchall()
        for _id, q in rows:
            emb = self.model.encode([q]).astype("float32")
            emb = self._normalize(emb)
            self.index.add(emb)
            self.id_map.append(_id)

    def add(self, question: str, answer: str):
        emb = self.model.encode([question]).astype("float32")
        emb = self._normalize(emb)
        self.index.add(emb)

        self.conn.execute(
            "INSERT INTO memory (question, answer) VALUES (?, ?)",
            (question, answer)
        )
        self.conn.commit()

        self.id_map.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])

    def search(self, query: str, k=1):
        if self.index.ntotal == 0:
            return None

        q_emb = self.model.encode([query]).astype("float32")
        q_emb = self._normalize(q_emb)

        # cosine similarity scores
        sim, indices = self.index.search(q_emb, k)
        idx = indices[0][0]
        score = float(sim[0][0])

        db_id = self.id_map[idx]
        row = self.conn.execute(
            "SELECT answer FROM memory WHERE id=?",
            (db_id,)
        ).fetchone()

        if row:
            return score, row[0]
        return None
