import json
import faiss
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer

class HybridRetriever:
    def __init__(self, index_path, meta_path, chunks_path):
        self.index = faiss.read_index(index_path)
        self.embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")

        with open(meta_path) as f:
            meta = json.load(f)

        self.ids = meta["ids"]
        self.metadatas = meta["metadatas"]

        self.text = {}
        with open(chunks_path) as f:
            for line in f:
                r = json.loads(line)
                self.text[r["chunk_id"]] = r["text"]

    def keyword_search(self, query):
        results = []
        for cid, text in self.text.items():
            if query.lower() in text.lower():
                results.append(cid)
        return results

    def semantic_search(self, query, k=20):
        emb = self.embedder.encode([query], normalize_embeddings=True)
        _, idxs = self.index.search(emb, k)
        return [self.ids[i] for i in idxs[0]]

    def rrf(self, rankings, k=60):
        scores = defaultdict(float)
        for rank_list in rankings:
            for rank, cid in enumerate(rank_list):
                scores[cid] += 1 / (k + rank + 1)
        return scores

    def retrieve(self, query, top_k=10):
        sem = self.semantic_search(query)
        key = self.keyword_search(query)

        rrf_scores = self.rrf([sem, key])

        results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        docs = []
        for cid, score in results[:top_k]:
            docs.append({
                "chunk_id": cid,
                "text": self.text[cid],
                "metadata": {},
                "rrf_score": score
            })

        return docs
