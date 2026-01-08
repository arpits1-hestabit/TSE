from langchain_classic.memory import ConversationBufferWindowMemory

class MemoryStore:
    def __init__(self, k=5):
        self.memory = ConversationBufferWindowMemory(
            k=k,
            return_messages=True
        )

    def add_user(self, text):
        self.memory.chat_memory.add_user_message(text)

    def add_ai(self, text):
        self.memory.chat_memory.add_ai_message(text)

    def get_context(self):
        messages = self.memory.chat_memory.messages
        return "\n".join(
            f"{m.type}: {m.content}" for m in messages
        )
