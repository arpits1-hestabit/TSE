from dataclasses import dataclass
from typing import List
import asyncio

from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage, ChatCompletionClient
from messages import WorkerTask, WorkerTaskResult


class WorkerAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(description="Worker Agent")
        self._model_client = model_client

    @message_handler
    async def handle_task(self, message: WorkerTask, ctx: MessageContext) -> WorkerTaskResult:

        print(f"\nWorker {self.id} received task")

        system_prompt = (
            "You are an expert AI assistant.\n"
            "Answer ONLY in English.\n"
            "Do NOT mix languages.\n"
            "Keep it short and clear.\n"
        )

        if message.previous_results:
            system_prompt += "Use previous results and improve them.\n"

        try:
            model_result = await asyncio.wait_for(
                self._model_client.create(
                    [
                        SystemMessage(content=system_prompt),
                        UserMessage(content=message.task, source="user"),
                    ],
                ),
                timeout=300,
            )

        except asyncio.TimeoutError:
            print(f"Worker {self.id} timed out!")
            return WorkerTaskResult(result="ERROR: Worker timed out.")

        print(f"Worker {self.id} finished")

        return WorkerTaskResult(result=str(model_result.content))
