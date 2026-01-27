from autogen_agentchat.agents import AssistantAgent
from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore

SIMILARITY_THRESHOLD = 0.82


class MemoryAgent(AssistantAgent):
    def __init__(self, model_client):
        super().__init__(
            name="MemoryAgent",
            model_client=model_client,
            system_message="""
You are a memory-aware assistant.
If relevant memory exists, reuse it verbatim.
"""
        )
        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()

    async def respond(self, user_input: str):
        print("\n ------ MEMORY CHECK ------")

        result = self.vector_store.search(user_input)

        if result:
            score, content = result
            print(f"[VECTOR DB] Similarity score: {score:.4f}")

            if score >= SIMILARITY_THRESHOLD:
                print("Memory HIT — responding from memory")
                self.session_memory.add("user", user_input)
                self.session_memory.add("assistant", content)
                return f"[MEMORY RESPONSE]\n{content}"

        print("Memory MISS — generating fresh answer")

        session_context = self.session_memory.get_context()

        prompt = f"""
SESSION CONTEXT:
{session_context}

USER QUERY:
{user_input}
"""

        response = await self.run(task=prompt)
        answer = response.messages[-1].content

        self.session_memory.add("user", user_input)
        self.session_memory.add("assistant", answer)
        self.vector_store.add(user_input, answer)

        return f"[FRESH RESPONSE]\n{answer}"
