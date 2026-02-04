# NEXUS AI

A multi-agent AI system designed for complex problem-solving and analysis across diverse domains.

## Overview

NEXUS AI orchestrates multiple specialized AI agents to collaborate on tasks like business planning, technical design, and strategic analysis. It leverages semantic memory and FAISS vector database for intelligent context retrieval.

## Quick Start

1. **Setup**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Update `.env` with API credentials
   - Configure settings in `config.py`

3. **Run**
   ```bash
   python main.py
   ```

## Features

- **Multi-Agent System**: 9 specialized agents working in coordination
- **Semantic Memory**: FAISS-based vector search for relevant context
- **Structured Logging**: Track system execution and debugging
- **Output Management**: Organized result storage in `outputs/` directory
- **Domain Coverage**: Startups, RAG pipelines, task management, architecture design

## Project Structure

- `agents/`: Individual agent implementations
- `memory_store/`: FAISS vector database
- `logs/`: Execution logs
- `outputs/`: Generated reports and analyses
- `config.py`: System configuration
- `logger.py`: Logging utilities
- `semantic_memory.py`: Memory operations
- `main.py`: Entry point
