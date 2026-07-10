import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")


TABLES = [
    "raw_orders",
    "raw_returns",
    "raw_products",
    "raw_stores",
    "raw_customers",
    "raw_marketing_spend",
    "raw_targets",
]


def main() -> None:
    print("Validating raw DuckDB tables...\n")

    conn = duckdb.connect(DB_PATH)

    for table_name in TABLES:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        column_count = len(conn.execute(f"DESCRIBE {table_name}").fetchall())

        print(f"{table_name}: {row_count:,} rows, {column_count} columns")

    print("\nSample raw orders:")
    sample_orders = conn.execute(
        """
        SELECT *
        FROM raw_orders
        LIMIT 5;
        """
    ).fetchdf()

    print(sample_orders)

    print("\nDuplicate order_id check:")
    duplicate_orders = conn.execute(
        """
        SELECT 
            order_id,
            COUNT(*) AS duplicate_count
        FROM raw_orders
        GROUP BY order_id
        HAVING COUNT(*) > 1
        ORDER BY duplicate_count DESC
        LIMIT 10;
        """
    ).fetchdf()

    print(duplicate_orders)

    print("\nMissing customer_id count:")
    missing_customers = conn.execute(
        """
        SELECT COUNT(*) AS missing_customer_id_count
        FROM raw_orders
        WHERE customer_id IS NULL;
        """
    ).fetchdf()

    print(missing_customers)

    conn.close()


if __name__ == "__main__":
    main()