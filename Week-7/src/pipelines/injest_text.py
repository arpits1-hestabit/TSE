import json
import faiss
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM

# ---------------- Paths ----------------
INDEX_FILE = "src/vectorstore/index.faiss"
META_FILE = "src/vectorstore/index_meta.json"
CHUNKS_FILE = "src/data/chunks/text_chunks.jsonl"

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
TOP_K = 5


class QueryEngine:
    def __init__(self):
        # ---------- FAISS ----------
        self.index = faiss.read_index(INDEX_FILE)
        print(f"✔ FAISS loaded ({self.index.ntotal} vectors)")

        with open(META_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.ids = meta["ids"]

        # ---------- Chunk text ----------
        self.chunk_text = {}
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                self.chunk_text[r["chunk_id"]] = r["text"]

        # ---------- Embeddings ----------
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embedder = SentenceTransformer(EMBED_MODEL, device=device)

        # ---------- Local Mistral ----------
        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )

        print("✔ Embeddings + Mistral loaded")

    # ---------- Retrieval ----------
    def retrieve(self, query, top_k=TOP_K):
        q_emb = self.embedder.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        _, indices = self.index.search(q_emb, top_k)

        contexts = []
        for idx in indices[0]:
            cid = self.ids[idx]
            contexts.append(self.chunk_text.get(cid, ""))

        return contexts

    # ---------- Prompt ----------
    def build_prompt(self, query, contexts):
        context_block = "\n\n---\n\n".join(contexts)

        return f"""<s>[INST]
You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context_block}

Question:
{query}
[/INST]
"""

    # ---------- Generate ----------
    def answer(self, query):
        contexts = self.retrieve(query)
        prompt = self.build_prompt(query, contexts)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.2,
                do_sample=True
            )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return response.split("[/INST]")[-1].strip()


# ---------- CLI ----------
if __name__ == "__main__":
    engine = QueryEngine()

    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break

        print("\n🧠 Answer:\n")
        print(engine.answer(q))
