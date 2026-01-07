import sqlite3

def load_schema(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT sql FROM sqlite_master
        WHERE type='table'
    """)

    schema = "\n".join(row[0] for row in cur.fetchall())
    conn.close()
    return schema
