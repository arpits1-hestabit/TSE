import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

INDEX_FILE = Path("src/vectorstore/index.faiss")
META_FILE = Path("src/data/chunks/metadata.jsonl")
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
TOP_K = 5

class QueryEngine:
    def __init__(self):
        # FAISS index
        self.index = faiss.read_index(str(INDEX_FILE))

        # metadata
        with open(META_FILE, encoding="utf-8") as f:
            self.metadata = [json.loads(line) for line in f]

        # loading embedding model
        self.model = SentenceTransformer(EMBED_MODEL, device="cpu")

    def search(self, query: str, top_k: int = TOP_K):
        # embedding generation for the model
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        ).astype("float32")

        query_embedding = np.array([query_embedding])

        # FAISS search
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = self.metadata[idx]
            results.append({
                "score": float(score),
                "chunk_id": chunk.get("chunk_id"),
                "text": chunk.get("text", ""),
                "metadata": chunk.get("metadata", {})
            })

        return results


# CLI
if __name__ == "__main__":
    engine = QueryEngine()

    while True:
        query = input("\nEnter your query (or 'exit'): ")
        if query.lower() == "exit":
            break

        results = engine.search(query)

        print("\nTop Results:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. Chunk ID: {r['chunk_id']}, Score: {r['score']:.4f}")
            print(r["text"][:500])
            print("-" * 60)
