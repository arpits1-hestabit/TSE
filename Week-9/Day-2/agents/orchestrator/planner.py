import asyncio
import json
import re
from typing import List

from autogen_core import AgentId, RoutedAgent, MessageContext, message_handler
from autogen_core.models import SystemMessage, UserMessage, ChatCompletionClient

from messages import (
    UserTask,
    WorkerTask,
    ReflectionTask,
    ValidationTask,
    FinalResult,
)

class OrchestratorAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient):
        super().__init__(description="Orchestrator / Planner Agent")
        self._model_client = model_client

    # This is a helper function to extract JSON from LLM output.
    def _extract_json(self, text: str) -> dict | None:
        """
        It will extract the FIRST valid JSON object from model output.
        """
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    # Execution plan creation
    async def create_execution_plan(self, task: str) -> List[List[str]]:
        prompt = (
            "You are a task planner.\n"
            "Decide how many layers and parallel workers are needed.\n\n"
            "Rules:\n"
            "- Simple explanation → 1 layer, 2 workers\n"
            "- Medium task → 2 layers, 3 workers\n"
            "- Complex task → 3+ layers\n\n"
            "Return JSON ONLY in this format:\n"
            "{ \"layers\": [[\"w1\", \"w2\"], [\"w3\"]] }\n\n"
            f"Task: {task}"
        )

        result = await self._model_client.create(
            [
                SystemMessage(content=prompt),
                UserMessage(content="Create execution plan.", source="user"),
            ],
        )

        raw = str(result.content)

        print("\n[Planner output]")
        print(raw)

        parsed = self._extract_json(raw)

        # This is a fallback plan in case execution plan parsing fails.
        if not parsed or "layers" not in parsed:
            print("\n[Planner warning] Invalid or empty plan → using fallback")
            return [["w1", "w2"], ["w3"]]

        return parsed["layers"]

    # Orchestration handler
    @message_handler
    async def handle_task(self, message: UserTask, ctx: MessageContext) -> FinalResult:
        task = message.task

        print("\nPlanner received:", task)

        layers = await self.create_execution_plan(task)

        # Execution plan logging
        print("\nExecution Tree:")
        for i, layer in enumerate(layers):
            print(f"Layer {i}: {layer}")

        previous_results: List[str] = []

        # Execution of layers
        for layer_idx, worker_keys in enumerate(layers):
            print(f"\n--- Executing Layer {layer_idx} ---")

            workers = [AgentId("worker", key) for key in worker_keys]

            results = await asyncio.gather(
                *[
                    self.send_message(
                        WorkerTask(task=task, previous_results=previous_results),
                        worker,
                    )
                    for worker in workers
                ]
            )

            previous_results = [r.result for r in results]

        # Reflection step
        reflected = await self.send_message(
            ReflectionTask(task=task, worker_outputs=previous_results),
            AgentId("reflection", "default"),
        )

        # Validation step
        validated = await self.send_message(
        ValidationTask(task=task, answer=reflected.result),
        AgentId("validator", "default"),
    )

        if not validated.is_valid:
            return FinalResult(
                result=f"Validation failed:\n{validated.feedback}\n\n{validated.answer}"
        )

        return FinalResult(result=validated.answer)