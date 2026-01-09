import json
import tiktoken
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE = Path("dataset/train.jsonl")
OUTPUT_FILE = Path("dataset/train_clean.jsonl")
ATTACHMENTS_DIR = Path("Attachments")
MAX_TOKENS = 2000
ENCODING_NAME = "cl100k_base" # this is used because it is safe for coding and instruction datasets.


encoding = tiktoken.get_encoding(ENCODING_NAME)

# function to count tokens in a text
def count_tokens(text):
    if not text:
        return 0
    return len(encoding.encode(text))


samples = []
with INPUT_FILE.open() as f:
    for line in f:
        samples.append(json.loads(line))

print(f"Loaded {len(samples)} samples")


lengths = []
clean_samples = []

for s in samples:
    instruction = s.get("instruction", "")
    input_text = s.get("input", "")
    output = s.get("output", "")

    instr_len = count_tokens(instruction)
    input_len = count_tokens(input_text)
    output_len = count_tokens(output)

    total_len = instr_len + input_len + output_len

    s["token_stats"] = {
        "instruction": instr_len,
        "input": input_len,
        "output": output_len,
        "total": total_len
    }

    lengths.append(total_len)

    
    if (
        total_len <= MAX_TOKENS and
        instr_len > 0 and
        output_len > 0
    ):
        clean_samples.append(s)


OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w") as f:
    for s in clean_samples:
        f.write(json.dumps(s) + "\n")

print(f"Cleaned dataset size: {len(clean_samples)}")

# histogram for token lengths
plt.figure(figsize=(8, 5))
plt.hist(lengths, bins=50)
plt.title("Token Length Distribution")
plt.xlabel("Total Tokens")
plt.ylabel("Number of Samples")
plt.savefig(ATTACHMENTS_DIR/"token_length_distribution.png")
print("Data cleaning complete")
