# Multi-Agent Tool Chain Orchestration System

**Overview:** A dynamic multi-agent system that orchestrates specialized agents (File, Database, Code Executor) to process complex user queries through automated planning, sequential execution with dependency resolution, and context-aware result aggregation.

**Purpose:** Enables intelligent task decomposition where an orchestrator LLM creates execution plans, routes tasks to appropriate tool-specialized agents, manages data flow between steps, and synthesizes final answers from accumulated context.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN ENTRY POINT                        │
│                          (main.py)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ User Query Input
                             ▼
        ╔══════════════════════════════════════════════╗
        ║           ORCHESTRATION PIPELINE             ║
        ╚══════════════════════════════════════════════╝
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
    ┌───────────────┐              ┌──────────────────┐
    │ 1. Planning   │              │ 2. Summarization │
    │ run_orchestr  │─────────────▶│ summarize_results│
    └───────┬───────┘              └────────┬─────────┘
            │                               │
            │                               ▼
            │                      ┌─────────────────┐
            │                      │ 3. Final Answer │
            │                      │  answer_agent   │
            │                      └─────────────────┘
            ▼
```

## Orchestrator Agent (Planner)

```
        ╔════════════════════════════════════════════╗
        ║         ORCHESTRATOR AGENT                 ║
        ║         (orchestrator.py)                  ║
        ╚════════════════════════════════════════════╝
                         │
                         │ Receives User Query
                         ▼
            ┌─────────────────────────┐
            │ LLM Plans Execution     │
            │ (Structured Output)     │
            │                         │
            │ Returns ExecutionPlan:  │
            │ {                       │
            │   "steps": [            │
            │     {                   │
            │       "agent": "file",   │
            │       "task": "...",    │
            │       "input_keys": [], │
            │       "output_key": "x" │
            │     }                   │
            │   ]                     │
            │ }                       │
            └────────┬────────────────┘
                     │
                     │ Parse Plan
                     ▼
        ┌────────────────────────────┐
        │ Execute Steps Sequentially │
        │ with Dependency Resolution │
        └────────┬───────────────────┘
                 │
                 ▼
```

## Available Agent Types

```
    ╔═══════════════════════════════════════════════════╗
    ║              SPECIALIZED AGENTS                   ║
    ╚═══════════════════════════════════════════════════╝
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │  FILE   │    │    DB    │    │   CODE   │
    │  AGENT  │    │  AGENT   │    │ EXECUTOR │
    └────┬────┘    └────┬─────┘    └────┬─────┘
         │              │               │
         ▼              ▼               ▼
```

## 1. File Agent (file_agent.py)

```
        ╔════════════════════════════════════════╗
        ║            FILE AGENT                  ║
        ╚════════════════════════════════════════╝
                         │
                         │ Uses FileSurfer Tool
                         ▼
            ┌─────────────────────────┐
            │   FileSurfer Agent      │
            │   - base_path:          │
            │     ./executed_code     │
            │   - Navigates & finds    │
            │     file locations       │
            └────────┬────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Returns:                   │
        │ Absolute file paths         │
        │ in executed_code directory │
        └────────────────────────────┘
```

## 2. Database Agent (db_agent.py)

```
        ╔════════════════════════════════════════╗
        ║          DATABASE AGENT                ║
        ║         (SQLite Tools)                 ║
        ╚════════════════════════════════════════╝
                         │
                         │ Three Tools Available
                         ▼
        ┌────────────────────────────┐
        │ 1. list_tables()           │
        │    - Lists all tables      │
        │    - Payload: {}           │
        └────────┬───────────────────┘
                 │
        ┌────────┴───────────────────┐
        │ 2. inspect_schema()        │
        │    - Get table structure   │
        │    - Payload:              │
        │      {"tables": ["x"]}     │
        └────────┬───────────────────┘
                 │
        ┌────────┴───────────────────┐
        │ 3. execute_query()         │
        │    - Run SQL queries       │
        │    - Payload:              │
        │      {"sql": "SELECT...",  │
        │       "allow_write": bool} │
        └────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────────────────┐
        │ Security Constraints:      │
        │ • SELECT requires LIMIT    │
        │ • Only INSERT allowed      │
        │ • No UPDATE/DELETE/DDL     │
        │ • Pattern validation       │
        └────────────────────────────┘
```

## 3. Code Executor (code_executor.py)

```
        ╔════════════════════════════════════════╗
        ║          CODE EXECUTOR                 ║
        ╚════════════════════════════════════════╝
                         │
                         │ Creates Python Scripts
                         ▼
            ┌─────────────────────────┐
            │ LocalCommandLineCodeExec│
            │ - work_dir:             │
            │   ./executed_code       │
            │ - timeout: 600s         │
            └────────┬────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ PythonCodeExecutionTool    │
        │ - Writes SOURCE CODE       │
        │ - Executes scripts         │
        │ - Captures output          │
        └────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────────────────┐
        │ Returns:                   │
        │ ToolCallSummaryMessage     │
        │ containing execution result│
        └────────────────────────────┘
```

## Execution Flow

```
        ╔════════════════════════════════════════╗
        ║        ORCHESTRATION EXECUTION         ║
        ╚════════════════════════════════════════╝

User Query ──▶ Orchestrator Agent
                      │
                      ▼
              ┌───────────────┐
              │ Generate Plan │
              │ (JSON Schema) │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ For Each Step │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
      [FILE]         [DB]         [CODE]
        │             │             │
        │    ┌────────┴────────┐    │
        │    │  Build Context  │    │
        │    │  from previous  │    │
        │    │  step outputs   │    │
        │    └────────┬────────┘    │
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Store Result  │
              │ in Context    │
              │ Dict with     │
              │ output_key    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ All Steps Done│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Summarize    │
              │   Results     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Answer Agent  │
              │ Final Output  │
              └───────────────┘
```

## Data Flow & Context Management

```
context: Dict[str, any] = {}

Step 1: file_agent
  ├─ output_key: "file_path"
  └─ context["file_path"] = "/path/to/sales.csv"

Step 2: db_agent
  ├─ input_keys: ["file_path"]
  ├─ task + context from Step 1
  ├─ output_key: "query_result"
  └─ context["query_result"] = {...}

Step 3: code_executor
  ├─ input_keys: ["query_result"]
  ├─ task + context from Step 2
  ├─ output_key: "analysis"
  └─ context["analysis"] = "..."

Final Context:
{
  "file_path": "...",
  "query_result": {...},
  "analysis": "..."
}
```

## Answer Agent (answer_agent.py)

```
        ╔════════════════════════════════════════╗
        ║           ANSWER AGENT                 ║
        ╚════════════════════════════════════════╝
                         │
                         │ Receives:
                         │ - User Query
                         │ - Summarized Context
                         ▼
            ┌─────────────────────────┐
            │ Generate Final Answer   │
            │ Based ONLY on summary   │
            │ provided                │
            └────────┬────────────────┘
                     │
                     ▼
            ┌─────────────────────────┐
            │ Clean, Final Response   │
            │ to User                 │
            └─────────────────────────┘
```

## Key Components

- **Models**: Groq API (openai/gpt-oss-20b) with function calling
- **Database**: SQLite with CSV import via pandas
- **Code Execution**: Local Python execution with 600s timeout
- **File System**: FileSurfer for ./executed_code directory
- **Memory**: ListMemory for answer agent
- **Orchestration**: Sequential step execution with dependency resolution
- **Security**: SQL validation, forbidden pattern blocking