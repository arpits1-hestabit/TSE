from sentence_transformers import SentenceTransformer
import faiss
import json
import os
import numpy as np
from src.config.config import get_config
from src.utils.logger import get_logger
from src.utils.errors import RetrievalError
from src.vectorstore.index_manager import IndexManager

logger = get_logger(__name__)


class TextSearcher:
    def __init__(self):
        self.config = get_config()
        self.index_manager = IndexManager()
        self.index_manager.load_index()
        self.index_manager.load_metadata()

    def search(self, query_embedding: np.ndarray, top_k: int = None):
        """
        Search using config-based index path

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results (uses config default if None)

        Returns:
            Tuple of (distances, indices, metadata)
        """
        try:
            top_k = top_k or self.config.get('retrieval.top_k', 5)

            # Ensure proper shape
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)

            distances, indices = self.index_manager.search(
                query_embedding.astype('float32'),
                top_k
            )

            # Get metadata for results
            results = []
            for idx in indices[0]:
                if idx >= 0:
                    metadata = self.index_manager.get_by_id(str(idx))
                    results.append({
                        "index": int(idx),
                        "distance": float(distances[0][len(results)]),
                        "metadata": metadata
                    })

            logger.info(f"✓ Text search found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"✗ Text search error: {e}")
            raise RetrievalError(f"Text search failed: {str(e)}")

    def batch_search(self, query_embeddings: np.ndarray, top_k: int = None):
        """Batch search multiple queries"""
        try:
            results = []
            for embedding in query_embeddings:
                result = self.search(embedding, top_k)
                results.append(result)
            return results
        except Exception as e:
            logger.error(f"✗ Batch search error: {e}")
            raise RetrievalError(f"Batch search failed: {str(e)}")
