import json
import numpy as np
from pathlib import Path
from src.config.config import get_config
from src.utils.logger import get_logger
from src.vectorstore.index_manager import IndexManager
from src.embeddings.embedder import Embedder
from src.generator.indexer import FAISSIndexer

logger = get_logger(__name__)

class TextIngestor:
    def __init__(self):
        self.config = get_config()
        self.embedder = Embedder()
        self.indexer = FAISSIndexer()
        self.index_manager = IndexManager()
    
    def ingest(self, documents: list) -> bool:
        """
        Ingest documents and save to config-based paths
        
        Args:
            documents: List of documents with 'id' and 'text'
        """
        try:
            logger.info(f"Ingesting {len(documents)} documents...")
            
            # Embed documents
            texts = [doc.get('text', '') for doc in documents]
            embeddings = self.embedder.encode(texts)
            
            # Create index
            self.indexer.create_index(embeddings)
            
            # Save index using config path
            self.indexer.save()
            
            # Save metadata
            for i, doc in enumerate(documents):
                self.index_manager.add_metadata(str(i), {
                    "id": doc.get('id'),
                    "text": doc.get('text'),
                    "source": doc.get('source')
                })
            
            self.index_manager.save_metadata()
            logger.info(f"✓ Ingestion complete: {len(documents)} docs saved")
            return True
        
        except Exception as e:
            logger.error(f"✗ Ingestion error: {e}")
            return False
    
    def ingest_from_file(self, file_path: str) -> bool:
        """Ingest from JSON file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            with open(file_path, 'r') as f:
                documents = json.load(f)
            
            return self.ingest(documents)
        except Exception as e:
            logger.error(f"✗ File ingestion error: {e}")
            return False