from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.llm.model_loader import load_cached_model_and_embeddings
from src.retriever.text_search import TextSearcher
from src.retriever.image_search import ImageSearcher
from src.pipelines.sql_pipeline import SQLPipeline
from src.generator.sql_generator import SQLGenerator


import sqlite3

def load_db_schema(db_path="data/app.db") -> str:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT sql FROM sqlite_master
        WHERE type='table' AND name='documents'
    """)
    row = cur.fetchone()
    conn.close()

    if not row:
        raise RuntimeError("documents table not found in database")

    return row[0]

# initializing the app
app = FastAPI(
    title="Enterprise RAG System",
    version="1.0.0"
)

# laoding the model and embeddings
model, tokenizer, embeddings = load_cached_model_and_embeddings()

text_searcher = TextSearcher(
    vector_dir="src/data/chunks"
)


image_searcher = ImageSearcher(
    embeddings_path="src/vectorstore/images/embeddings.npy",
    captions_path="src/vectorstore/images/captions.jsonl"
)

sql_pipeline = SQLPipeline(
    db_path="data/app.db",
    llm=model,
    embeddings=embeddings
)

sql_generator = SQLGenerator()

schema = load_db_schema("data/app.db")

# request and response models
class AskRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class AskImageRequest(BaseModel):
    query: Optional[str] = None
    mode: str
    top_k: Optional[int] = 5


class AskSQLRequest(BaseModel):
    question: str


# for checking if the api is working
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "RAG + Image + SQL API is running"
    }



@app.post("/ask")
def ask_endpoint(request: dict):
    query = request.get("query")
    results = text_searcher.search(query, top_k=5)
    return {"results": results}


@app.post("/ask-image")
def ask_image(
    request: AskImageRequest,
    image: UploadFile = File(None)
):
    
    mode = request.mode.lower()

    if mode == "text_to_image":
        if not request.query:
            raise HTTPException(400, "Query required")
        results = image_searcher.text_to_image(
            request.query, request.top_k
        )
        return {"results": results}

    if mode == "text_to_text":
        if not request.query:
            raise HTTPException(400, "Query required")
        results = image_searcher.text_to_text(
            request.query, request.top_k
        )
        return {"results": results}

    if mode in ["image_to_image", "image_to_text"]:
        if image is None:
            raise HTTPException(400, "Image file required")

        image_path = f"/tmp/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())

        if mode == "image_to_image":
            results = image_searcher.image_to_image(
                image_path, request.top_k
            )
            return {"results": results}

        if mode == "image_to_text":
            result = image_searcher.image_to_text(
                image_path, request.top_k
            )
            return result

    raise HTTPException(400, "Invalid mode")

@app.post("/ask-sql")
async def ask_sql(payload: dict):
    question = payload.get("question")
    if not question:
        return {"error": "No question provided"}

    schema = load_db_schema("data/app.db")

    sql_query = sql_generator.generate_sql(question, schema)

    conn = sqlite3.connect("data/app.db")
    cur = conn.cursor()

    results = []
    executed_statements = []
    try:
        #splitting multiple statements usign the semicolon
        statements = [stmt.strip() for stmt in sql_query.split(";") if stmt.strip()]

        for stmt in statements:
            cur.execute(stmt)
            executed_statements.append(stmt)
            # Only fetch rows for SELECT statements
            if stmt.lower().startswith("select"):
                results.extend(cur.fetchall())

        conn.commit()
        summary = f"Executed {len(executed_statements)} statement(s), fetched {len(results)} rows."
        explanation = "Executed SQL statements:\n" + "\n".join(executed_statements)

    except sqlite3.Error as e:
        # fixing the sql query using llm
        fixed_sql = sql_generator.fix_sql(sql_query, schema, str(e))
        summary = "Execution failed"
        explanation = f"SQL Error: {e}\nAttempted fixed SQL: {fixed_sql}"
        sql_query = fixed_sql
        results = []

    finally:
        conn.close()

    return {
        "sql": sql_query,
        "results": results,
        "summary": summary,
        "explanation": explanation
    }
