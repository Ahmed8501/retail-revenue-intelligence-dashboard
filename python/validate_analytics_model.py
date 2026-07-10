import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")


TABLES = [
    "dim_product",
    "dim_store",
    "dim_customer",
    "fact_sales",
    "fact_returns",
    "fact_marketing",
    "monthly_targets",
]


def main() -> None:
    print("Validating analytics model...\n")

    conn = duckdb.connect(DB_PATH)

    for table_name in TABLES:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        column_count = len(conn.execute(f"DESCRIBE {table_name}").fetchall())
        print(f"{table_name}: {row_count:,} rows, {column_count} columns")

    print("\nSales KPI sample:")
    print(
        conn.execute(
            """
            SELECT
                ROUND(SUM(revenue), 2) AS total_revenue,
                ROUND(SUM(gross_profit), 2) AS total_gross_profit,
                ROUND(SUM(gross_profit) / NULLIF(SUM(revenue), 0), 4) AS gross_margin_pct,
                COUNT(DISTINCT order_id) AS total_orders,
                SUM(quantity) AS units_sold
            FROM fact_sales;
            """
        ).fetchdf()
    )

    print("\nRevenue by region:")
    print(
        conn.execute(
            """
            SELECT
                ds.region,
                ROUND(SUM(fs.revenue), 2) AS revenue,
                ROUND(SUM(fs.gross_profit), 2) AS gross_profit
            FROM fact_sales fs
            LEFT JOIN dim_store ds
                ON fs.store_id = ds.store_id
            GROUP BY ds.region
            ORDER BY revenue DESC;
            """
        ).fetchdf()
    )

    print("\nMarketing KPI sample:")
    print(
        conn.execute(
            """
            SELECT
                channel,
                ROUND(SUM(spend), 2) AS spend,
                ROUND(SUM(attributed_revenue), 2) AS attributed_revenue,
                ROUND(SUM(attributed_revenue) / NULLIF(SUM(spend), 0), 2) AS roas,
                SUM(conversions) AS conversions
            FROM fact_marketing
            GROUP BY channel
            ORDER BY roas DESC;
            """
        ).fetchdf()
    )

    conn.close()


if __name__ == "__main__":
    main()