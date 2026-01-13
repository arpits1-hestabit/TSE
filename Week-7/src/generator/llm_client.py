import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained( MODEL_NAME, device_map="auto",dtype = "auto")


def generate(prompt: str, max_tokens: int = 512) -> str:
    messages = f"{prompt}"
    inputs = tokenizer( messages, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    if decoded.startswith(prompt):
        return decoded[len(prompt):].strip()

    return decoded.strip()