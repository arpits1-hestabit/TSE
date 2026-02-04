from fastapi import FastAPI, UploadFile, File , Form
from pathlib import Path
import shutil
from memory.memory_store import MemoryStore
from evaluation.rag_eval import RAGEvaluator

from tests.test_retrieval import ask_retrieval
from retriever.test_image_search import image_to_image_final, image_to_text_final, text_to_image_final
from pipelines.sql_pipeline import SQLPipeline
from src.config.config import get_config
from src.utils.logger import get_logger
from src.retriever.text_search import TextSearcher
from src.retriever.image_search import ImageSearcher
from src.embeddings.embedder import Embedder
from src.generator.llm_client import LLMClient

logger = get_logger(__name__)

app = FastAPI(title="RAG System")

# Initialize with config paths
config = get_config()
embedder = Embedder()
text_searcher = TextSearcher()
image_searcher = ImageSearcher()
llm_client = LLMClient()

@app.on_event("startup")
async def startup():
    logger.info(f"✓ RAG System started")
    logger.info(f"Config: {config.env}")
    logger.info(f"Index path: {config.index_path}")
    logger.info(f"Metadata path: {config.metadata_path}")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "env": config.env,
        "index_path": str(config.index_path),
        "metadata_path": str(config.metadata_path)
    }

@app.post("/ask")
def ask(question: str):
    answer = ask_retrieval(question)
    score = evaluator.faithfulness_score(answer["answer"], answer["context"])
    answer["score"] = score
    return answer

@app.post("/ask-image")
def ask_image(
    question: str = Form(None),
    image: UploadFile = File(None),
    top_k: int = 5,
):
    if not question and not image:
        return {"error": "Provide either a question or an image"}

    image_path = None
    if image:
        image_path = UPLOAD_DIR / image.filename
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    if image_path and question:
        answer =  image_to_text_final(str(image_path), question, top_k)
        score = evaluator.faithfulness_score(answer["answer"], answer["context"])
        answer["score"] = score
        return answer

    if image_path:
        answer =  image_to_image_final(str(image_path), top_k)
        score = evaluator.faithfulness_score(answer["answer"], answer["context"])
        answer["score"] = score
        return answer

    answer =  text_to_image_final(question, top_k)
    score = evaluator.faithfulness_score(answer["answer"], answer["context"])
    answer["score"] = score
    return answer


@app.post("/ask-sql")
def ask_sql(question: str):
    result = sql_pipeline.run(question)
    return result

@app.post("/search/text")
async def search_text(query: str, top_k: int = None):
    try:
        embedding = embedder.encode([query])
        results = text_searcher.search(embedding[0], top_k)
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/search/image")
async def search_image(query: str, top_k: int = None):
    try:
        embedding = embedder.encode([query])
        results = image_searcher.search(embedding[0], top_k)
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Image search error: {e}")
        return {"status": "error", "message": str(e)}