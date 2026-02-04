from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.memory import ListMemory
from model_client import get_llama_model

# memory
research_memory = ListMemory()

research_agent = AssistantAgent(
    name="research_agent",
    description="Research Agent: gathers facts only.",
    system_message=(
        "You are a Research Agent.\n"
        "You must ONLY research and provide facts.\n"
        "Do NOT summarize or answer."
    ),
    model_client=get_llama_model(),
    memory=[research_memory]
)

research_agent_tool = AgentTool(research_agent, return_value_as_last_message=True)
