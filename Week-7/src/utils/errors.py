class RAGError(Exception):
    """Base exception for RAG system"""
    pass

class IndexLoadError(RAGError):
    """Raised when FAISS index fails to load"""
    pass

class IndexSaveError(RAGError):
    """Raised when saving FAISS index fails"""
    pass

class MetadataError(RAGError):
    """Raised when metadata operations fail"""
    pass

class EmbeddingError(RAGError):
    """Raised when embedding generation fails"""
    pass

class RetrievalError(RAGError):
    """Raised when retrieval fails"""
    pass

class GenerationError(RAGError):
    """Raised when LLM generation fails"""
    pass

class ConfigError(RAGError):
    """Raised when configuration is invalid"""
    pass

class DatabaseError(RAGError):
    """Raised when database operations fail"""
    pass