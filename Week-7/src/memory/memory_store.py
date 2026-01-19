from collections import deque
from datetime import datetime

class MemoryStore:
    def __init__(self, k=5):
        self.conversation_history = []
        self.question_history = deque(maxlen=5)

    def add_user(self, text):
        self.conversation_history.append({
            "type": "user",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })

    def add_ai(self, text):
        self.conversation_history.append({
            "type": "ai",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })

    def add_question(self, question: str, mode: str = "Text RAG"):
        self.question_history.append({
            "question": question,
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        })

    def get_question_history(self):
        return list(reversed(list(self.question_history)))

    def get_context(self):
        return "\n".join(
            f"{m['type']}: {m['content']}" for m in self.conversation_history
        )

    def clear_history(self):
        self.conversation_history = []

    def clear_all(self):
        self.conversation_history = []
        self.question_history.clear()
