import os
import json
import numpy as np
from tqdm import tqdm
from pathlib import Path
from src.config.config import get_config
from src.utils.logger import get_logger
from src.vectorstore.index_manager import IndexManager
from src.embeddings.clip_embedder import CLIPEmbedder
from src.generator.indexer import FAISSIndexer

logger = get_logger(__name__)

IMAGE_ROOT = "src/data/raw/EnterpriseRAG_2025_02_markdown"
VECTOR_DIR = "src/vectorstore/images/"

def collect_images(root):
    image_paths = []
    for root_dir, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                image_paths.append(os.path.join(root_dir, f))
    return image_paths

class ImageIngestor:
    def __init__(self):
        self.config = get_config()
        self.embedder = CLIPEmbedder(
            vector_dir=VECTOR_DIR
        )
        self.indexer = FAISSIndexer()
        self.index_manager = IndexManager()
        self.images_dir = self.config.images_dir
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def ingest(self, images: list) -> bool:
        """
        Ingest image embeddings
        
        Args:
            images: List of dicts with 'id', 'path', 'caption'
        """
        try:
            logger.info(f"Ingesting {len(images)} images...")
            
            embeddings_list = []
            captions_data = []
            
            for img in images:
                try:
                    # Embed image
                    embedding = self.embedder.embed_image(img['path'])
                    embeddings_list.append(embedding)
                    
                    # Save caption
                    captions_data.append({
                        "image_id": img['id'],
                        "caption": img.get('caption', ''),
                        "source": img.get('source')
                    })
                except Exception as e:
                    logger.warning(f"Skipping image {img['id']}: {e}")
                    continue
            
            if not embeddings_list:
                logger.error("No images were processed")
                return False
            
            # Create and save index
            embeddings = np.array(embeddings_list)
            self.indexer.create_index(embeddings)
            self.indexer.save()
            
            # Save captions using config path
            captions_file = self.images_dir / "captions.jsonl"
            with open(captions_file, 'w') as f:
                for caption in captions_data:
                    f.write(json.dumps(caption) + '\n')
            
            logger.info(f"✓ Image ingestion complete: {len(embeddings)} images")
            return True
        
        except Exception as e:
            logger.error(f"✗ Image ingestion error: {e}")
            return False

def ingest_images():
    os.makedirs(VECTOR_DIR, exist_ok=True)

    embedder = CLIPEmbedder(
        vector_dir=VECTOR_DIR
    )

    image_paths = collect_images(IMAGE_ROOT)
    print(f"Found {len(image_paths)} images")

    for img_path in tqdm(image_paths, desc="Processing images", unit="img"):
        try:
            embedder.process_single_image(img_path)
        except Exception as e:
            print(f"Failed: {img_path} | {e}")

    print("Image ingestion complete")

if __name__ == "__main__":
    ingest_images()