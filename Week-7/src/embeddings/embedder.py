import json
import numpy as np
import os
import logging
import time
from src.config.config import get_config
from src.utils.logger import get_logger
from src.utils.errors import EmbeddingError

logger = get_logger(__name__)

CHUNKS_FILE = "src/data/chunks/text_chunks.jsonl"
OUT_EMB = "src/data/chunks/embeddings.npy"
OUT_META = "src/data/chunks/metadata.json"
MODEL_NAME = "BAAI/bge-small-en-v1.5" # used bge-small model from BAAI as it is performing well on text embeddings
#MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # used bge-small model from BAAI as it is performing well on text embeddings

LOG_DIR = "src/logs"
LOG_FILE = os.path.join(LOG_DIR,"embeddings.log")
STOP_AFTER_ID = "c7475e1d98f9a46a4652e503881d4a67232b41d3.pdf_407" # the embedding will be generated till this chunk ID (for demo purpose)

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
    handlers = [
        logging.FileHandler(LOG_FILE, encoding = "utf-8")
    ]
)

logger = logging.getLogger(__name__)

class Embedder:
    def __init__(self):
        self.config = get_config()
        self.model_name = self.config.embedding_model
        self.dimension = self.config.get('embeddings.dimension', 384)
        self.model = self._load_model()
    
    def _load_model(self):
        """Load embedding model from config"""
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedder: {self.model_name}")
            return SentenceTransformer(self.model_name)
        except Exception as e:
            logger.error(f"Error loading embedder: {e}")
            raise EmbeddingError(f"Cannot load {self.model_name}: {str(e)}")
    
    def encode(self, texts):
        """Encode texts to embeddings"""
        try:
            return self.model.encode(texts, convert_to_numpy=True)
        except Exception as e:
            logger.error(f"Encoding error: {e}")
            raise EmbeddingError(f"Encoding failed: {str(e)}")

def generate_embeddings():
    start_time = time.time()
    logger.info("Embedding generation started")
    
    texts, metadatas, ids = [], [], []

    try:
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                cid = r["chunk_id"].strip() # removing any leading/trailing spaces

                texts.append(r["text"])
                metadatas.append(r["metadata"]) # metadata associated with the chunk
                ids.append(cid)
                # used resumable embedding as the total chunks are 74223
                if cid == STOP_AFTER_ID:
                    logger.info(f"Stopped at chunk ID: {cid}")
                    break

        logger.info(f"Last loaded chunk ID: {ids[-1]}")
        logger.info(f"Total chunks loaded: {len(texts)}")

        model = SentenceTransformer(MODEL_NAME)
        logger.info(f"Model {MODEL_NAME} loaded")

        embeddings = model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        np.save(OUT_EMB, embeddings)
        logger.info(f"Embeddings saved to {OUT_EMB}")
    
        with open(OUT_META, "w", encoding="utf-8") as f:
            json.dump(
                {"ids": ids,"text":texts, "metadatas": metadatas},
                f,
                ensure_ascii=False,
                indent=2
            )
        logger.info(f"Metadata saved to {OUT_META}")
        logger.info(f"Embedding generation completed in {time.time() - start_time:.2f}s")

        return embeddings, ids, metadatas

    except Exception as e:
        logger.exception(f"Error during embedding generation")
        raise

if __name__ == "__main__":
    generate_embeddings()



