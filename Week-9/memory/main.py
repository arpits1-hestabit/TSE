import asyncio
from llm_client import get_llm_client
from memory.memory_agent import MemoryAgent

async def main():
    model_client = get_llm_client()
    agent = MemoryAgent(model_client)

    while True:
        query = input("\nUser -> ")
        if query.lower() in {"exit", "quit"}:
            break

        reply = await agent.respond(query)
        print("\nAgent ->", reply)

if __name__ == "__main__":
    asyncio.run(main())
