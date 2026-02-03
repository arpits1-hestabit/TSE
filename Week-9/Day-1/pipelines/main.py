import asyncio
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage
from agents import research_agent as ra, summarizer_agent as sa, answer_agent as aa

async def main():
    user_query = "What is machine learning and how is it used?"
    cancellation = CancellationToken()

    print(f"User_query: {user_query}\n")

    research = await ra.research_agent.on_messages(
        [TextMessage(content=user_query, source="user")],
        cancellation
    )
    output = research.chat_message.content
    print("Research Output:\n", output, "\n")

    summary = await sa.summarizer_agent.on_messages(
        [TextMessage(content=output, source="researcher")],
        cancellation
    )
    output = summary.chat_message.content
    print("Summary Output:\n", output, "\n")

    answer = await aa.answer_agent.on_messages(
        [TextMessage(content=output, source="summarizer")],
        cancellation
    )
    final_answer = answer.chat_message.content
    print(f"Final Answer: {final_answer}\n")


asyncio.run(main())
