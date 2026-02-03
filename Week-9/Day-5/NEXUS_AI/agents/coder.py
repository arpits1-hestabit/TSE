from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class CoderAgent:
    """
    Coder agent responsible for generating high-quality source code
    based on assigned tasks.

    Responsibilities:
    - Produces clean, modular, and well-structured code
    - Applies best practices and industry standards
    - Adds meaningful comments and documentation
    - Ensures correctness, readability, and maintainability

    This agent focuses purely on code generation and does not perform
    validation or optimization unless explicitly instructed.
    """

    def __init__(self, model_client):
        """
        Initializes the Coder agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="coder",
            system_message="""
            You are the Coder agent.
            Write clean, modular, correct code for tasks.
            Use proper comments and best practices.
            """,
            model_client=model_client
        )

    async def run(self, task):
        """
        Generates source code for a given task.
        Sends the task prompt to the underlying AssistantAgent and
        returns the generated code as a plain text response.
        """

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=task, source="user")],
            cancellation
        )

        return response.chat_message.content
