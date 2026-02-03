from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class OptimizerAgent:
    """
    Optimizer agent responsible for improving the efficiency and design
    of solutions produced by other agents.

    Responsibilities:
    - Enhances performance and reduces latency
    - Refactors designs for better scalability and maintainability
    - Applies best practices and optimization techniques
    - Suggests architectural and implementation-level improvements

    This agent focuses on optimization rather than correctness validation.
    """

    def __init__(self, model_client):
        """
        Initializes the Optimizer agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="optimizer",
            system_message="""
            You are the Optimizer agent.
            Optimize performance, reduce latency, improve design.
            Use best practices.
            """,
            model_client=model_client
        )

    async def run(self, task):
        """
        Optimizes a given task or agent output and returns improvements.
        Sends the content to the underlying AssistantAgent and retrieves
        suggestions focused on performance, design, and efficiency.
        """

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=task, source="user")],
            cancellation
        )

        return response.chat_message.content
