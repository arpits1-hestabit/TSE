# Memory System Documentation

## Overview
A memory management system built with FAISS vector database and LLM integration for maintaining session-based conversation history and context retrieval.

## Architecture

### Core Components

#### 1. **llm_client.py**
Handles communication with the language model. Manages API calls, request formatting, and response processing for LLM interactions.

#### 2. **vector_store.py**
Manages FAISS vector database operations:
- Stores and retrieves embeddings
- Performs similarity searches
- Indexes conversation embeddings for fast retrieval
- Uses `faiss.index` for persistent storage

#### 3. **session_memory.py**
Maintains conversation state:
- Stores user messages and assistant responses
- Tracks session metadata (timestamps, user info)
- Manages message history within a session
- Provides session retrieval methods

#### 4. **memory_agent.py**
Orchestrates memory operations:
- Coordinates between LLM client and vector store
- Retrieves relevant context from past conversations
- Manages memory updates after each interaction
- Implements retrieval-augmented generation (RAG)

#### 5. **main.py**
Entry point and integration layer:
- Initializes system components
- Handles user input processing
- Orchestrates conversation flow
- Manages session lifecycle

## Key Features

- **Vector Embeddings**: Converts conversations to vectors for semantic search
- **Session Management**: Isolates and manages independent conversation sessions
- **Context Retrieval**: Finds relevant past interactions using similarity search
- **LLM Integration**: Augments responses with retrieved context
- **Persistent Storage**: Saves embeddings and session data via FAISS index

## Configuration

Environment variables are stored in `.env`:
- LLM API credentials
- Vector store settings
- Session management parameters

## Workflow

1. User input received in `main.py`
2. Message embedded and stored in `session_memory.py`
3. Similar past messages retrieved via `vector_store.py`
4. Context passed to `llm_client.py` for response generation
5. Response stored and indexed for future retrieval

## Usage

Initialize and run the memory system through `main.py` with proper environment configuration.