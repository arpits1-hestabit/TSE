import asyncio
import os
import json
from typing import Dict, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from file_agent import file_agent
from code_executor import code_executor
from db_agent import db_agent

load_dotenv()
from autogen_ext.models.openai import OpenAIChatCompletionClient

key = os.getenv("GROQ_API_KEY")
model_info = {
    "family": "oss",
    "vision": False,
    "function_calling": True,
    "json_output": True,
    "structured_output": True,
    "context_length": 4096,
}

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=key,
    base_url="https://api.groq.com/openai/v1",
    model_info=model_info,
    parallel_tool_calls=False
)

class PlanStep(BaseModel):
    agent: str
    task: str
    input_keys: List[str] = []
    output_key: str

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]

sys_msg = '''
You act as an orchestration planner.

Your responsibility is to DESIGN an execution plan only.
You are NOT allowed to run tasks, generate code, or compute results.

Your response MUST be valid JSON and MUST strictly conform to the schema below:

ExecutionPlan:
{
  "steps": [
    {
      "agent": "file | db | code",
      "task": "string",
      "input_keys": ["string"],
      "output_key": "string"
    }
  ]
}

All code execution is stateless. Therefore, use at most ONE code agent step.
Do NOT create dependencies between multiple code agent steps.

MANDATORY CONSTRAINTS (NO EXCEPTIONS):

1. Every step MUST include exactly these fields:
   - agent
   - task
   - input_keys
   - output_key

2. Do NOT add any extra fields.
   - No ids
   - No names
   - No parameters
   - No metadata of any form

3. The "task" field MUST be written as a plain English instruction.
   - Do NOT include source code
   - Do NOT include results or outputs
   - Do NOT include reasoning, thoughts, or explanations

4. The "output_key":
   - Must be a concise snake_case identifier
   - Must be unique across all steps
   - Must clearly represent the stored output of that step

5. The "input_keys":
   - Must reference only output_key values from earlier steps
   - Must be an empty list if the step has no dependencies

6. Agent roles are strictly defined:
   - file → discover or locate files
   - db   → execute SQL queries and read from database tables
   - code → perform Python-based data analysis using previous outputs

7. Steps must be ordered strictly by dependency.
   - A step can only depend on outputs produced earlier in the plan

8. Output requirements:
   - Return raw JSON only
   - No explanations
   - No markdown formatting
   - No extra text before or after the JSON
'''

orchestrator = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=(sys_msg),
    output_content_type_format=ExecutionPlan
)

db = db_agent(name="DB_AGENT",model_client=model_client,db_path="executed_code/sales.db")

async def run_orchestration(user_query: str) -> Dict[str, any]:
    plan_result = await orchestrator.run(task=user_query)
    plan_json = plan_result.messages[-1].content
    print(json.loads(plan_json))
    plan = ExecutionPlan.model_validate(json.loads(plan_json))
    context: Dict[str, any] = {}

    for step in plan.steps:
        step_context = {k: context[k] for k in getattr(step, "input_keys", []) if k in context}

        if step.agent == "file":
            output = await file_agent(step.task)
            print(output)
            context[step.output_key] = output

        elif step.agent == "db":
            enriched_task = step.task
            if step_context:
                enriched_task += f"\n\nContext:\n{json.dumps(step_context, indent=2,default=str)}"

            output = await db.run(task=enriched_task)
            context[step.output_key] = output
            print(output)

        elif step.agent == "code":
            enriched_task = step.task
            if step_context:
                enriched_task += f"\n\nContext:\n{json.dumps(step_context, indent=2,default=str)}"

            output = await code_executor(enriched_task)
            context[step.output_key] = output
            print(output)

        else:
            raise ValueError(f"Unknown agent type: {step.agent}")

    return context

def summarize_results(context: Dict[str, any]) -> str:
    return "\n".join(f"{k}: {v}" for k, v in context.items())