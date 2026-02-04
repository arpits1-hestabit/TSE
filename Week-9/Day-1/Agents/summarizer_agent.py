from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.memory import ListMemory
from model_client import get_llama_model
 
summarizer_memory = ListMemory()

summarizer_agent = AssistantAgent(
    name="summarizer_agent",
    description="Summarizer Agent: summarize research only.",
    system_message=(
        "You are a Summarizer Agent.\n"
        "ONLY summarize the research provided.\n"
        "Do NOT add new info."
    ),
    model_client=get_llama_model(),
    memory=[summarizer_memory]
)

summarizer_agent_tool = AgentTool(summarizer_agent, return_value_as_last_message=True)