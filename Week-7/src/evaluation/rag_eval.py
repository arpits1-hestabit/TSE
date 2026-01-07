from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset
from transformers import pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
import json


def evaluate_faithfulness(
    question: str,
    sql_results: list,
    answer: str,
    llm,
    embeddings
):
    context = json.dumps(sql_results, indent=2)

    dataset = Dataset.from_dict({
        "question": [question],
        "answer": [answer],
        "contexts": [[context]]
    })

    text_gen_pipeline = pipeline(
        "text-generation",
        model=llm,
        tokenizer=llm.config._name_or_path,
        max_new_tokens=256,
        temperature=0
    )

    ragas_llm = HuggingFacePipeline(pipeline=text_gen_pipeline)

    ragas_embeddings = HuggingFaceEmbeddings(
        model_name=embeddings.model_name
    )

    scores = evaluate(
        dataset=dataset,
        metrics=[faithfulness],
        llm=ragas_llm,
        embeddings=ragas_embeddings
    )

    faithfulness_score = scores["faithfulness"][0]

    return {
        "faithfulness": round(float(faithfulness_score), 3),
        "hallucinated": faithfulness_score < 0.7
    }
