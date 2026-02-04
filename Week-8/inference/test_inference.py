import asyncio
import time
import json
import csv
from openai import AsyncOpenAI
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoTokenizer


PROMPT_FILE = "prompts.json"
MAX_TOKENS = 200
TOKENIZER_PATH = "Qwen/Qwen2.5-1.5B-Instruct"

MODELS = [
    #{"name": "base_fp16", "port": 8000, "model_id": "Qwen/Qwen2.5-1.5B-Instruct"},
    #{"name": "finetuned", "port": 8001, "model_id": "merged_qwen"},
    #{"name": "int8", "port": 8002, "model_id": "/home/arpitsaxena/Desktop/TSE/Week-8/quantized/model-int8"},
    #{"name": "int4", "port": 8003, "model_id": "/home/arpitsaxena/Desktop/TSE/Week-8/quantized/model-int4"},
    {"name": "gguf", "port": 8004, "model_id": "/home/arpitsaxena/Desktop/TSE/Week-8/quantized/model-q4_0.gguf"},
]

BLEU_SMOOTH = SmoothingFunction().method1

# Loading prompts and references
with open(PROMPT_FILE, "r") as f:
    data = json.load(f)

PROMPTS = data["prompts"]
REFERENCES = data["references"]

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)

# Metrics computation
def compute_metrics(output, reference):
    exact_match = int(output.strip().lower() == reference.strip().lower())
    bleu = sentence_bleu(
        [reference.split()],
        output.split(),
        smoothing_function=BLEU_SMOOTH,
    )
    return exact_match, bleu

# Streaming inference
async def stream_inference(client, model_id, prompt):
    start_time = time.time()
    first_token_time = None
    output = ""

    stream = await client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            if first_token_time is None:
                first_token_time = time.time()
            output += delta.content

    end_time = time.time()

    gen_tokens = len(tokenizer.encode(output))

    return {
        "output": output.strip(),
        "latency": end_time - start_time,
        "ttft": (first_token_time - start_time) if first_token_time else None,
        "tokens": gen_tokens,
        "tokens_per_sec": gen_tokens / (end_time - first_token_time)
        if first_token_time else 0,
    }
# Batch inference
async def batch_inference(client, model_id, prompts):
    start = time.time()

    response = await client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": p} for p in prompts],
        max_tokens=MAX_TOKENS,
        stream=False,
    )

    end = time.time()
    outputs = [c.message.content for c in response.choices]

    total_tokens = sum(len(tokenizer.encode(o)) for o in outputs)
    total_time = end - start

    return outputs, total_tokens, total_time

# Benchmark runner
async def benchmark():
    results = []

    for model in MODELS:
        base_url = f"http://localhost:{model['port']}/v1"
        client = AsyncOpenAI(base_url=base_url, api_key="EMPTY")

        print(f"\nBenchmarking {model['name']} (port {model['port']})")

        # Warm-up
        print("Warming up...")
        await stream_inference(client, model["model_id"], PROMPTS[0])

        # Streaming tests
        for idx, prompt in enumerate(PROMPTS):
            res = await stream_inference(client, model["model_id"], prompt)
            exact_match, bleu = compute_metrics(res["output"], REFERENCES[idx])

            results.append(
                {
                    "model": model["name"],
                    "prompt_idx": idx + 1,
                    "latency_sec": round(res["latency"], 3),
                    "ttft_sec": round(res["ttft"], 3) if res["ttft"] else None,
                    "token_count": res["tokens"],
                    "tokens_per_sec": round(res["tokens_per_sec"], 2),
                    "exact_match": exact_match,
                    "bleu_score": round(bleu, 4),
                }
            )

            print(
                f"{model['name']} | Prompt {idx+1} | "
                f"TTFT={res['ttft']:.3f}s | "
                f"Latency={res['latency']:.2f}s | "
                f"TPS={res['tokens_per_sec']:.2f} | "
                f"BLEU={bleu:.4f}"
            )

        # Batch test
        batch_outputs, batch_tokens, batch_time = await batch_inference(
            client, model["model_id"], PROMPTS
        )

        results.append(
            {
                "model": model["name"],
                "prompt_idx": "BATCH",
                "latency_sec": round(batch_time, 3),
                "ttft_sec": None,
                "token_count": batch_tokens,
                "tokens_per_sec": round(batch_tokens / batch_time, 2),
                "exact_match": None,
                "bleu_score": None,
            }
        )

        print(
            f"{model['name']} | BATCH | "
            f"Prompts={len(PROMPTS)} | "
            f"Tokens/sec={batch_tokens / batch_time:.2f}"
        )

    # Saving CSV
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Inference quality tests
    print("\n=== Running Inference Quality Tests ===")
    for model in MODELS:
        base_url = f"http://localhost:{model['port']}/v1"
        client = AsyncOpenAI(base_url=base_url, api_key="EMPTY")
        
        bleu_scores = [r["bleu_score"] for r in results if r["model"] == model["name"] and r["bleu_score"]]
        exact_matches = [r["exact_match"] for r in results if r["model"] == model["name"] and r["exact_match"] is not None]
        
        avg_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
        avg_exact = sum(exact_matches) / len(exact_matches) if exact_matches else 0
        
        print(f"{model['name']} | Avg BLEU={avg_bleu:.4f} | Avg Exact Match={avg_exact:.2%}")
        assert avg_bleu > 0, f"BLEU score too low for {model['name']}"
        
    # Performance regression tests
    print("\n=== Running Performance Regression Tests ===")
    for model in MODELS:
        ttft_values = [r["ttft_sec"] for r in results if r["model"] == model["name"] and r["ttft_sec"]]
        avg_ttft = sum(ttft_values) / len(ttft_values) if ttft_values else 0
        
        print(f"{model['name']} | Avg TTFT={avg_ttft:.3f}s")
        assert avg_ttft < 5.0, f"TTFT regression detected for {model['name']}"

if __name__ == "__main__":
    asyncio.run(benchmark())
