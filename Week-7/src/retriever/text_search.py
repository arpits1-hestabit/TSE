from sentence_transformers import SentenceTransformer
import faiss
import json
import os
import numpy as np


class TextSearcher:
    def __init__(self, vector_dir: str):
        self.vector_dir = vector_dir

        self.documents = []

        # FAISS index
        self.index = faiss.read_index(
            os.path.join(vector_dir, "faiss.index")
        )

        # loading jsonl
        with open(
            os.path.join(vector_dir, "text_chunks.jsonl"),
            "r",
            encoding="utf-8"
        ) as f:
            for line in f:
                self.documents.append(json.loads(line))

        # loading embedding model
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            np.array(query_embedding, dtype="float32"),
            top_k
        )

        results = []
        for idx, score in zip(indices[0], scores[0]):
            doc = self.documents[idx].copy()
            doc["score"] = float(score)
            results.append(doc)

        return results
