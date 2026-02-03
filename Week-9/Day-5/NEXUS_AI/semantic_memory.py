import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SemanticMemory:
    """
    Persistent semantic memory using sentence embeddings and FAISS.

    This class:
    - Encodes text using a SentenceTransformer model(all-MiniLM-L6-v2)
    - Stores embeddings in a FAISS index for fast similarity search
    - Persists both embeddings and raw text to disk
    - Allows retrieval of past (query, response) pairs via semantic search

    Use case:
    - Long-term memory for agents
    - Context retrieval for LLM prompting
    """

    def __init__(self):
        """
        Initialize the semantic memory system.

        - Creates storage directory if missing
        - Loads embedding model
        - Initializes FAISS index
        - Loads previously stored memory from disk (if available)
        """

        # Directory for persisting memory files
        self.memory_dir = "memory_store"
        os.makedirs(self.memory_dir, exist_ok=True)

        # File paths for FAISS index and stored text
        self.index_path = os.path.join(self.memory_dir, "faiss.index")
        self.text_path = os.path.join(self.memory_dir, "memory.pkl")

        # Sentence embedding model
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

        # Embedding dimension for MiniLM model
        self.dim = 384

        # FAISS index using L2 (Euclidean) distance
        self.index = faiss.IndexFlatL2(self.dim)

        # List to store original text corresponding to embeddings
        self.text_data = []

        # Load existing memory if present on disk
        self.load()

    def add(self, query: str, response: str):
        """
        Add a new (query, response) pair to semantic memory.

        The query and response are combined, embedded, and stored
        in the FAISS index along with the original text.

        Args:
            query (str): User input or question
            response (str): Generated or stored response
        """

        # Combine query and response into a single text block
        text = f"Q: {query}\nA: {response}"

        # Generate embedding and convert to float32 (FAISS requirement)
        embedding = self.encoder.encode([text])
        embedding = np.array(embedding).astype("float32")

        # Add embedding to FAISS index
        self.index.add(embedding)

        # Store raw text for retrieval
        self.text_data.append(text)

        # Persist memory to disk
        self.save()

    def search(self, query: str, k: int = 3):
        """
        Search semantic memory for relevant past entries.

        Args:
            query (str): Search query
            k (int): Number of top matches to return

        Returns:
            list[str]: Top-k semantically similar memory entries
        """

        # Return empty list if no memory exists
        if len(self.text_data) == 0:
            return []

        # Encode search query
        query_embedding = self.encoder.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        # Perform similarity search in FAISS index
        distances, indices = self.index.search(query_embedding, k)

        # Collect matching texts
        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.text_data[idx])

        return results

    def save(self):
        """
        Persist FAISS index and stored text data to disk.
        This allows semantic memory to survive application restarts.
        """

        # Save FAISS index
        faiss.write_index(self.index, self.index_path)

        # Save associated text data
        with open(self.text_path, "wb") as f:
            pickle.dump(self.text_data, f)

    def load(self):
        """
        Load FAISS index and stored text data from disk if available.
        If files are missing, a fresh empty memory is used.
        """

        # Load FAISS index if present
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

        # Load stored text data if present
        if os.path.exists(self.text_path):
            with open(self.text_path, "rb") as f:
                self.text_data = pickle.load(f)
