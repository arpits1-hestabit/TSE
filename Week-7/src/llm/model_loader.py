from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer

LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
EMBEDDINGS_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def load_cached_model_and_embeddings():
    tokenizer = AutoTokenizer.from_pretrained(
        LLM_MODEL_NAME,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL_NAME,
        device_map="auto",
        trust_remote_code=True
    )

    embeddings = SentenceTransformer(EMBEDDINGS_MODEL_NAME)

    return model, tokenizer, embeddings
