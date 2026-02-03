import asyncio
import json

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

from silent_externals import silence_all_logs
from config import GROQ_API_KEY
from logger import setup_logger

# Agent imports
from agents.planner import PlannerAgent
from agents.orchestrator import OrchestratorAgent
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.optimizer import OptimizerAgent
from agents.validator import ValidatorAgent
from agents.reporter import ReporterAgent


# Silence logs from third-party libraries (HTTP clients, SDKs, HuggingFace etc.)
silence_all_logs()

# Configure application-wide logger
logger = setup_logger()


async def main():
    """
    Asynchronous entry point for running the Nexus AI workflow.

    Workflow:
    1. Initialize the LLM client using Groq's OpenAI-compatible API
    2. Create a Planner agent to generate a structured execution plan
    3. Initialize specialized agents (research, coding, analysis, etc.)
    4. Pass all agents to the Orchestrator for coordinated execution
    5. Accept a user task as input
    6. Generate and validate a JSON-based execution plan
    7. Execute the plan step-by-step using the orchestrator
    8. Display final outputs produced by each agent

    This function is designed to be run inside an asyncio event loop.
    """

    # Initialize the LLM client
    model_client = OpenAIChatCompletionClient(
        model="openai/gpt-oss-120b",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model_info=ModelInfo(
            vision=False,
            function_calling=False,
            json_output=True,
            family="groq"
        )
    )

    # Planner agent generates the execution plan
    planner = PlannerAgent(model_client)

    # Dictionary of specialized agents used during execution
    agents = {
        "Researcher": ResearcherAgent(model_client),
        "Coder": CoderAgent(model_client),
        "Analyst": AnalystAgent(model_client),
        "Critic": CriticAgent(model_client),
        "Optimizer": OptimizerAgent(model_client),
        "Validator": ValidatorAgent(model_client),
        "Reporter": ReporterAgent(model_client),
    }

    # Orchestrator controls agent execution order and data flow
    orchestrator = OrchestratorAgent(agents, logger)

    # Accept user input task
    user_question = input("\nEnter your task: ")

    # Generate execution plan
    logger.info("Planner generating execution plan...")
    plan_json = await planner.run(user_question)

    # Abort if planner returns nothing
    if not plan_json:
        logger.error("Planner returned empty plan. Exiting...")
        return

    # Validate that planner output is valid JSON
    try:
        json.loads(plan_json)
    except json.JSONDecodeError:
        logger.error(f"Planner returned invalid JSON:\n{plan_json}")
        return

    logger.info("Plan generated successfully")

    # Execute the plan using the orchestrator
    results = await orchestrator.run(user_question, plan_json)

# Standard async entry-point guard
if __name__ == "__main__":
    asyncio.run(main())
