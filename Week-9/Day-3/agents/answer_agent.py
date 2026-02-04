from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.memory import ListMemory
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
 
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

answer_memory = ListMemory()

answer_agent = AssistantAgent(
    name="answer_agent",
    description="Answer Agent: produce final answer only.",
    system_message=(
        "You are an Answer Agent.\n"
        "Generate the final answer based ONLY on the summary provided."
    ),
    model_client=model_client,
    memory=[answer_memory]
)
 
answer_agent_tool = AgentTool(answer_agent, return_value_as_last_message=True)


