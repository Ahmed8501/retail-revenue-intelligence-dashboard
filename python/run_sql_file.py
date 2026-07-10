import os
import sys
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Usage: python python/run_sql_file.py sql/file_name.sql")

    sql_file_path = os.path.join(BASE_DIR, sys.argv[1])

    if not os.path.exists(sql_file_path):
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql = file.read()

    conn = duckdb.connect(DB_PATH)
    conn.execute(sql)
    conn.close()

    print(f"Executed SQL file successfully: {sys.argv[1]}")


if __name__ == "__main__":
    main()