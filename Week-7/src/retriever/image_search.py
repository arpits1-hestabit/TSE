import json
import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
from typing import List, Dict

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
