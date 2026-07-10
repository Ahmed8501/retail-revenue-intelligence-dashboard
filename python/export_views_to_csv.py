import os
import duckdb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "output", "retail_analytics.duckdb")
EXPORT_DIR = os.path.join(BASE_DIR, "data", "output", "powerbi_exports")

os.makedirs(EXPORT_DIR, exist_ok=True)


VIEWS = [
    "vw_executive_overview",
    "vw_product_performance",
    "vw_store_region_performance",
    "vw_marketing_roi",
]


def main() -> None:
    print("Exporting KPI views to CSV files...")

    conn = duckdb.connect(DB_PATH)

    for view_name in VIEWS:
        export_path = os.path.join(EXPORT_DIR, f"{view_name}.csv")

        conn.execute(
            f"""
            COPY (
                SELECT *
                FROM {view_name}
            )
            TO '{export_path}'
            (HEADER, DELIMITER ',');
            """
        )

        row_count = conn.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
        print(f"Exported {view_name}: {row_count:,} rows")

    conn.close()

    print(f"CSV exports created in: {EXPORT_DIR}")


if __name__ == "__main__":
    main()