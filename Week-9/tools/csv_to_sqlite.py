import sqlite3
import pandas as pd
from pathlib import Path


def load_csv_to_sqlite(
    csv_path: str,
    db_path: str,
    table_name: str,
    if_exists: str = "replace"
):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Creating connection to SQLite database
    conn = sqlite3.connect(db_path)

    try:
        df.to_sql(
            table_name,
            conn,
            if_exists=if_exists,
            index=False
        )
    finally:
        conn.close()

    return {
        "table": table_name,
        "rows_inserted": len(df),
        "columns": list(df.columns)
    }


if __name__ == "__main__":
    result = load_csv_to_sqlite(
        csv_path="executed_code/sales.csv",
        db_path="executed_code/sales.db",
        table_name="sales"
    )

    print("CSV loaded successfully:")
    print(result)
