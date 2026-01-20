import uuid

API_TITLE = "GGUF LLM Service"
API_VERSION = "1.0"

MODEL_BASE_URL = "http://localhost:8004/v1"
MODEL_ID = "model-q4_0.gguf"

DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95

def generate_request_id():
    return str(uuid.uuid4())
