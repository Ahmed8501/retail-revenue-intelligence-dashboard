import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DATA_DIR = os.path.join(BASE_DIR, "data", "output")

os.makedirs(OUTPUT_DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(OUTPUT_DATA_DIR, "retail_analytics.duckdb")


TABLES = {
    "raw_orders": "orders.csv",
    "raw_returns": "returns.csv",
    "raw_products": "products.csv",
    "raw_stores": "stores.csv",
    "raw_customers": "customers.csv",
    "raw_marketing_spend": "marketing_spend.csv",
    "raw_targets": "targets.csv",
}


def main() -> None:
    print("Loading raw CSV files into DuckDB...")

    conn = duckdb.connect(DB_PATH)

    for table_name, file_name in TABLES.items():
        file_path = os.path.join(RAW_DATA_DIR, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file: {file_path}")

        conn.execute(f"DROP TABLE IF EXISTS {table_name}")

        conn.execute(
            f"""
            CREATE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{file_path}', header = true);
            """
        )

        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Loaded {table_name}: {row_count:,} rows")

    conn.close()

    print(f"DuckDB database created at: {DB_PATH}")


if __name__ == "__main__":
    main()