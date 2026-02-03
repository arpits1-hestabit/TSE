from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

class AnalystAgent:
    """
    Analyst agent responsible for evaluating intermediate outputs produced by
    other agents in the system.

    Responsibilities:
    - Reviews agent-generated content for logical correctness
    - Identifies scalability and performance concerns
    - Highlights inefficiencies, edge cases, or flawed assumptions
    - Provides structured analytical feedback to improve solution quality

    This agent does not generate new solutions; instead, it acts as a quality
    control layer focused on technical soundness and robustness.
    """

    def __init__(self, model_client):
        """
        Initializes the Analyst agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="analyst",
            system_message="""
            You are the Analyst agent.
            Analyze output for correctness, scalability, performance.
            """,
            model_client=model_client
        )

    async def run(self, task):
        """
        Analyzes a given task or agent output and returns analytical feedback.
        """

        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=task, source="user")],
            cancellation
        )

        return response.chat_message.content
