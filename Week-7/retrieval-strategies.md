# Retrieval Strategies

Overview of retrieval methods in the RAG system.

## 1. Semantic Search

**How it works**: Dense vectors capture meaning, FAISS finds similar docs

```python
# Query → BGE embedding → FAISS similarity → Top-K results
query_vec = model.encode(query, normalize=True)
scores, indices = index.search(query_vec, k=20)
```

**Strengths**:
- Understands synonyms and context
- Finds conceptually similar content
- Robust to paraphrasing

**Weaknesses**:
- May miss exact term matches
- Requires quality embeddings

**Use when**: Query is conceptual, needs semantic understanding

## 2. Keyword Search

**How it works**: Case-insensitive substring matching

```python
for chunk_id, text in documents.items():
    if query.lower() in text.lower():
        results.append(chunk_id)
```

**Strengths**:
- Finds exact matches reliably
- Fast and simple
- No model dependency

**Weaknesses**:
- No semantic understanding
- Misses synonyms

**Use when**: Looking for specific terms, codes, identifiers

## 3. Hybrid Retrieval with RRF

**How it works**: Combines semantic + keyword search using Reciprocal Rank Fusion

```python
# Get results from both methods
semantic_results = semantic_search(query, k=20)
keyword_results = keyword_search(query)

# RRF fusion: score = Σ(1 / (k + rank))
def rrf(rankings, k=60):
    scores = defaultdict(float)
    for rank_list in rankings:
        for rank, doc_id in enumerate(rank_list):
            scores[doc_id] += 1 / (k + rank + 1)
    return scores

combined_scores = rrf([semantic_results, keyword_results])
```

**Why RRF?**
- Rank-based (no score normalization needed)
- Proven effective in research
- Easy to add more retrieval methods

**Example**:
```
Query: "Q3 revenue growth"

Semantic ranks: [DocA(1), DocB(2), DocC(3)]
Keyword ranks:  [DocC(1), DocD(2), DocA(3)]

RRF scores (k=60):
- DocA: 1/61 + 1/64 = 0.032
- DocC: 1/63 + 1/61 = 0.032
- DocB: 1/62 = 0.016
- DocD: 1/63 = 0.016

Final ranking: C, A, B, D
```

**Strengths**:
- Best of both worlds
- Robust to individual method failures
- No hyperparameter tuning needed

**Configuration**:
- RRF constant k: 60 (default)
- Semantic top-k: 20
- Final output: 10

## 4. Reranking

**How it works**: Cross-encoder scores query-document pairs for accuracy

```python
# Stage 1: Fast retrieval (hybrid) → 10 results
# Stage 2: Accurate reranking → 5 results

pairs = [(query, doc["text"]) for doc in retrieved_docs]
scores = cross_encoder.predict(pairs)
final_results = top_k_by_score(docs, scores, k=5)
```

**Bi-Encoder vs Cross-Encoder**:
```
Bi-Encoder (Retrieval):     Cross-Encoder (Reranking):
- Separate encodings        - Joint encoding
- Fast (pre-computed)       - Slower (on-demand)
- Good accuracy             - Excellent accuracy
- Can scale to millions     - Limited to hundreds
```

**Model**: `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Strengths**:
- Significant accuracy boost (+15-25% precision)
- Better query-document interaction
- Handles nuanced relevance

**Weaknesses**:
- Slower than bi-encoders (~300-500ms)
- Cannot pre-compute scores

**Use when**: Accuracy is critical, small result set, user-facing

## 5. Image Search

**How it works**: CLIP embeddings for text-to-image search

```python
# Text query → CLIP text encoder → Cosine similarity → Images
query_vec = clip_text_encoder(query)
scores = np.dot(image_embeddings, query_vec)
top_images = argsort(scores)[:k]
```

**Features**:
- Natural language image search
- BLIP captions for metadata
- OCR filtering for text-heavy images

**Example**:
```python
# Find diagrams
results = searcher.search("database architecture diagram")

# Find specific text in images
results = searcher.search(
    "error message",
    ocr_filter="404"
)
```
