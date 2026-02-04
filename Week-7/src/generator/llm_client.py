import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Optional, List, Dict
from src.config.config import get_config
from src.utils.logger import get_logger
from src.utils.errors import GenerationError

logger = get_logger(__name__)

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained( MODEL_NAME, device_map="auto",dtype = "auto")


def generate(prompt: str, max_tokens: int = 512) -> str:
    messages = f"{prompt}"
    inputs = tokenizer( messages, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    if decoded.startswith(prompt):
        return decoded[len(prompt):].strip()

    return decoded.strip()

class LLMClient:
    # System prompts for different tasks
    SYSTEM_PROMPTS = {
        "rag": """You are a helpful assistant answering questions based on provided context.
Always cite the source when answering. If the answer is not in the context, say "I don't have enough information to answer this question."
Be concise and factual.""",
        
        "sql": """You are a SQL expert. Generate only valid SQL queries based on the schema provided.
Do not include markdown formatting, explanations, or comments unless explicitly asked.
Return only the SQL code.""",
        
        "summarization": """You are a document summarizer. Provide concise, factual summaries.
Focus on key points and maintain accuracy. Keep summaries under 200 words.""",
        
        "code_generation": """You are a code generation expert. Generate clean, well-documented code.
Follow best practices and include necessary error handling."""
    }
    
    def __init__(self, model_name: Optional[str] = None):
        self.config = get_config()
        self.model_name = model_name or self.config.model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load LLM model with error handling"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            logger.info(f"✓ Model loaded: {self.model_name}")
            
        except Exception as e:
            logger.error(f"✗ Error loading model: {e}")
            raise GenerationError(f"Failed to load model {self.model_name}: {str(e)}")
    
    def generate(self,
                prompt: str,
                system_role: str = "rag",
                max_tokens: Optional[int] = None,
                temperature: float = None) -> str:
        """
        Generate response with system prompt and chat template.
        
        Args:
            prompt: User prompt
            system_role: Type of task (rag, sql, summarization, etc.)
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
        
        Returns:
            Generated response
        """
        try:
            if self.model is None:
                raise GenerationError("Model not loaded")
            
            max_tokens = max_tokens or self.config.get('model.max_tokens', 512)
            temperature = temperature or self.config.get('model.temperature', 0.7)
            
            system_prompt = self.SYSTEM_PROMPTS.get(system_role, self.SYSTEM_PROMPTS["rag"])
            
            # Format as chat conversation
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # Apply chat template
            formatted_prompt = self._apply_chat_template(messages)
            
            logger.debug(f"Generating with temperature={temperature}, max_tokens={max_tokens}")
            
            # Generate
            response = self._call_model(formatted_prompt, max_tokens, temperature)
            return response.strip()
            
        except GenerationError:
            raise
        except Exception as e:
            logger.error(f"✗ Error in generation: {e}")
            raise GenerationError(f"Generation failed: {str(e)}")
    
    def _apply_chat_template(self, messages: List[Dict[str, str]]) -> str:
        """Apply chat template based on model type"""
        try:
            if "mistral" in self.model_name.lower():
                # Mistral chat format
                formatted = "[INST] "
                for msg in messages:
                    if msg['role'] == 'system':
                        formatted += f"<s>{msg['content']}\n"
                    elif msg['role'] == 'user':
                        formatted += f"{msg['content']}"
                formatted += " [/INST]"
                return formatted
            
            elif "llama" in self.model_name.lower():
                # Llama2 format
                formatted = ""
                for msg in messages:
                    if msg['role'] == 'system':
                        formatted += f"<<SYS>>\n{msg['content']}\n<</SYS>>\n\n"
                    elif msg['role'] == 'user':
                        formatted += f"[INST] {msg['content']} [/INST]"
                return formatted
            
            else:
                # Generic format
                return "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in messages])
        
        except Exception as e:
            logger.error(f"✗ Error applying template: {e}")
            raise GenerationError(f"Template error: {str(e)}")
    
    def _call_model(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Call the actual model"""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=self.config.get('model.top_p', 0.9),
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        
        except Exception as e:
            logger.error(f"✗ Model call error: {e}")
            raise GenerationError(f"Model error: {str(e)}")
    
    def rag_generate(self, question: str, context: str) -> str:
        """Generate RAG response with context"""
        prompt = f"""Context:
{context}

Question: {question}

Answer:"""
        return self.generate(prompt, system_role="rag")
    
    def sql_generate(self, query: str, schema: str) -> str:
        """Generate SQL from natural language"""
        prompt = f"""Database Schema:
{schema}

Generate SQL for: {query}"""
        return self.generate(prompt, system_role="sql", max_tokens=256)
    
    def summarize(self, text: str) -> str:
        """Summarize text"""
        return self.generate(text, system_role="summarization", max_tokens=256)