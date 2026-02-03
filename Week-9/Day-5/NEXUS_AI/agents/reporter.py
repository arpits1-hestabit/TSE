import os
import re
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class ReporterAgent:
    """
    Reporter agent responsible for compiling and presenting the final output
    of the multi-agent workflow.

    Responsibilities:
    - Aggregates outputs from all contributing agents
    - Produces a clear, concise, and well-structured final response
    - Ensures professional formatting and readability
    - Persists the final report to disk for later reference

    This agent acts as the final synthesis and presentation layer of the system.
    """

    def __init__(self, model_client, output_dir="outputs"):
        """
        Initializes the Reporter agent with a language model client.
        """

        self.agent = AssistantAgent(
            name="Reporter",
            system_message="""
            You are the Reporter agent.
            Compile all provided outputs into a clear, structured, and professional final answer.
            Focus on conciseness and clarity.
            """,
            model_client=model_client
        )

        # Ensure output directory exists
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def sanitize_filename(text: str) -> str:
        """
        Converts arbitrary text into a filesystem-safe filename.

        Removes invalid characters, replaces spaces with underscores,
        and limits filename length to prevent OS-related issues.
        """
        text = text.strip().replace(" ", "_")
        text = re.sub(r"[^\w\-_\.]", "", text)
        return text[:100]

    async def run(self, user_question: str, aggregated_outputs: dict):
        """
        Generates and saves the final report based on aggregated agent outputs.

        Workflow:
        1. Constructs a prompt containing the user question and agent outputs
        2. Sends the prompt to the Reporter LLM agent
        3. Receives a consolidated final answer
        4. Saves the result as a markdown file in the output directory
        """

        cancellation = CancellationToken()

        # Build prompt for the Reporter agent
        prompt = f"""
            USER QUESTION:
            {user_question}

            AGENT OUTPUTS:
        """

        for agent_name, output in aggregated_outputs.items():
            # Truncate individual agent outputs to keep prompt size reasonable
            prompt += f"### {agent_name} Output:\n{output[:1200]}\n\n"

        prompt += (
            "Instructions: Compile all outputs into one final answer, "
            "in a clear and structured manner."
        )

        # Invoke the Reporter agent
        response = await self.agent.on_messages(
            [TextMessage(content=prompt, source="user")],
            cancellation
        )

        final_text = response.chat_message.content

        # Create a safe filename from the user question
        filename = self.sanitize_filename(user_question) + ".md"
        filepath = os.path.join(self.output_dir, filename)

        # Persist the final report to disk
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# User Question:\n{user_question}\n\n")
            f.write("# Final Answer (Reporter Output)\n\n")
            f.write(final_text)

        return final_text
