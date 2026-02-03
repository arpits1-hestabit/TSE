# ✅ User Question:
design a rag pipeline for 50k documents

# ✅ Final Answer (Reporter Output)

## Retrieval‑Augmented Generation (RAG) Pipeline for ≈ 50 k Documents  
*A production‑ready design that balances semantic quality, latency, cost and operational simplicity.*

---  

### 1️⃣  High‑Level Architecture  

| Stage | Goal | Recommended Implementation (single‑node start) | Why it fits 50 k docs |
|-------|------|-----------------------------------------------|-----------------------|
| **1. Ingestion & Raw Store** | Pull files from source systems, keep an immutable copy | Object store (AWS S3, GCS, Azure Blob) – folder hierarchy mirrors source | Cheap, durable, easy versioning |
| **2. Pre‑processing & Chunking** | Convert to text, split into LLM‑friendly pieces, extract metadata | `langchain.document_loaders` → `RecursiveCharacterTextSplitter` (200‑400 tokens, 30‑50 token overlap) | Produces ~5‑8 k chunks for 50 k docs → < 1 M vectors, still small enough for a single GPU/CPU |
| **3. Embedding Generation** | Produce dense semantic vectors | • Sentence‑Transformers `all‑mpnet‑base‑v2` (384‑dim) **or** OpenAI `text‑embedding‑3‑large` (1536‑dim) <br> • Batch on a single GPU or multi‑core CPU (≈ 5 min total) | High recall, low cost; a single GPU can embed the whole corpus in < 5 min |
| **4. Vector Store / Index** | Fast Approx‑Nearest‑Neighbour (ANN) search with optional metadata filters | **FAISS** (IVF‑HNSW + PQ/OPQ, float16) – in‑process for prototyping <br> **Milvus / Qdrant / Pinecone** for managed scaling | 50 k × 384 ≈ 7 MB (float32) → fits comfortably in RAM; FAISS gives sub‑ms latency |
| **5. Retrieval Service** | Answer a user query with top‑k relevant chunks | API layer (FastAPI / Flask) → query normaliser → embed query with same model → FAISS `search(k)` → optional metadata filter | Keeps latency < 30 ms for the ANN step |
| **6. Context Assembly & Re‑ranking** | Order/condense retrieved chunks for LLM prompt | Simple concatenation + length check **or** cross‑encoder re‑ranker (e.g., `cross‑encoder/ms‑marco-MiniLM-L-6-v2`) | Improves relevance without heavy compute |
| **7. LLM Generation** | Produce the final answer | • OpenAI `gpt‑4‑turbo` (API) **or** locally hosted Llama‑2‑70B via **vLLM** / **llama.cpp** <br> Prompt template: *“Answer the question using only the following context. If the answer is not present, say you don’t know.”* | Keeps token budget < 4 k (chunks + question + system prompt) |
| **8. Post‑processing & Return** | Clean up response, add citations, log metrics | Add source IDs, confidence scores, store request/response in a log DB (PostgreSQL / DynamoDB) | Enables monitoring, auditability, feedback loops |

> **Diagram (Mermaid)**  

```mermaid
flowchart TD
    subgraph Ingestion
        A[Document Connectors] --> B[Raw Store (S3)]
    end
    subgraph Preprocess
        B --> C[Chunker & Normaliser]
        C --> D[Metadata Extractor]
        D --> E[Chunk Store (Parquet/JSON)]
    end
    subgraph Embedding
        E --> F[Batch Embedder (GPU/CPU workers)]
        F --> G[Vector Store (FAISS / Milvus / Pinecone)]
    end
    subgraph Retrieval
        H[User Query] --> I[Query Normaliser]
        I --> J[Query Embedder (same model as F)]
        J --> K[ANN Search + Metadata Filters]
        K --> L[Top‑k Chunk IDs]
    end
    subgraph Generation
        L --> M[Context Assembler]
        M --> N[Prompt Builder]
        N --> O[LLM Inference (OpenAI / vLLM / Llama.cpp)]
        O --> P[Post‑process (citations, logging)]
        P --> Q[Answer to User]
    end
```

---  

### 2️⃣  Detailed Component Choices  

| Component | Library / Service | Key Settings | Production Tips |
|-----------|-------------------|--------------|-----------------|
| **Loaders** | `langchain.document_loaders` (DirectoryLoader, PDFMinerLoader, TextLoader) | Detect mime‑type, store original path as metadata | Parallelise with `ThreadPoolExecutor` for I/O bound files |
| **Chunker** | `RecursiveCharacterTextSplitter` | chunk_size = 300 tokens, chunk_overlap = 40 tokens | Adjust size to stay ≤ 4 k tokens when combined with prompt |
| **Embedding Model** | • HF `sentence‑transformers/all‑mpnet‑base‑v2` (384‑dim) <br> • OpenAI `text‑embedding‑3‑large` (1536‑dim) | batch_size = 64, dtype = float16 | Cache model on GPU; for OpenAI, batch calls to stay within rate limits |
| **Vector Index** | FAISS `IndexIVFPQ` (or `IndexIVFFlat` + HNSW) | nlist ≈ 256, m = 8 (PQ), use `faiss.IndexIVFPQ` with `faiss.METRIC_INNER_PRODUCT` | Store index on SSD; keep a RAM‑resident “live” copy of hot shards |
| **Retriever API** | FastAPI + `uvicorn` workers = 4‑8 | async endpoint, request timeout = 2 s | Deploy behind an API‑gateway (ALB, Cloud‑Run) for auto‑scaling |
| **Re‑ranker (optional)** | `cross‑encoder/ms‑marco‑MiniLM‑L‑6‑v2` | top‑k = 20 → re‑rank → final k = 5 | Improves precision for ambiguous queries, adds ~10 ms latency |
| **LLM Backend** | • OpenAI `gpt‑4‑turbo` (API) <br> • vLLM (GPU) <br> • llama.cpp (CPU) | temperature = 0.0, max_new_tokens = 512 | Choose based on cost vs. latency; for on‑prem, keep the model in 8‑bit to save VRAM |
| **Metadata Store** | PostgreSQL (or DynamoDB) | Table `rag_requests` (id, query, chunks, answer, latency, timestamp) | Enables traceability, A/B testing, and RLHF data collection |

---  

### 3️⃣  Prototype Code (LangChain + FAISS)

```python
# -------------------------------------------------
# 1️⃣  Imports & configuration
# -------------------------------------------------
import os, time, json, pathlib
from typing import List

from langchain.document_loaders import DirectoryLoader, TextLoader, PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI, HuggingFacePipeline
from langchain.chains import RetrievalQA

# -----------------------------------------------------------------
# 2️⃣  Ingestion & chunking (re‑usable functions)
# -----------------------------------------------------------------
def load_documents(root: str) -> List:
    """Walk a folder and load supported files into LangChain Document objects."""
    loaders = {
        ".txt": TextLoader,
        ".pdf": PDFMinerLoader,
        # add more extensions as needed
    }

    docs = []
    for path in pathlib.Path(root).rglob("*"):
        if path.suffix.lower() in loaders:
            loader = loaders[path.suffix.lower()](str(path))
            docs.extend(loader.load())
    return docs


def chunk_documents(docs, chunk_size=300, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)


# -----------------------------------------------------------------
# 3️⃣  Embedding & vector store creation
# -----------------------------------------------------------------
def build_faiss_store(chunks, embedding_model="all-mpnet-base-v2"):
    embedder = HuggingFaceEmbeddings(model_name=embedding_model,
                                     model_kwargs={"device": "cuda"})  # or "cpu"
    # FAISS will automatically convert to numpy float32 vectors
    vectorstore = FAISS.from_documents(chunks, embedder)
    return vectorstore


# -----------------------------------------------------------------
# 4️⃣  Retrieval‑augmented QA chain
# -----------------------------------------------------------------
def get_qa_chain(vectorstore, llm_name="gpt-4-turbo"):
    # LLM – you can swap OpenAI ↔ HuggingFacePipeline
    llm = OpenAI(model_name=llm_name, temperature=0.0, max_tokens=512)

    # RetrievalQA combines retriever + prompt template
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",          # "map_rerank" if you have a re‑ranker
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True,
    )
    return qa


# -----------------------------------------------------------------
# 5️⃣  End‑to‑end orchestration (run once or on a schedule)
# -----------------------------------------------------------------
if __name__ == "__main__":
    ROOT_DIR = "data/corpus"
    print("🔎 Loading documents …")
    docs = load_documents(ROOT_DIR)

    print(f"📄 {len(docs)} raw docs → chunking")
    chunks = chunk_documents(docs)
    print(f"🧩 Produced {len(chunks)} chunks")

    print("🔗 Building FAISS index …")
    start = time.time()
    store = build_faiss_store(chunks)
    print(f"✅ Index built in {time.time() - start:.1f}s")

    # Persist for later reuse
    store.save_local("faiss_index")

    # Example query
    qa = get_qa_chain(store)
    resp = qa({"query": "What are the main challenges of scaling micro‑services?"})
    print("\n--- Answer ------------------------------------------------")
    print(resp["result"])
    print("\n--- Sources ----------------------------------------------")
    for src in resp["source_documents"]:
        print(f"- {src.metadata.get('source', 'unknown')} (score N/A)")
```

*The script is intentionally modular – swap any component (loader, embedder, vector store, LLM) without touching the others.*  

---  

### 4️⃣  Optimisation & Scaling Guide  

| Aspect | Immediate “quick win” (single‑node) | Mid‑term (distributed) |
|--------|-------------------------------------|------------------------|
| **Embedding throughput** | Use **FAISS‑GPU** or batch on a single RTX‑3090/4090; enable `torch.backends.cudnn.benchmark=True`. | Deploy an **embedding service** (Ray Serve / FastAPI) behind a load‑balancer; scale horizontally. |
| **Vector‑store memory** | Store vectors as **float16** (`faiss.IndexIVFPQ(..., metric=faiss.METRIC_INNER_PRODUCT)` with `faiss.downcast_index`). Use on‑disk IVF (load only hot lists). | Switch to a **sharded Milvus/Qdrant cluster**; keep hot shards in RAM, cold shards on SSD. |
| **Query latency** | Pre‑load the FAISS index in a long‑running process; warm‑up the first few queries. | Deploy vector store as a **micro‑service** with built‑in caching (Redis) and horizontal autoscaling. |
| **LLM cost/latency** | Prefer **OpenAI `gpt‑4‑turbo`** for low latency & pay‑as‑you‑go. | Host **Llama‑2‑70B** via **vLLM** on multi‑GPU nodes; use 8‑bit quantisation to halve VRAM. |
| **Throughput** | Run the FastAPI service with `uvicorn --workers 4`. | Kubernetes HPA / Cloud Run autoscaling; split retrieval (FAISS) and generation pods. |
| **Monitoring** | Emit Prometheus metrics (embed‑time, query‑latency, LLM‑tokens). | Add Grafana dashboards, alert on 95‑th percentile latency > 1 s. |

> **Rule of thumb for 50 k docs**: the entire vector set (384 dim × 50 k ≈ 7 MB) comfortably fits in RAM, so a single‑node FAISS index is **sufficient** for production‑grade latency (< 30 ms). Move to a distributed store only when you exceed ~200 k–500 k docs or need multi‑region redundancy.  

---  

### 5️⃣  Validation & Test Suite  

| Test Pillar | What to verify | Example pytest implementation |
|-------------|----------------|------------------------------|
| **Retrieval correctness** | Top‑k chunks contain the expected ground‑truth passage. | ```python def test_retrieval_accuracy(rag_store, gold_set): ids = rag_store.as_retriever().get_relevant_documents(gold_set.query) assert recall_at_k(ids, gold_set.relevant_ids, k=5) >= 0.8 ``` |
| **Generation relevance** | LLM answer matches reference (Exact‑Match / ROUGE‑L) or passes human review. | ```python def test_answer_quality(qa_chain, test_cases): out = qa_chain({"query": test_cases[i].question}) assert rouge_l(out["result"], test_cases[i].reference) > 0.7 ``` |
| **Performance** | End‑to‑end latency ≤ 2 s (CPU) / ≤ 0.7 s (GPU) under concurrent load. | Use `locust` or `hey` to fire 30 QPS for 60 s; assert `mean_latency < 0.7`. |
| **Scalability** | Adding new documents does not degrade query latency beyond a set threshold. | Incrementally `add_documents` to FAISS, measure `search_time`; ensure < 5 % increase per 10 k docs. |
| **Robustness** | Empty/long queries, special characters, or missing chunks are handled gracefully. | Parametrised tests for edge‑case queries; expect a *“I don’t know”* fallback. |

All tests can live under `tests/` and be run with `pytest -m "rag"` as part of CI/CD.

---  

### 6️⃣  Operational Checklist (What to ship & monitor)

| Category | Item | Recommended Tool |
|----------|------|------------------|
| **Infrastructure** | • GPU/CPU nodes with enough RAM (≥ 16 GB) <br> • Persistent storage for raw docs & FAISS index | Terraform / CloudFormation, EC2 / GKE |
| **Security** | • IAM policies limiting access to S3 bucket & vector store <br> • API keys for LLM services stored in secret manager | AWS IAM, GCP Secret Manager |
| **Observability** | • Prometheus metrics: embed_time, search_latency, llm_latency, error_rate <br> • Logs: request_id, source_chunk_ids, generation timestamps | Grafana, Loki, CloudWatch |
| **CI/CD** | • Unit & integration tests (above) <br> • Docker image build, push to registry, automated rollout | GitHub Actions, Argo CD |
| **Data Governance** | • Metadata schema (source, timestamp, tags) <br> • Retention policy for raw docs & embeddings | Glue / BigQuery catalog |
| **Disaster Recovery** | • Regular snapshot of S3 bucket and FAISS index <br> • Can rebuild index from raw docs in ≤ 30 min | Backup scripts, cron jobs |

---  

### 7️⃣  Roadmap (Beyond 50 k)  

| Milestone | Trigger | Action |
|-----------|---------|--------|
| **M0 – MVP** | ≤ 50 k docs, single‑node budget | Use the prototype code, FAISS on a modest VM (e.g., `c5.xlarge` + `g4dn.xlarge`). |
| **M1 – Scale to 200 k** | Vector size > 30 MB, RAM pressure > 70 % | Move to **FAISS‑GPU** or **Milvus** with sharding; keep hot shards in memory. |
| **M2 – Multi‑region HA** | Need for geo‑redundancy / low latency worldwide | Deploy vector store in a managed SaaS (Pinecone / Qdrant Cloud) and expose via regional API Gateways. |
| **M3 – Real‑time Updates** | Continuous document ingestion (e.g., new tickets) | Implement an **incremental indexing pipeline** (add‑only to FAISS or Milvus) + change‑data‑capture from source system. |
| **M4 – Rerank + Feedback Loop** | Low retrieval precision on niche queries | Add cross‑encoder reranker, store user‑feedback, periodically fine‑tune the embedding model. |

---  

## 📦  TL;DR Summary  

1. **Ingest → Chunk → Embed → Index (FAISS)**  
2. Serve **ANN search** via a FastAPI endpoint; retrieve top‑5 chunks.  
3. Assemble context, prompt an LLM (OpenAI or local) and return answer with citations.  
4. For 50 k documents the whole pipeline runs on a **single VM** (CPU + GPU optional) with **sub‑second latency** and **minimal cost**.  
5. Use the provided modular Python prototype to get started, then follow the optimisation table to scale to larger corpora or stricter SLAs.  

Feel free to copy the code, adapt the tech choices, and integrate the test suite and monitoring checklist into your CI/CD pipeline. Good luck building your RAG system!