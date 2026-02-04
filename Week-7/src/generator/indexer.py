import json
import numpy as np
import faiss
from pathlib import Path
from src.config.config import get_config
from src.utils.logger import get_logger
from src.utils.errors import IndexSaveError

logger = get_logger(__name__)

embeddings_file = Path("src/vectorstore/images/embeddings.npy")
metadata_file = Path("src/data/chunks/metadata.jsonl")
index_file = Path("src/vectorstore/images/faiss.index")

class FAISSIndexer:
    def __init__(self):
        self.config = get_config()
        self.index = None
    
    def create_index(self, embeddings: np.ndarray, dimension: int = None):
        """Create FAISS index from embeddings"""
        try:
            dimension = dimension or self.config.get('embeddings.dimension', 384)
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            logger.info(f"✓ Index created with {self.index.ntotal} vectors")
            return True
        except Exception as e:
            logger.error(f"✗ Error creating index: {e}")
            raise IndexSaveError(f"Failed to create index: {str(e)}")
    
    def save(self):
        """Save index using config path"""
        try:
            if self.index is None:
                raise IndexSaveError("No index to save")
            
            index_path = self.config.index_path
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            faiss.write_index(self.index, str(index_path))
            logger.info(f"✓ Index saved to {index_path}")
            return True
        except Exception as e:
            logger.error(f"✗ Error saving index: {e}")
            raise IndexSaveError(f"Failed to save index: {str(e)}")

def main():
    embeddings = np.load(embeddings_file).astype("float32")

    with open(metadata_file, encoding="utf-8") as f:
        metadata = [json.loads(line) for line in f]

    dim = embeddings.shape[1]
    print(f"Embedding dimension: {dim}")
    print(f"Total vectors: {len(embeddings)}")  
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, str(index_file))


if __name__ == "__main__":
    main()