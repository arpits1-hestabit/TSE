from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient

def get_llama_model():
    return LlamaCppChatCompletionClient(
        model_path="models/qwen2.5-coder-7b-instruct-q4_k_m.gguf",
        n_ctx=8192,
        max_tokens=512,
        temperature=0.4,
        verbose=False
    )
