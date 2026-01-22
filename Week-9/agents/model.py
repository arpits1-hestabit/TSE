from autogen_ext.models.openai import OpenAIChatCompletionClient

# def get_ollama_client(
#     #model: str = "ordis/gte-Qwen2-7B-instruct-Q5_K_M-GGUF-8k:latest",
#     #model: str = "tinyllama",
#     #model: str = "phi3:14b",
#     #model: str = "mistral:7b",
#     host: str = "http://localhost:11434",
# ):
#     return OpenAIChatCompletionClient(
#         model=model,
#         base_url=f"{host}/v1",
#         api_key="ollama",
#         model_info={
#              "family": "ollama",
#              "vision": False,
#              "function_calling": False,
#              "json_output": False,
#              "structured_output": False,
#              "supports_system_messages": True,
#              "multiple_system_messages": True,
#          }
#     )

from autogen_ext.models.openai import OpenAIChatCompletionClient

def get_ollama_client(model_name: str):
    return OpenAIChatCompletionClient(
        model=model_name,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        model_info={
            "family": "ollama",
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "structured_output": False,
            "supports_system_messages": True,
            "multiple_system_messages": True,
        },
    )
