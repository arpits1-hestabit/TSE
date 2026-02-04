import asyncio
from autogen_core import AgentId, SingleThreadedAgentRuntime

from model import get_ollama_client

from agents.worker_agent import WorkerAgent
from agents.reflection import ReflectionAgent
from agents.validator import ValidatorAgent
from agents.orchestrator.planner import OrchestratorAgent

from agents.messages import UserTask


async def main():
    runtime = SingleThreadedAgentRuntime()
    #model_client = get_ollama_client("granite3-dense:8b")
    #model_client = get_ollama_client("ordis/gte-Qwen2-7B-instruct-Q5_K_M-GGUF-8k:latest")
    #model_client = get_ollama_client("tinyllama")
    #model_client = get_ollama_client("phi3:14b")
    #model_client = get_ollama_client("mistral:7b")
    model_client = get_ollama_client("qwen3:8b")
    await WorkerAgent.register(
        runtime,
        "worker",
        lambda: WorkerAgent(model_client),
    )

    await ReflectionAgent.register(
        runtime,
        "reflection",
        lambda: ReflectionAgent(model_client),
    )

    await ValidatorAgent.register(
        runtime,
        "validator",
        lambda: ValidatorAgent(model_client),
    )

    await OrchestratorAgent.register(
        runtime,
        "orchestrator",
        lambda: OrchestratorAgent(model_client),
    )

    runtime.start()
    print("\n-- SYSTEM STARTED --\n")

    result = await runtime.send_message(
        UserTask(task="Explain how a machine learning model is trained, separating tasks that can be done in parallel."),
        AgentId("orchestrator", "default"),
    )

    await runtime.stop_when_idle()
    await model_client.close()

    print("\n" + "-==-" * 80)
    print("FINAL RESULT:\n")
    print(result.result)



if __name__ == "__main__":
    asyncio.run(main())
