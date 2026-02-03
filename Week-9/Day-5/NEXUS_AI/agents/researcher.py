from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class ResearcherAgent:
    """
    Researcher agent responsible for gathering domain knowledge, best practices,
    tools, libraries, and conceptual insights relevant to a given task.

    Responsibilities:
    - Collects background information and reference material
    - Identifies suitable libraries, frameworks, and algorithms
    - Shares industry best practices and design patterns
    - Avoids implementation details or code generation

    This agent focuses purely on research and knowledge synthesis.
    """

    def __init__(self, model_client):
        """
        Initializes the Researcher agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="researcher",
            system_message="""
            You are the Researcher agent.
            Gather best practices, libraries, tools, algorithms.
            Do NOT code. Just provide knowledge.
            """,
            model_client=model_client
        )

    async def run(self, task):
        """
        Performs research for a given task and returns synthesized knowledge.
        Sends the task to the underlying AssistantAgent and retrieves
        conceptual guidance, references, and best practices.
        """

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=task, source="user")],
            cancellation
        )

        return response.chat_message.content

