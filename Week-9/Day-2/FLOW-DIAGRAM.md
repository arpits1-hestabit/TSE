# Multi-Agent Orchestration System Flow Diagram
The diagrams uses ASCII art to visualize the agent interactions, message passing, and the overall workflow from receiving a user task to returning the final validated result.

Key sections included:

- System architecture overview
- Main execution flow with the Orchestrator/Planner
- Layer-by-layer parallel worker execution
- Worker agent processing details
- Reflection phase for combining outputs
- Validation phase with error handling
- Message type data flow
- Complete flow summary
## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN ENTRY POINT                        │
│                          (main.py)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Initialize Runtime & Agents
                             ▼
                    ┌────────────────────┐
                    │  Agent Registry    │
                    ├────────────────────┤
                    │ • WorkerAgent      │
                    │ • ReflectionAgent   │
                    │ • ValidatorAgent   │
                    │ • OrchestratorAgent│
                    └────────┬───────────┘
                             │
                             │ Send UserTask
                             ▼
```

## Main Execution Flow

```
                    ┌──────────────────────┐
                    │   UserTask Message   │
                    │   task: str          │
                    └──────────┬───────────┘
                               │
                               ▼
        ╔══════════════════════════════════════════════╗
        ║        ORCHESTRATOR AGENT (Planner)          ║
        ║         orchestrator/planner.py              ║
        ╚══════════════════════════════════════════════╝
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
    ┌───────────────────────┐    ┌──────────────────────┐
    │ 1. Create Execution   │    │ LLM analyzes task    │
    │    Plan via LLM       │───▶│ complexity & returns │
    │                       │    │ JSON execution plan  │
    └───────────┬───────────┘    └──────────────────────┘
                │
                │ Parsing Result
                ▼
    ┌────────────────────────────────────┐
    │  Execution Plan Structure:         │
    │  {                                 │
    │    "layers": [                     │
    │      ["w1", "w2"],  // Layer 0     │
    │      ["w3"]         // Layer 1     │
    │    ]                               │
    │  }                                 │
    └────────────┬───────────────────────┘
                 │
                 │ Fallback: [["w1","w2"],["w3"]] if parsing fails
                 ▼
```

## Layer Execution (Parallel Workers)

```
    ╔═══════════════════════════════════════════════════╗
    ║          LAYER-BY-LAYER EXECUTION                 ║
    ╚═══════════════════════════════════════════════════╝
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    ┌─────────┐                     ┌─────────┐
    │ Layer 0 │                     │ Layer N │
    └────┬────┘                     └────┬────┘
         │                               │
    ┌────┴─────────────┐                 │
    │ Parallel Workers │                 │
    └────┬─────────────┘                 │
         │                               │
    ┌────┴────┬─────────┐                │
    │         │         │                │
    ▼         ▼         ▼                ▼
┌───────┐ ┌───────┐ ┌───────┐      ┌──────────┐
│Worker │ │Worker │ │Worker │ ───▶ │ Results  │
│  w1   │ │  w2   │ │  wN   │      │Aggregated│
└───────┘ └───────┘ └───────┘      └────┬─────┘
                                         │
                                         │ previous_results[]
                                         │ passed to next layer
                                         ▼
```

## Worker Agent Details

```
        ╔════════════════════════════════════════╗
        ║         WORKER AGENT PROCESS           ║
        ║         (worker_agent.py)              ║
        ╚════════════════════════════════════════╝
                         │
                         │ Receives WorkerTask
                         ▼
            ┌─────────────────────────┐
            │   WorkerTask Message    │
            ├─────────────────────────┤
            │ • task: str             │
            │ • previous_results: []  │
            └────────┬────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Build System Prompt:       │
        │ • Answer in English only   │
        │ • Keep short and clear     │
        │ • Use previous results     │
        │   (if available)           │
        └────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────────────────┐
        │   Call LLM via             │
        │   model_client.create()    │
        │   (timeout: 300s)          │
        └────────┬───────────────────┘
                 │
                 ▼
            ┌─────────┐
            │ Result  │
            └─────────┘
```

## Reflection Phase

```
        ╔════════════════════════════════════════╗
        ║        REFLECTION AGENT                ║
        ║         (reflection.py)                 ║
        ╚════════════════════════════════════════╝
                         │
                         │ After all layers complete
                         ▼
            ┌─────────────────────────┐
            │  ReflectionTask Message  │
            ├─────────────────────────┤
            │ • task: str             │
            │ • worker_outputs: []    │
            └────────┬────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Combine worker outputs     │
        │ into clean final answer:    │
        │ • Only English             │
        │ • No new facts             │
        │ • Clear and structured     │
        └────────┬───────────────────┘
                 │
                 ▼
            ┌─────────────┐
            │ Reflected    │
            │   Result    │
            └──────┬──────┘
                   │
                   ▼
```

## Validation Phase

```
        ╔════════════════════════════════════════╗
        ║         VALIDATOR AGENT                ║
        ║          (validator.py)                ║
        ╚════════════════════════════════════════╝
                         │
                         ▼
            ┌─────────────────────────┐
            │  ValidationTask Message │
            ├─────────────────────────┤
            │ • task: str             │
            │ • answer: str           │
            └────────┬────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ LLM validates answer:      │
        │ 1. English only?           │
        │ 2. Correct for task?       │
        │                            │
        │ Returns JSON:              │
        │ {                          │
        │   "is_valid": bool,        │
        │   "feedback": str          │
        │ }                          │
        └────────┬───────────────────┘
                 │
                 ▼
            ┌─────────┐
            │ Valid?  │
            └────┬────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
      [YES]              [NO]
        │                 │
        │                 ▼
        │    ┌────────────────────┐
        │    │ Return error with  │
        │    │ feedback + answer  │
        │    └────────────────────┘
        │
        ▼
    ┌──────────────┐
    │ FinalResult  │
    │   result     │
    └──────────────┘
```

## Message Types (Data Flow)

```
UserTask ──────▶ OrchestratorAgent
                      │
                      ├─▶ WorkerTask ──────▶ WorkerAgent ──▶ WorkerTaskResult
                      │                                              │
                      │    (aggregated across layers) ◀──────────────┘
                      │
                      ├─▶ ReflectionTask ──▶ ReflectionAgent ──▶ ReflectedResult
                      │
                      └─▶ ValidationTask ──▶ ValidatorAgent ──▶ ValidationResult
                                                                      │
                                                                      └─▶ FinalResult
```

## Complete Flow Summary

```
1. User submits task
2. Orchestrator creates execution plan (layers + workers)
3. For each layer:
   - Spawn parallel workers
   - Workers process task with previous layer results
   - Aggregate results
4. Reflection combines all outputs
5. Validator checks final answer
6. Return FinalResult to user
```

## Key Components

- **Runtime**: SingleThreadedAgentRuntime (autogen_core)
- **Model**: Ollama LLM (configurable: qwen3:8b)
- **Communication**: Message-based async agent communication
- **Parallelism**: asyncio.gather for concurrent worker execution
- **Error Handling**: Timeouts (300s), JSON parsing fallbacks