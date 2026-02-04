import faiss
import json
import numpy as np
import torch
from pathlib import Path
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict

from src.config.config import get_config
from src.utils.logger import get_logger
from src.utils.errors import RetrievalError

logger = get_logger(__name__)

class ImageSearcher:
    def __init__(
        self,
        embeddings_path: str = "src/vectorstore/images/embeddings.npy",
        captions_path: str = "src/vectorstore/images/captions.jsonl",
        device: str | None = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # CLIP model and processor
        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        ).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )
        self.model.eval()

        # Embeddings
        self.embeddings = np.load(embeddings_path)
        self.embeddings = self._normalize(self.embeddings)

        # Captions
        self.metadata = []
        with open(captions_path, "r", encoding="utf-8") as f:
            for line in f:
                self.metadata.append(json.loads(line))

        assert len(self.embeddings) == len(self.metadata), (
            "Embeddings and captions count mismatch"
        )

        print(f"Loaded {len(self.embeddings)} image embeddings")


    def _normalize(self, x: np.ndarray) -> np.ndarray:
        return x / np.linalg.norm(x, axis=1, keepdims=True)

    def _embed_text(self, query: str) -> np.ndarray:
        inputs = self.processor(
            text=query, return_tensors="pt", padding=True
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_text_features(**inputs)

        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()[0]


    def search(
        self,
        query: str,
        top_k: int = 5,
        ocr_filter: str | None = None,
    ) -> List[Dict]:
    

        query_vec = self._embed_text(query)

        # cosine similarity
        scores = np.dot(self.embeddings, query_vec)

        ranked_idx = np.argsort(scores)[::-1]

        results = []
        for idx in ranked_idx:
            item = self.metadata[idx]

            # ocr filter
            if ocr_filter:
                if ocr_filter.lower() not in item.get("ocr_text", "").lower():
                    continue

            results.append({
                "score": float(scores[idx]),
                "image_path": item["image_path"],
                "caption": item.get("caption", ""),
                "ocr_text": item.get("ocr_text", ""),
            })

            if len(results) >= top_k:
                break

        return results
    
    def _load_captions(self) -> dict:
        """Load image captions from config path"""
        try:
            if not self.captions_file.exists():
                logger.warning(f"Captions file not found: {self.captions_file}")
                return {}
            
            captions = {}
            with open(self.captions_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    captions[data['image_id']] = data['caption']
            
            logger.info(f"✓ Loaded {len(captions)} image captions")
            return captions
        except Exception as e:
            logger.error(f"✗ Error loading captions: {e}")
            return {}
    
    def search(self, image_embedding: np.ndarray, top_k: int = None):
        """Search images using config paths"""
        try:
            top_k = top_k or self.config.get('retrieval.top_k', 5)
            
            # Load image index
            from src.vectorstore.index_manager import IndexManager
            manager = IndexManager()
            manager.load_index()
            
            distances, indices = manager.search(image_embedding, top_k)
            
            results = []
            for idx in indices[0]:
                if idx >= 0:
                    image_id = str(idx)
                    caption = self.captions.get(image_id, "No caption")
                    image_path = self.images_dir / f"{image_id}.jpg"
                    
                    results.append({
                        "image_id": image_id,
                        "distance": float(distances[0][len(results)]),
                        "caption": caption,
                        "path": str(image_path)
                    })
            
            logger.info(f"✓ Image search found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"✗ Image search error: {e}")
            raise RetrievalError(f"Image search failed: {str(e)}")
