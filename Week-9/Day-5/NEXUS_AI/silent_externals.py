import os
import logging
import warnings

def silence_all_logs():
    """
    Completely silences noisy external libraries like:
    - HuggingFace Hub
    - Transformers
    - SentenceTransformers
    - HTTPX requests
    """
    warnings.filterwarnings("ignore", category=UserWarning)
    # Disable HuggingFace progress bars
    os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    # Disable tokenizer parallel warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Reduce transformers verbosity
    os.environ["TRANSFORMERS_VERBOSITY"] = "error"

    # Silence loggers from noisy libraries
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Global fallback: silence all loggers except errors for code using logging without explicit config
    logging.basicConfig(level=logging.ERROR)


