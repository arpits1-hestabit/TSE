# Multimodal RAG

Image search and processing in the RAG system.

## Overview

Three-component system for visual search:
1. **CLIP**: Visual embeddings
2. **BLIP**: Image captions
3. **Tesseract**: OCR text extraction

## Architecture

```
                  Image Input
                      ↓
┌───────────────┬──────────────┬─────────────┐
│ CLIP Embedding│ BLIP Caption │ OCR Extract │
└───────────────┴──────────────┴─────────────┘
    ↓                 ↓               ↓
    └─────────────────┴───────────────┘
                      ↓
              Store in Vector DB
                      ↓
         Text Query → CLIP Search → Images
```

## 1. CLIP Embeddings

**Model**: `openai/clip-vit-base-patch32`

**What it does**: Maps images and text to same 512-dim space

```
# Image embedding
image = Image.open("photo.jpg")
image_vec = clip_model.get_image_features(image)
image_vec = normalize(image_vec)  # L2 norm

# Text embedding
query = "team meeting in conference room"
text_vec = clip_model.get_text_features(query)
text_vec = normalize(text_vec)

# Similarity
score = cosine_similarity(text_vec, image_vec)
```

**Key feature**: Zero-shot - no training needed for new domains

## 2. BLIP Captioning

**Model**: `Salesforce/blip-image-captioning-base`

**What it does**: Generates natural language descriptions

```
image = Image.open("diagram.png")
caption = blip_model.generate(image, max_tokens=30)
# Output: "a diagram showing database architecture with connections"
```

**Why add captions?**
- Improves searchability
- Provides context
- Makes images accessible

## 3. OCR Integration

**Tool**: Tesseract

**What it does**: Extracts text from images

```
text = pytesseract.image_to_string(image)
```

**Use cases**:
- Screenshots with error messages
- Diagrams with labels
- Scanned documents
- Presentations with text

## Image Ingestion Pipeline

```
# Process all images in directory
for image_path in image_files:
    image = Image.open(image_path).convert("RGB")
    
    # 1. Generate CLIP embedding
    embedding = clip_embed(image)
    
    # 2. Generate caption
    caption = blip_caption(image)
    
    # 3. Extract OCR text
    ocr_text = tesseract_ocr(image)
    
    # 4. Store
    save({
        "path": image_path,
        "embedding": embedding,
        "caption": caption,
        "ocr_text": ocr_text
    })
```

## Image Search

### Basic Search

```
searcher = ImageSearcher(
    embeddings_path="vectorstore/images/embeddings.npy",
    captions_path="vectorstore/images/captions.jsonl"
)

# Text-to-image search
results = searcher.search("architecture diagram", top_k=5)
```

### OCR Filtering

```
# Find images containing specific text
results = searcher.search(
    query="error message",
    top_k=5,
    ocr_filter="404"  # Only images with "404" in OCR text
)
```

### How Search Works

```
def search(query, top_k=5):
    # 1. Encode query with CLIP
    query_vec = clip_text_encoder(query)
    
    # 2. Compute cosine similarity
    scores = dot_product(image_embeddings, query_vec)
    
    # 3. Rank by score
    ranked_indices = argsort(scores, descending=True)
    
    # 4. Return top-k
    return [images[i] for i in ranked_indices[:top_k]]
```

## Limitations

1. **CLIP**: Limited to training distribution, struggles with fine details
2. **BLIP**: Generic captions, may miss technical terms
3. **OCR**: Poor accuracy on low-res or handwritten text
4. **Scale**: Current setup works for 1K-10K images
