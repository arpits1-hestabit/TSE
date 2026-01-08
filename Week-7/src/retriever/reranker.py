from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query, docs, top_k=5):
        pairs = [(query, d["text"]) for d in docs]
        scores = self.model.predict(pairs)

        for d, s in zip(docs, scores):
            d["score"] = float(s)

        return sorted(docs, key=lambda x: x["score"], reverse=True)[:top_k]
