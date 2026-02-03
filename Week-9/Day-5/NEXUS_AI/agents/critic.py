from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class CriticAgent:
    """
    Critic agent responsible for identifying weaknesses, risks, and gaps
    in solutions produced by other agents.

    Responsibilities:
    - Detects missing components or incomplete reasoning
    - Highlights logical flaws and risky assumptions
    - Points out edge cases and potential failure scenarios
    - Provides constructive criticism to improve overall solution quality

    This agent focuses on finding problems rather than proposing fixes.
    """

    def __init__(self, model_client):
        """
        Initializes the Critic agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="critic",
            system_message="""
            You are the Critic agent.
            Find weaknesses, missing pieces, risks.
            """,
            model_client=model_client
        )

    async def run(self, task):
        """
        Reviews a given task or agent output and returns critical feedback.
        Sends the content to the underlying AssistantAgent and retrieves
        an evaluation focused on risks, omissions, and weaknesses.
        """

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=task, source="user")],
            cancellation
        )

        return response.chat_message.content
