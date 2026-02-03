from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.memory import ListMemory
from agents.model_client import get_llama_model
 
answer_memory = ListMemory()

answer_agent = AssistantAgent(
    name="answer_agent",
    description="Answer Agent: produce final answer only.",
    system_message=(
        "You are an Answer Agent.\n"
        "Generate the final answer based ONLY on the summary provided."
    ),
    model_client=get_llama_model(),
    memory=[answer_memory]
)
 
answer_agent_tool = AgentTool(answer_agent, return_value_as_last_message=True)


