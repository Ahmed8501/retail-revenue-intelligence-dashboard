# Data Model

This project follows a simple BI pipeline that transforms raw CSV files into clean, dashboard-ready datasets.

## Pipeline Flow

Raw CSV files
→ DuckDB raw tables
→ Clean SQL tables
→ Fact and dimension tables
→ KPI views
→ Power BI dashboard
Raw Layer

The raw layer contains the original synthetic CSV files loaded into DuckDB without major transformations.

Raw tables:

raw_orders
raw_returns
raw_products
raw_stores
raw_customers
raw_marketing_spend
raw_targets
Clean Layer

The clean layer standardizes and prepares the raw data for analysis.

Cleaning steps include:

Removing duplicate order rows
Standardizing mixed date formats
Replacing missing customer IDs with GUEST
Cleaning inconsistent city formatting
Replacing missing product categories with Unknown
Casting numeric columns to proper data types
Flagging suspicious discount values

Clean tables:

clean_orders
clean_returns
clean_products
clean_stores
clean_customers
clean_marketing_spend
clean_targets
Analytics Layer

The analytics layer organizes the data into fact and dimension tables.

Dimension tables:

dim_product
dim_store
dim_customer

Fact tables:

fact_sales
fact_returns
fact_marketing
monthly_targets
KPI Views

The final KPI views are designed for Power BI dashboard consumption.

Views:

vw_executive_overview
vw_product_performance
vw_store_region_performance
vw_marketing_roi

Each view supports a specific dashboard page.
