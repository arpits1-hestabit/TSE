# Agent Fundamentals

### Components

1. **Answer Agent** (`answer_agent.py`)
   - Responsible for generating answers based on user queries
   - Integrates with the language model for response generation

2. **Research Agent** (`research_agent.py`)
   - Conducts research and information gathering
   - Processes and analyzes retrieved information

3. **Summarizer Agent** (`summarizer_agent.py`)
   - Summarizes complex information into concise outputs
   - Distills key insights from research findings

4. **Model Client** (`model_client.py`)
   - Manages communication with the language model
   - Handles model initialization and API calls

### Pipeline
- Main orchestration happens in `pipelines/main.py`
- Coordinates agent interactions and workflow execution
```
User → Research Agent → Info
Research Agent → Summarizer Agent → Summary
Summarizer Agent → Answer Agent → Final Answer
```

## Model Configuration
- **Model**: Qwen 2.5 Coder 7B Instruct (Q4_K_M quantized)
- **Location**: `models/qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- **Type**: Quantized GGUF format for efficient inference

## Dependencies
See `requirements.txt` for all project dependencies.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure the model file exists in the `models/` directory
3. Run the pipeline: `python pipelines/main.py`

## Key Concepts
- **Multi-Agent System**: Multiple specialized agents working together
- **LLM Integration**: Agents powered by local language models
- **Task Delegation**: Each agent handles specific responsibilities
- **Workflow Orchestration**: Coordinated execution of agent tasks