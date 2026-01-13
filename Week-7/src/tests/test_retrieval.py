from retriever.hybrid_retriever import HybridRetriever
from pipelines.context_builder import ContextBuilder
from generator.llm_client import generate

def ask_retrieval(query: str):
    top_k = 5
    filters = {
        # leave empty if not needed
    }

    retriever = HybridRetriever(
        index_path="src/vectorstore/images/faiss.index",
        metadata_path="src/data/chunks/metadata.jsonl",
    )

    results = retriever.search(
        query=query,
        top_k=top_k,
        filters=filters
    )

    context_payload = ContextBuilder().build(results)

    final_prompt = f"""
You are a helpful and factual assistant.

Use ONLY the context below to answer the question.
If the answer is not present, say "I don't know".

Context:
{context_payload['context'][:1000]}

Question:
{query}

Answer:
"""
    answer = generate(final_prompt)

    return {
        "query": query,
        "answer": answer.strip(),
        "context": context_payload['context'][:1000]
    }   