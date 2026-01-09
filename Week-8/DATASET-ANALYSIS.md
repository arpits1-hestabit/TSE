# Week-8 Dataset Processing Summary

## Overview
Dataset processing pipeline for Code Alpaca (20K instruction-output pairs) and 
---

## File Summaries

### 1. `convert_jsonl.py` - Format Conversion
**Purpose**: Convert JSON array format to JSONL (one record per line)

 - It will read the data and writes each sample as single JSON line and save it to `code_alpaca_20k.jsonl`

### 2. `instruction_dataset.py` - Task Generation & Splitting
**Purpose**: Generate diverse task types and create train/validation splits

**Configuration**:
- Total samples: 4,000
- Train/Val ratio: 90/10 split
- Random seed: 42 (reproducible)

**Task Types Generated**:
| Type | Count | Description |
|------|-------|-------------|
| **QA** | 1,600 | Direct code generation (instruction → output) |
| **Reasoning** | 1,400 | Code explanation tasks |
| **Extraction** | 1,000 | Function signature extraction |


**Outputs**:
- `train.jsonl`: 3,600 training samples
- `val.jsonl`: 400 validation samples

---

### 3. `data_cleaner.py`
**Purpose**: Filter low-quality samples and add token statistics

**Configuration**:
- Max tokens per sample: 2,000
- Tokenizer: `tiktoken` with `cl100k_base` encoding.
  - Used this embedding model as it is safe for instruction and coding models.

**Filtering Criteria**:
1. Total tokens ≤ 2,000 (prevents overly long samples)
2. Instruction tokens > 0 (ensures clear task specification)
3. Output tokens > 0 (ensures complete examples)


**Outputs**:
- `train_clean.jsonl`: Filtered training data (ready for model training)
- `Attachments/token_length_distribution.png`: Histogram of token distribution

