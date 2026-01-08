# RAG Architecture

Enterprise RAG system with multimodal retrieval and SQL query capabilities.

## System Overview

```
                User Query
                    ↓
        Query Router (SQL/Text/Image)
                    ↓
┌─────────────┬──────────────┬─────────────┐
│ SQL Pipeline│Text Retrieval│Image Search │
└─────────────┴──────────────┴─────────────┘
    ↓               ↓              ↓
Database         FAISS Index    CLIP Index
    ↓               ↓              ↓
    └───────────────┴──────────────┘
                    ↓
              LLM Generation
                    ↓
            Evaluation (RAGAS)
                    ↓
              Final Answer
```

## Core Components

### 1. Ingestion Pipeline
- **Text**: PDF, TXT, CSV, DOCX → 800-char chunks
- **Images**: JPG, PNG → CLIP embeddings + captions + OCR
- **Output**: JSONL chunks + NumPy embeddings

### 2. Embedding Generation
- **Model**: BAAI/bge-small-en-v1.5 (384-dim)
- **Batch size**: 32
- **Normalization**: L2 normalized for cosine similarity
- **Storage**: FAISS flat index

### 3. Retrieval System

**Hybrid Retrieval** (`hybrid_retriever.py`):
```
Semantic search (top-20) + Keyword search
Combined with RRF (k=60)
Returns top-10 results
```

**Reranking** (`reranker.py`):
```
Cross-encoder: ms-marco-MiniLM-L-6-v2
Refines top-10 to top-5
```

**Image Search** (`image_search.py`):
```
CLIP text-to-image similarity
Optional OCR filtering
```

### 4. Generation
- **LLM**: Qwen2.5-1.5B-Instruct
- **SQL Generation**: Schema-aware, conversation memory
- **Answer Generation**: Context-grounded responses

### 5. Evaluation
- **Framework**: RAGAS
- **Metric**: Faithfulness score
- **Threshold**: <0.7 flags hallucinations

## Data Flow

### Document Processing
```
Raw Docs → Load → Chunk (800/100) → Embed (BGE) → FAISS Index
```

### Image Processing
```
Images → CLIP Embed + BLIP Caption + OCR → Vector Store
```

### Query Processing
```
Query → Hybrid Retrieve (20) → Rerank (5) → Context → LLM → Answer
```

## File Structure

```
src/
├── embeddings/
│   ├── embedder.py          # Text embeddings
│   └── clip_embedder.py     # Image embeddings
├── retriever/
│   ├── hybrid_retriever.py  # Hybrid search + RRF
│   ├── reranker.py          # Cross-encoder reranking
│   ├── image_search.py      # CLIP-based search
│   └── text_search.py       # Basic vector search
├── generator/
│   └── sql_generator.py     # Text-to-SQL
├── pipelines/
│   ├── injest.py            # Text ingestion
│   ├── image_injest.py      # Image ingestion
│   ├── sql_pipeline.py      # SQL workflow
│   └── context_builder.py   # Context formatting
├── evaluation/
│   └── rag_eval.py          # RAGAS evaluation
├── memory/
│   └── memory_store.py      # Conversation memory
└── vectorstore/
    ├── index.faiss          # Text vectors
    └── images/              # Image vectors
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| Vector DB | FAISS |
| Embeddings | BGE-small, CLIP |
| LLM | Qwen2.5-1.5B |
| Reranking | Cross-Encoder |
| Vision | CLIP, BLIP |
| OCR | Tesseract |
| Memory | LangChain |
| Evaluation | RAGAS |
| Database | SQLite |

## Key Features

1. **Hybrid Retrieval**: Semantic + keyword search with RRF fusion
2. **Multimodal**: Text and image search in unified system
3. **SQL QA**: Natural language to SQL with error recovery
4. **Evaluation**: Built-in faithfulness scoring
5. **Memory**: Conversation context for follow-ups
6. **Reranking**: Cross-encoder for accuracy boost
