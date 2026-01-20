from openai import AsyncOpenAI
from config import MODEL_BASE_URL, MODEL_ID

class ModelClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=MODEL_BASE_URL,
            api_key="EMPTY"
        )

    async def chat(self, messages, max_tokens, temperature, top_p, stream):
        return await self.client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=None,
        )
