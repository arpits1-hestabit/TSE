from dataclasses import dataclass
from typing import List

from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage, ChatCompletionClient
from messages import ReflectionTask, ReflectedResult


class ReflectionAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(description="Reflection Agent")
        self._model_client = model_client

    @message_handler
    async def reflect(self, message: ReflectionTask, ctx: MessageContext) -> ReflectedResult:

        prompt = (
            "Combine the worker outputs into a clean final answer.\n"
            "Answer ONLY in English.\n"
            "Do NOT add new facts.\n"
            "Keep it clear and structured.\n"
        )

        combined = "\n".join(message.worker_outputs)

        model_result = await self._model_client.create(
            [
                SystemMessage(content=prompt),
                UserMessage(content=combined, source="user"),
            ],
        )

        return ReflectedResult(result=str(model_result.content))
