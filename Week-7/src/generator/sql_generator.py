import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

PROMPT_DIR = "src/prompts"

class SQLGenerator:
    def __init__(self):
        model_path = os.path.expanduser(
            "~/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/"
            "snapshots/989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

        # Load prompts
        self.sql_generation_prompt = self._load_prompt("sql_generation.txt")
        self.sql_invalid_prompt = self._load_prompt("sql_invalid.txt")
        self.sql_explain_prompt = self._load_prompt("sql_explain.txt")

    def _load_prompt(self, filename):
        path = os.path.join(PROMPT_DIR, filename)
        if not os.path.exists(path):
            raise RuntimeError(f"Prompt file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded[len(prompt):].strip()

    def generate_sql(self, question, schema):
        prompt = self.sql_generation_prompt.format(
            question=question,
            schema=schema
        )
        return self._generate(prompt)

    def fix_sql(self, sql, schema, error):
        prompt = self.sql_invalid_prompt.format(
            sql=sql,
            schema=schema,
            error=error
        )
        return self._generate(prompt)

    def explain_result(self, question, sql, result):
        prompt = self.sql_explain_prompt.format(
            question=question,
            sql=sql,
            result=result
        )
        return self._generate(prompt)
