# from collections import deque

# class SessionMemory:
#     def __init__(self, max_turns=6):
#         self.buffer = deque(maxlen=max_turns)

#     def add(self, role: str, content: str):
#         print(f"[SESSION MEMORY] Saved {role} message")
#         self.buffer.append({"role": role, "content": content})

#     def get_context(self) -> str:
#         if not self.buffer:
#             return "No session memory"
#         return "\n".join(
#             f"{m['role'].upper()}: {m['content']}" for m in self.buffer
#         )

#     def clear(self):
#         self.buffer.clear()



from autogen_core.memory import Memory, MemoryContent, MemoryMimeType, MemoryQueryResult, UpdateContextResult


class SessionMemory(Memory):
    def __init__(self, max_turns: int = 8):
        self.max_turns = max_turns
        self.turns = []

    async def add(self, content: str):
        self.turns.append(content)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    async def query(self, query_str: str):
        # return all stored turns as memory content
        return [
            MemoryContent(content=t, mime_type=MemoryMimeType.TEXT)
            for t in self.turns
        ]

    async def update_context(self, model_context):
        # Returns the last max_turns messages
        return UpdateContextResult(
            memories=MemoryQueryResult(
                results=[
                    MemoryContent(content=t, mime_type=MemoryMimeType.TEXT)
                    for t in self.turns
                ]
            )
        )

    async def clear(self):
        self.turns = []

    async def close(self):
        pass
