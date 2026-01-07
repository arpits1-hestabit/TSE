import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

DEFAULT_MODEL_PATH = os.path.expanduser(
    "~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/"
    "snapshots/989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
)


def load_llm(model_path: str = DEFAULT_MODEL_PATH):

    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
        trust_remote_code=True
    )

    model.eval()

    return model, tokenizer
