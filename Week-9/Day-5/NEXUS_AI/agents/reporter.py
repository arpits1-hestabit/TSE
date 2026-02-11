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

    def __init__(self, model_client, output_dir="NEXUS_AI/outputs"):
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

        Supports both:
        - Legacy format: {agent_name: output}
        - New format: {
            "outputs": {agent_name: output},
            "confidence": {agent_name: float}
          }
        """

        cancellation = CancellationToken()

        # Normalize input (backward compatible)
        if "outputs" in aggregated_outputs:
            outputs = aggregated_outputs.get("outputs", {})
            confidence = aggregated_outputs.get("confidence", {})
        else:
            outputs = aggregated_outputs
            confidence = {}

        # Build prompt for the Reporter agent
        prompt = f"""
        USER QUESTION:
        {user_question}

        AGENT OUTPUTS:
        """

        for agent_name, output in outputs.items():
            # Ensure output is always string-safe
            if not isinstance(output, str):
                output = str(output)

            score = confidence.get(agent_name)

            header = f"### {agent_name} Output"
            if score is not None:
                header += f" (confidence: {score:.2f})"

            prompt += f"{header}:\n{output[:1200]}\n\n"

        prompt += (
            "Instructions: Compile all outputs into one final answer, "
            "in a clear, concise, and well-structured manner."
        )

        # Invoke Reporter agent
        response = await self.agent.on_messages(
            [TextMessage(content=prompt, source="user")],
            cancellation
        )

        final_text = response.chat_message.content

        # Save to disk
        filename = self.sanitize_filename(user_question) + ".md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# User Question\n\n{user_question}\n\n")
            f.write("# Final Answer (Reporter Output)\n\n")
            f.write(final_text)

        return final_text
