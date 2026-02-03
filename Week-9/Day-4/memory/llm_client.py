from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()
def get_groq_client(model="openai/gpt-oss-20b"):
    return OpenAIChatCompletionClient(
        model=model,
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        model_info={
            "family": "groq",
            "supports_system_messages": True,
            "function_calling": False,
            "vision": False,
            "json_output": False,
            "structured_output": False,
        },
    )

def get_ollama_client(model="qwen3:8b"):
    return OpenAIChatCompletionClient(
        model=model,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        model_info={
            "family": "ollama",
            "supports_system_messages": True,
            "function_calling": False,
            "vision": False,
            "json_output": False,
            "structured_output": False,
        },
    )


def get_llm_client():
    provider = os.getenv("MODEL_PROVIDER", "groq").lower()

    if provider == "ollama":
        return get_ollama_client()
    else:
        return get_groq_client()
