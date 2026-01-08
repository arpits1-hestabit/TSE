# SQL Question Answering

Natural language to SQL conversion with error recovery.

## Architecture

```
Natural Language Question
    ↓
Schema Loading (DB structure)
    ↓
SQL Generation (Qwen LLM)
    ↓
Execute on SQLite
    ↓
├─ Success → Results
├─ Error → Fix SQL → Retry
└─ No Results → Return Empty
    ↓
Explain Results (Natural Language)
    ↓
Evaluate Faithfulness (RAGAs)
    ↓
Final Answer
```

## Components

### 1. SQL Generator

**Model**: Qwen2.5-1.5B-Instruct (1.5B params, FP16)

Used `Qwen model` for the conversion of natural language to sql query.

### 2. Schema Loader

```python
def load_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sql FROM sqlite_master
        WHERE type='table'
    """)
    
    schema = "\n".join(row[0] for row in cursor.fetchall())
    return schema
```

**Example Schema**:
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
```

### 3. Prompts

**SQL Generation** (`sql_generation.txt`):
```
You are an expert SQL generator.

Rules:
- Output ONLY valid SQL
- Do NOT explain anything
- Use ONLY tables and columns in schema
- If unsure, output: INVALID_SQL

Schema:
{schema}

Question:
{question}

SQL:
```

**SQL Fixing** (`sql_invalid.txt`):
```
The following SQL failed.

Schema: {schema}
SQL: {sql}
Error: {error}

Return FIXED SQL query only.
```

**Result Explanation** (`sql_explain.txt`):
```
Question: {question}
SQL: {sql}
Result: {result}

Explain in simple language.
```

## Workflow

### Basic Flow

```
1. Generate SQL
2. Execute
3. Fix and retry
4. Explain
```

```python
def run(question, schema):
    # 1. Generate SQL
    sql = generator.generate_sql(question, schema)
    
    # 2. Execute
    try:
        results = execute_sql(sql)
    except Exception as e:
        # 3. Fix and retry
        sql = generator.fix_sql(sql, schema, str(e))
        results = execute_sql(sql)
    
    # 4. Explain
    explanation = generator.explain_result(question, sql, results)
    
    return {
        "sql": sql,
        "results": results,
        "explanation": explanation
    }
```

### Error Recovery

```python
# Attempt 1: Generate SQL
sql = "SELECT * FROM employes"  # Typo!

# Execute → Error: "no such table: employes"

# Attempt 2: Fix SQL
fixed_sql = generator.fix_sql(
    sql=sql,
    schema=schema,
    error="no such table: employes"
)
# Output: "SELECT * FROM employees"

# Execute → Success!
```

**Max retries**: 2 attempts

## Examples

### Example 1: Simple Query

**Question**: "How many employees are there?"

**Generated SQL**:
```sql
SELECT COUNT(*) as count FROM employees
```

**Results**:
```json
[{"count": 150}]
```

**Explanation**: "There are 150 employees in the database."

### Example 2: Filtered Query

**Question**: "What's the average salary in Engineering?"

**Generated SQL**:
```sql
SELECT AVG(salary) as avg_salary 
FROM employees 
WHERE department = 'Engineering'
```

**Results**:
```json
[{"avg_salary": 95000}]
```

**Explanation**: "The average salary in the Engineering department is $95,000."

### Example 3: Join Query

**Question**: "Show me employees and their department budgets"

**Generated SQL**:
```sql
SELECT e.name, e.department, d.budget
FROM employees e
JOIN departments d ON e.department = d.dept_name
LIMIT 10
```

### Example 4: Error Recovery

**Question**: "List all products"

**Attempt 1** (WRONG):
```sql
SELECT * FROM product
```
**Error**: "no such table: product"

**Attempt 2** (FIXED):
```sql
SELECT * FROM products
```
**Success**: Returns product list

## Conversation Memory

Enables follow-up questions:

```python
memory = MemoryStore(k=5)

# First question
memory.add_user("What's the total revenue?")
memory.add_ai("Total revenue is $2.5M")

# Follow-up uses context
memory.add_user("How about last quarter?")
# Memory provides context: previous question was about revenue
```

**Memory Format**:
```
user: What's the total revenue?
ai: Total revenue is $2.5M
user: How about last quarter?
```

## Evaluation

**Framework**: RAGAS Faithfulness

```python
def evaluate(question, sql_results, answer):
    score = ragas_evaluate(
        question=question,
        contexts=[json.dumps(sql_results)],
        answer=answer
    )
    
    return {
        "faithfulness": score,
        "hallucinated": score < 0.7
    }
```

**Faithfulness score**:
- 1.0 = Fully grounded in data
- 0.7-1.0 = Acceptable
- <0.7 = Potential hallucination


### Error Handling

```python
# Handle common errors
try:
    results = cursor.execute(sql)
except sqlite3.OperationalError as e:
    # Syntax error, missing table/column
    sql = fix_sql(sql, schema, str(e))
except sqlite3.DatabaseError as e:
    # Database locked, etc.
    retry_with_backoff()
```

