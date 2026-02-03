import json
import re

from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage, ChatCompletionClient

from messages import ValidationTask, ValidationResult


class ValidatorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(description="Validator Agent")
        self._model_client = model_client

    # This is a helper function to extract JSON from LLM output.
    def _extract_json(self, text: str) -> dict | None:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    @message_handler
    async def validate(
        self, message: ValidationTask, ctx: MessageContext
    ) -> ValidationResult:

        prompt = (
            "Check whether the following answer is:\n"
            "1. Written only in English\n"
            "2. Correct for the given task\n\n"
            "Return JSON ONLY:\n"
            "{\n"
            "  \"is_valid\": true/false,\n"
            "  \"feedback\": \"short explanation\"\n"
            "}\n\n"
            f"Task: {message.task}\n"
            f"Answer: {message.answer}"
        )

        response = await self._model_client.create(
            [
                SystemMessage(content=prompt),
                UserMessage(content="Validate.", source="user"),
            ],
        )

        raw = str(response.content)

        print("\n[Validator raw output]")
        print(raw)

        parsed = self._extract_json(raw)

        # Fallback for invalid JSON
        if not parsed:
            print("[Validator warning] Invalid JSON → accepting answer")
            return ValidationResult(
                is_valid=True,
                feedback="Validator returned invalid JSON; accepted by fallback.",
                answer=message.answer,
            )

        # Extract validation results
        is_valid = bool(parsed.get("is_valid", True))
        feedback = str(parsed.get("feedback", ""))

        return ValidationResult(
            is_valid=is_valid,
            feedback=feedback,
            answer=message.answer,
        )
