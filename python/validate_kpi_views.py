import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")


VIEWS = [
    "vw_executive_overview",
    "vw_product_performance",
    "vw_store_region_performance",
    "vw_marketing_roi",
]


def main() -> None:
    print("Validating KPI views...\n")

    conn = duckdb.connect(DB_PATH)

    for view_name in VIEWS:
        row_count = conn.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
        column_count = len(conn.execute(f"DESCRIBE {view_name}").fetchall())
        print(f"{view_name}: {row_count:,} rows, {column_count} columns")

    print("\nExecutive overview totals:")
    print(
        conn.execute(
            """
            SELECT
                ROUND(SUM(revenue), 2) AS revenue,
                ROUND(SUM(gross_profit), 2) AS gross_profit,
                ROUND(SUM(gross_profit) / NULLIF(SUM(revenue), 0), 4) AS gross_margin_pct,
                SUM(total_orders) AS total_orders,
                SUM(units_sold) AS units_sold
            FROM vw_executive_overview;
            """
        ).fetchdf()
    )

    print("\nTop 10 products by revenue:")
    print(
        conn.execute(
            """
            SELECT
                product_name,
                category,
                ROUND(revenue, 2) AS revenue,
                ROUND(gross_profit, 2) AS gross_profit,
                ROUND(gross_margin_pct, 4) AS gross_margin_pct,
                ROUND(return_rate_pct, 4) AS return_rate_pct
            FROM vw_product_performance
            ORDER BY revenue DESC
            LIMIT 10;
            """
        ).fetchdf()
    )

    print("\nStore/region target achievement sample:")
    print(
        conn.execute(
            """
            SELECT
                region,
                order_month,
                ROUND(SUM(revenue), 2) AS revenue,
                ROUND(MAX(revenue_target), 2) AS revenue_target,
                ROUND(SUM(gross_profit), 2) AS gross_profit,
                ROUND(MAX(profit_target), 2) AS profit_target
            FROM vw_store_region_performance
            GROUP BY region, order_month
            ORDER BY order_month, region
            LIMIT 10;
            """
        ).fetchdf()
    )

    print("\nMarketing ROI by channel:")
    print(
        conn.execute(
            """
            SELECT
                channel,
                ROUND(SUM(spend), 2) AS spend,
                ROUND(SUM(attributed_revenue), 2) AS attributed_revenue,
                ROUND(SUM(attributed_revenue) / NULLIF(SUM(spend), 0), 2) AS roas,
                SUM(conversions) AS conversions
            FROM vw_marketing_roi
            GROUP BY channel
            ORDER BY roas DESC;
            """
        ).fetchdf()
    )

    conn.close()


if __name__ == "__main__":
    main()