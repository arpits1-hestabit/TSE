from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.logger import get_logger
from src.utils.errors import EmbeddingError

logger = get_logger(__name__)

class RAGEvaluator:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
    
    def embedding_similarity(self, answer: str, context: str) -> float:
        """
        Calculate embedding cosine similarity between answer and context.
        Limited use - should not be sole evaluation metric.
        """
        try:
            answer_emb = self.embedding_model.encode([answer])
            context_emb = self.embedding_model.encode([context])
            similarity = cosine_similarity(answer_emb, context_emb)[0][0]
            return float(np.clip(similarity, 0.0, 1.0))
        except Exception as e:
            logger.error(f"✗ Error computing similarity: {e}")
            return 0.0
    
    def contextual_precision(self, answer: str, context_docs: List[str]) -> float:
        """
        Measure what fraction of context documents actually support the answer.
        Higher = more relevant context retrieved.
        """
        try:
            if not context_docs:
                return 0.0
            
            answer_emb = self.embedding_model.encode([answer])
            context_embs = self.embedding_model.encode(context_docs)
            
            similarities = cosine_similarity(answer_emb, context_embs)[0]
            # Count how many docs have high similarity
            precision = np.mean(similarities > 0.5)
            return float(np.clip(precision, 0.0, 1.0))
        
        except Exception as e:
            logger.error(f"✗ Error in precision calculation: {e}")
            return 0.0
    
    def contextual_recall(self, answer: str, context: str) -> float:
        """
        Measure what fraction of the answer is supported by context.
        Splits answer into sentences and checks each against context.
        """
        try:
            sentences = [s.strip() for s in answer.split('.') if s.strip()]
            
            if not sentences:
                return 0.0
            
            supported_count = 0
            for sentence in sentences:
                similarity = self.embedding_similarity(sentence, context)
                if similarity > 0.5:
                    supported_count += 1
            
            recall = supported_count / len(sentences)
            return float(np.clip(recall, 0.0, 1.0))
        
        except Exception as e:
            logger.error(f"✗ Error in recall calculation: {e}")
            return 0.0
    
    def answer_relevance(self, question: str, answer: str) -> float:
        """
        Basic relevance check: is answer related to the question?
        """
        try:
            question_emb = self.embedding_model.encode([question])
            answer_emb = self.embedding_model.encode([answer])
            
            relevance = cosine_similarity(question_emb, answer_emb)[0][0]
            return float(np.clip(relevance, 0.0, 1.0))
        
        except Exception as e:
            logger.error(f"✗ Error in relevance calculation: {e}")
            return 0.0
    
    def evaluate_rag(self,
                    question: str,
                    answer: str,
                    context: str,
                    context_docs: List[str]) -> Dict[str, float]:
        """
        Comprehensive RAG evaluation with multiple metrics.
        
        Returns dict with:
        - embedding_similarity: Answer-context similarity (0-1)
        - answer_relevance: Answer-question relevance (0-1)
        - contextual_precision: Fraction of relevant context (0-1)
        - contextual_recall: Fraction of answer supported by context (0-1)
        - overall_score: Weighted average (0-1)
        """
        try:
            logger.info("Starting RAG evaluation...")
            
            embedding_sim = self.embedding_similarity(answer, context)
            answer_rel = self.answer_relevance(question, answer)
            context_prec = self.contextual_precision(answer, context_docs)
            context_rec = self.contextual_recall(answer, context)
            
            # Weighted average
            overall = (
                embedding_sim * 0.15 +
                answer_rel * 0.25 +
                context_prec * 0.3 +
                context_rec * 0.3
            )
            
            results = {
                "embedding_similarity": round(embedding_sim, 3),
                "answer_relevance": round(answer_rel, 3),
                "contextual_precision": round(context_prec, 3),
                "contextual_recall": round(context_rec, 3),
                "overall_score": round(overall, 3)
            }
            
            logger.info(f"✓ Evaluation complete: {results}")
            return results
        
        except Exception as e:
            logger.error(f"✗ Evaluation error: {e}")
            return {
                "embedding_similarity": 0.0,
                "answer_relevance": 0.0,
                "contextual_precision": 0.0,
                "contextual_recall": 0.0,
                "overall_score": 0.0
            }