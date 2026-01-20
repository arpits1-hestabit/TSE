import logging
import uuid
from typing import List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from model_loader import ModelClient
from config import *

app = FastAPI(title=API_TITLE, version=API_VERSION)
model = ModelClient()

# Used for logging
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console = logging.StreamHandler()
    file = logging.FileHandler("logs/api_requests.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)

# Used to log each request and response
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        body = await request.json()
    except Exception:
        body = {}

    request_id = body.get("request_id", "N/A")
    logger.info(f"REQUEST {request_id} START {request.method} {request.url}")
    logger.info(f"BODY: {body}")

    response = await call_next(request)
    logger.info(f"REQUEST {request_id} END {response.status_code}")
    return response

# Used for request validation
class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    stream: bool = False

class ChatRequest(BaseModel):
    messages: List[Message]
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    stream: bool = False

# Prompts
GENERATE_SYSTEM_PROMPT = (
    "You are an expert AI assistant.\n"
    "Answer ONLY the question.\n"
    "Do NOT repeat the question.\n"
    "Be concise, factual, and clear."
)

CHAT_SYSTEM_PROMPT = (
    "You are a helpful, conversational assistant.\n"
    "Maintain context across messages.\n"
    "Do not repeat user input.\n"
    "Respond clearly and naturally."
)

def generate_request_id():
    return str(uuid.uuid4())

def needs_bullets(text: str) -> bool:
    return "bullet" in text.lower() or "points" in text.lower()

def sse(message: str):
    return f"data: {message}\n\n"

def clean_token(token):
    if not token:
        return ""
    if not isinstance(token, str):
        return ""
    # filter obvious garbage
    if token.strip() in {"IsAny", "<|endoftext|>"}:
        return ""
    return token

def sse_format(message: str) -> str:
    return f"data: {message}\n\n"


# When the generate endpoint is called
@app.post("/generate")
async def generate(req: GenerateRequest):
    system_prompt = GENERATE_SYSTEM_PROMPT
    if needs_bullets(req.prompt):
        system_prompt += "\nIMPORTANT: Respond ONLY in bullet points."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.prompt},
    ]

    response = await model.chat(
        messages,
        req.max_tokens,
        req.temperature,
        req.top_p,
        req.stream,
    )

    if req.stream:
        async def stream_tokens():
            async for chunk in response:
                delta = chunk.choices[0].delta
                token = clean_token(getattr(delta, "content", None))
                if token:
                    yield sse_format(token)
            yield sse_format("[DONE]")

        return StreamingResponse(
            stream_tokens(),
            media_type="text/event-stream",
        )

# When the chat endpoint is called
@app.post("/chat")
async def chat(req: ChatRequest):
    messages = [m.dict() for m in req.messages]

    # Inject system prompt ONCE
    if messages[0]["role"] != "system":
        system_prompt = CHAT_SYSTEM_PROMPT
        if needs_bullets(messages[-1]["content"]):
            system_prompt += "\nIMPORTANT: Respond ONLY in bullet points."
        messages.insert(0, {"role": "system", "content": system_prompt})

    response = await model.chat(
        messages,
        req.max_tokens,
        req.temperature,
        req.top_p,
        req.stream,
    )

    if req.stream:
        async def stream_tokens():
            async for chunk in response:
                delta = chunk.choices[0].delta
                token = clean_token(getattr(delta, "content", None))
                if token:
                    yield sse_format(token)
            yield sse_format("[DONE]")

        return StreamingResponse(
            stream_tokens(),
            media_type="text/event-stream",
        )

