import os
import json
import torch
import numpy as np
import pytesseract
from PIL import Image
from transformers import (
    CLIPProcessor, CLIPModel,
    BlipProcessor, BlipForConditionalGeneration
)

class CLIPEmbedder:
    def __init__(self, vector_dir):
        self.vector_dir = vector_dir
        os.makedirs(vector_dir, exist_ok=True)

        self.embeddings_path = os.path.join(vector_dir, "embeddings.npy")
        self.captions_path = os.path.join(vector_dir, "captions.jsonl")

        # using CLIP for embeddings
        self.clip_model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )
        self.clip_processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        # using BLIP for captions
        self.blip_processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.blip_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        self.clip_model.eval()
        self.blip_model.eval()

        # storage for embeddings and captions
        self.embeddings = []
        self.captions = []

    # tesseract OCR extraction
    def extract_ocr(self, image):
        text = pytesseract.image_to_string(image)
        return text.strip()

    def generate_caption(self, image):
        inputs = self.blip_processor(image, return_tensors="pt")
        with torch.no_grad():
            out = self.blip_model.generate(**inputs, max_new_tokens=30)
        return self.blip_processor.decode(out[0], skip_special_tokens=True)

    def embed_image(self, image):
        inputs = self.clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            features = self.clip_model.get_image_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.squeeze().cpu().numpy()

    def process_single_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        embedding = self.embed_image(image)

        caption = self.generate_caption(image)

        ocr_text = self.extract_ocr(image)

        self.embeddings.append(embedding)
        self.captions.append({
            "image_path": image_path,
            "caption": caption,
            "ocr_text": ocr_text
        })

    def save(self):
        embeddings_array = np.vstack(self.embeddings)
        np.save(self.embeddings_path, embeddings_array)

        with open(self.captions_path, "w", encoding="utf-8") as f:
            for item in self.captions:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        print(f"Saved {len(self.embeddings)} embeddings")
