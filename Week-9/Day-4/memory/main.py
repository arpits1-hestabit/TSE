import asyncio

from autogen_agentchat.agents import AssistantAgent
from memory.vector_store import FaissSQLiteMemory
from llm_client import get_llm_client


async def main():
    model_client = get_llm_client()

    # Semantic and Episodic memory store
    memory = FaissSQLiteMemory(
        db_path="memory/long_term.db",
        k=3,
        threshold=0.8,
    )

    assistant = AssistantAgent(
        name="assistant_with_memory",
        model_client=model_client,
        memory=[memory],
    )

    print("\nType your question (type 'exit' to quit):\n")

    while True:
        user_input = input("You:|> ")

        if user_input.lower() == "exit":
            break

        # Check memory
        recalled = await memory.query(user_input)

        if recalled:
            print("\nAssistant (from memory):|>")
            print(recalled[0].content, "\n")
            continue

        # Otherwise call LLM, if not found in the memory
        response = await assistant.run(task=user_input)

        answer = response.messages[-1].content
        print("\nAssistant:", answer, "\n")

        # Save only NEW question-answer pair
        await memory.add(content=answer, question=user_input)

    await assistant.close()


if __name__ == "__main__":
    asyncio.run(main())
