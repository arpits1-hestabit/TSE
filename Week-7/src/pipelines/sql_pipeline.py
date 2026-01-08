# src/pipelines/sql_pipeline.py

import sqlite3
from src.generator.sql_generator import SQLGenerator
from src.memory.memory_store import MemoryStore
from src.evaluation.rag_eval import evaluate_faithfulness

class SQLPipeline:
    def __init__(self, db_path: str, llm=None, embeddings=None):
        self.db_path = db_path
        self.generator = SQLGenerator()
        self.llm = llm
        self.embeddings = embeddings

    def run(self, question: str, schema: str = "", memory: MemoryStore = None):
        
        sql_query = self.generator.generate_sql(
            question=question,
            schema=schema,
            memory=memory
        )

        results = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            for row in rows:
                results.append(dict(zip(columns, row)))
            conn.close()
        except Exception as e:
            results = []
            print(f"{e}")

        
        explanation = f"Executed SQL: {sql_query}"
        summary = f"Returned {len(results)} rows."

        faithfulness = None
        hallucinated = None
        if self.llm and self.embeddings:
            try:
                eval_result = evaluate_faithfulness.evaluate_faithfulness(
                    question=question,
                    sql_results=results,
                    answer=explanation,
                    llm=self.llm,
                    embeddings=self.embeddings
                )
                faithfulness = eval_result["faithfulness"]
                hallucinated = eval_result["hallucinated"]
            except Exception as e:
                print(f"{e}")

    
        return {
            "sql": sql_query,
            "results": results,
            "summary": summary,
            "explanation": explanation,
            "faithfulness": faithfulness,
            "hallucinated": hallucinated
        }
