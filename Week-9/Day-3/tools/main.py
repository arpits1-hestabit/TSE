import asyncio
from tools.orchestrator import run_orchestration, summarize_results
from agents.answer_agent import answer_agent

async def main():
    user_query = "Analyze sales.csv and generate top 5 insights"

    context = await run_orchestration(user_query)
    summary = summarize_results(context)

    result = await answer_agent.run(
        task=f"User query:\n{user_query}\n\nContext:\n{summary}"
    )

    print("\n------ FINAL OUTPUT ------")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
