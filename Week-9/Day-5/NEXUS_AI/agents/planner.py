import json
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class PlannerAgent:
    """
    Planner agent responsible for decomposing a user query into a structured
    execution plan for the multi-agent system.

    Responsibilities:
    - Analyzes the user's request
    - Breaks the request into smaller, well-defined subtasks
    - Assigns each subtask to the most appropriate agent
    - Produces a machine-readable execution plan in strict JSON format

    This agent acts as the entry point for task orchestration and defines
    the workflow executed by the OrchestratorAgent.
    """

    def __init__(self, model_client):
        """
        Initializes the Planner agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="planner",
            system_message="""
            You are the Planner agent.

            Break the user query into sub tasks and assign correct agents.

            Agents:
            - Researcher
            - Coder
            - Analyst
            - Critic
            - Optimizer
            - Validator
            - Reporter

            RULES:
            - Return ONLY raw JSON
            - No markdown
            - No explanation

            Format:
            {
              "tasks": [
                {"agent": "Researcher", "task": "..."}
              ]
            }
            """,
            model_client=model_client
        )

    async def run(self, query):
        """
        Generates a structured execution plan for a given user query.
        Sends the query to the underlying AssistantAgent and expects a strict
        JSON response describing agent-task assignments.
        """

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=query, source="user")],
            cancellation
        )

        return response.chat_message.content
