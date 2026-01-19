## Overview

The deployment system consists of two main components:
- **FastAPI Backend** (`app.py`) - RESTful API server for RAG operations
- **Streamlit Frontend** (`ui.py`) - Interactive user interface for the RAG Assistant

## Architecture

### Backend (FastAPI)

**File:** [src/deployment/app.py](src/deployment/app.py)

The FastAPI application serves as the core backend providing REST endpoints for three main RAG modes:

#### Endpoints

1. **Text RAG Endpoint: `/ask`** (POST)
   - Accepts a text question
   - Returns answer with context and faithfulness score
   - Uses: `ask_retrieval()` from test suite
   - Evaluates: Faithfulness score via RAGEvaluator

2. **Image RAG Endpoint: `/ask-image`** (POST)
   - Supports three modes:
     - **Image + Question**: Multi-modal retrieval (image_to_text_final)
     - **Image Only**: Image-based search (image_to_image_final)
     - **Question Only**: Text-to-image retrieval (text_to_image_final)
   - Parameters:
     - `question` (optional): Text query
     - `image` (optional): Image file (jpg, png, jpeg)
     - `top_k` (default: 5): Number of results

3. **SQL RAG Endpoint: `/ask-sql`** (POST)
   - Accepts a natural language question about database
   - Generates SQL queries and returns results
   - Uses: SQLPipeline with `sales.db`
   - Returns: Query summary and results

#### Key Components

- **RAG Evaluator**: `RAGEvaluator()` for quality metrics
- **SQL Pipeline**: Integrated database query engine
- **Upload Directory**: `tmp/uploads/` for temporary file storage

#### Dependencies

- FastAPI framework
- Image search modules from retriever package
- SQL Pipeline from pipelines
- RAG evaluation utilities

---

### Frontend (Streamlit)

**File:** [src/deployment/ui.py](src/deployment/ui.py)

Interactive web interface for the RAG Assistant with three operational modes.

#### Operational Modes

1. **Text RAG Mode**
   - Text area for question input
   - Calls `/ask` endpoint
   - Displays: Answer and faithfulness score
   - Timeout: 600 seconds

2. **Image RAG Mode**
   - Optional question input
   - Image file uploader (jpg, png, jpeg)
   - Calls `/ask-image` endpoint
   - Parameters: top_k = 5
   - Displays: Answer and faithfulness score
   - Timeout: 1000 seconds
   - Handles: Image file transmission to backend

3. **SQL RAG Mode**
   - Question input for database queries
   - Calls `/ask-sql` endpoint
   - Displays: Query result summary
   - Specialized for database interaction

---

## Running the Deployment

### Prerequisites

Ensure all dependencies from [requirements.txt](requirements.txt) are installed.

### Start Backend Server

```bash
cd /home/arpitsaxena/Desktop/TSE/Week-7

# Option 1: Development mode with auto-reload
uvicorn src.deployment.app:app --reload

# Option 2: Production mode
uvicorn src.deployment.app:app --host 0.0.0.0 --port 8000
```

**Default:** `http://localhost:8000`

API Documentation available at: `http://localhost:8000/docs`

### Start Frontend Interface

In a separate terminal:

```bash
cd /home/arpitsaxena/Desktop/TSE/Week-7/src/deployment

streamlit run ui.py
```

**Default:** `http://localhost:8501`

### Required Services

- **FastAPI Backend**: Must be running on `http://localhost:8000`
- **Database**: `sales.db` must be available for SQL operations
- **Embedding Models**: CLIP embedder and vector store indices
- **FAISS Index**: Vector search index for retrieval

---

## Data Flow

### Text RAG Flow

```
User Question 
    ↓
Streamlit UI (/ask endpoint)
    ↓
FastAPI Backend (ask_retrieval)
    ↓
Retriever Module (vector search)
    ↓
LLM Generation
    ↓
RAG Evaluator (faithfulness scoring)
    ↓
Response with Score
```

### Image RAG Flow

```
User Input (Image/Question)
    ↓
Streamlit UI (file upload to /ask-image)
    ↓
FastAPI Backend (file saved to tmp/uploads)
    ↓
Image Embedder (CLIP)
    ↓
Multi-modal Retriever (image_to_text_final, etc.)
    ↓
Context Building
    ↓
RAG Evaluator
    ↓
Response
```

### SQL RAG Flow

```
Natural Language Question
    ↓
Streamlit UI (/ask-sql endpoint)
    ↓
SQL Pipeline
    ↓
Query Generation (LLM-based)
    ↓
Database Execution
    ↓
Result Summarization
    ↓
Response
```

---

## Environment Variables

May require configuration:
- `DATABASE_PATH` - Location of sales.db
- `MODEL_PATH` - Path to CLIP model
- `FAISS_INDEX_PATH` - Vector index location
- `API_PORT` - FastAPI port (default: 8000)
- `STREAMLIT_PORT` - Streamlit port (default: 8501)

---
