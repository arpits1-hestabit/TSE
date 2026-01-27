from collections import deque

class SessionMemory:
    def __init__(self, max_turns=6):
        self.buffer = deque(maxlen=max_turns)

    def add(self, role: str, content: str):
        print(f"[SESSION MEMORY] Saved {role} message")
        self.buffer.append({"role": role, "content": content})

    def get_context(self) -> str:
        if not self.buffer:
            return "No session memory"
        return "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in self.buffer
        )

    def clear(self):
        self.buffer.clear()
