import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")


TABLES = [
    "clean_orders",
    "clean_returns",
    "clean_products",
    "clean_stores",
    "clean_customers",
    "clean_marketing_spend",
    "clean_targets",
]


def main() -> None:
    print("Validating clean DuckDB tables...\n")

    conn = duckdb.connect(DB_PATH)

    for table_name in TABLES:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        column_count = len(conn.execute(f"DESCRIBE {table_name}").fetchall())

        print(f"{table_name}: {row_count:,} rows, {column_count} columns")

    print("\nClean orders date check:")
    print(
        conn.execute(
            """
            SELECT
                MIN(order_date) AS min_order_date,
                MAX(order_date) AS max_order_date,
                COUNT(*) AS total_rows
            FROM clean_orders;
            """
        ).fetchdf()
    )

    print("\nMissing customer handling:")
    print(
        conn.execute(
            """
            SELECT
                COUNT(*) AS guest_order_rows
            FROM clean_orders
            WHERE customer_id = 'GUEST';
            """
        ).fetchdf()
    )

    print("\nSuspicious discount rows:")
    print(
        conn.execute(
            """
            SELECT
                COUNT(*) AS suspicious_discount_rows
            FROM clean_orders
            WHERE is_suspicious_discount = TRUE;
            """
        ).fetchdf()
    )

    print("\nSample clean orders:")
    print(
        conn.execute(
            """
            SELECT *
            FROM clean_orders
            LIMIT 5;
            """
        ).fetchdf()
    )

    conn.close()


if __name__ == "__main__":
    main()