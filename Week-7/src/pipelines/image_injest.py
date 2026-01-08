import os
from tqdm import tqdm
from src.embeddings.clip_embedder import CLIPEmbedder

IMAGE_ROOT = "src/data/raw/EnterpriseRAG_2025_02_markdown"
VECTOR_DIR = "src/vectorstore/images/"

def collect_images(root):
    image_paths = []
    for root_dir, _, files in os.walk(root):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                image_paths.append(os.path.join(root_dir, f))
    return image_paths

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