import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker()
random.seed(42)
np.random.seed(42)
Faker.seed(42)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DATA_DIR, exist_ok=True)


# -----------------------------
# Configuration
# -----------------------------

NUM_PRODUCTS = 180
NUM_STORES = 30
NUM_CUSTOMERS = 5000
NUM_ORDERS = 25000

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

REGIONS = ["North", "South", "East", "West", "Central"]

CITIES = [
    "Cairo",
    "Giza",
    "Alexandria",
    "Mansoura",
    "Tanta",
    "Zagazig",
    "Aswan",
    "Luxor",
    "Hurghada",
    "Port Said",
]

STORE_TYPES = ["Physical Store", "Outlet", "Online Fulfillment Center"]

SALES_CHANNELS = ["Physical Store", "Website", "Mobile App", "Marketplace"]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Wallet", "Bank Transfer"]

CUSTOMER_SEGMENTS = ["New Customer", "Returning Customer", "VIP", "Occasional Buyer"]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]

PRODUCT_CATEGORIES = {
    "Electronics": ["Accessories", "Audio", "Smart Devices", "Computers"],
    "Home & Kitchen": ["Appliances", "Cookware", "Storage", "Cleaning"],
    "Fashion": ["Men", "Women", "Shoes", "Accessories"],
    "Beauty": ["Skincare", "Fragrance", "Haircare", "Makeup"],
    "Sports": ["Fitness", "Outdoor", "Footwear", "Equipment"],
}

BRANDS = [
    "NovaTech",
    "UrbanLine",
    "HomePro",
    "FitZone",
    "StyleCraft",
    "BrightLife",
    "CoreMax",
    "PureGlow",
]

MARKETING_CHANNELS = ["Google Ads", "Meta Ads", "Email", "TikTok Ads", "Affiliate"]

RETURN_REASONS = [
    "Damaged item",
    "Wrong size",
    "Changed mind",
    "Late delivery",
    "Product not as described",
    "Defective product",
]


# -----------------------------
# Helper functions
# -----------------------------

def random_date(start_date: datetime, end_date: datetime) -> datetime:
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def maybe_messy_city(city: str) -> str:
    """
    Introduce realistic city formatting issues.
    """
    options = [
        city,
        city.lower(),
        city.upper(),
        f"{city} ",
        f" {city}",
    ]
    return random.choice(options) if random.random() < 0.12 else city


def maybe_messy_date(date_value: datetime) -> str:
    """
    Introduce inconsistent date formats.
    """
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
    ]
    return date_value.strftime(random.choice(formats))


def write_csv(df: pd.DataFrame, filename: str) -> None:
    path = os.path.join(RAW_DATA_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Created {path} with {len(df):,} rows")


# -----------------------------
# Generate products
# -----------------------------

def generate_products() -> pd.DataFrame:
    rows = []

    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        subcategory = random.choice(PRODUCT_CATEGORIES[category])
        brand = random.choice(BRANDS)

        cost_price = round(random.uniform(5, 250), 2)

        # Some products have missing categories to simulate incomplete master data
        final_category = category if random.random() > 0.04 else None

        rows.append(
            {
                "product_id": f"PROD-{i:04d}",
                "product_name": f"{brand} {subcategory} Item {i}",
                "category": final_category,
                "subcategory": subcategory,
                "brand": brand,
                "cost_price": cost_price,
            }
        )

    return pd.DataFrame(rows)


# -----------------------------
# Generate stores
# -----------------------------

def generate_stores() -> pd.DataFrame:
    rows = []

    for i in range(1, NUM_STORES + 1):
        city = random.choice(CITIES)

        rows.append(
            {
                "store_id": f"STORE-{i:03d}",
                "store_name": f"{city} Store {i}",
                "city": maybe_messy_city(city),
                "region": random.choice(REGIONS),
                "store_type": random.choice(STORE_TYPES),
            }
        )

    return pd.DataFrame(rows)


# -----------------------------
# Generate customers
# -----------------------------

def generate_customers() -> pd.DataFrame:
    rows = []

    for i in range(1, NUM_CUSTOMERS + 1):
        signup_date = random_date(datetime(2023, 1, 1), END_DATE)
        city = random.choice(CITIES)

        rows.append(
            {
                "customer_id": f"CUST-{i:05d}",
                "signup_date": maybe_messy_date(signup_date),
                "customer_segment": random.choice(CUSTOMER_SEGMENTS),
                "city": maybe_messy_city(city),
                "age_group": random.choice(AGE_GROUPS),
            }
        )

    return pd.DataFrame(rows)


# -----------------------------
# Generate orders
# -----------------------------

def generate_orders(products: pd.DataFrame, stores: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    rows = []

    product_ids = products["product_id"].tolist()
    store_ids = stores["store_id"].tolist()
    customer_ids = customers["customer_id"].tolist()

    product_cost_map = products.set_index("product_id")["cost_price"].to_dict()

    for i in range(1, NUM_ORDERS + 1):
        product_id = random.choice(product_ids)
        cost_price = product_cost_map[product_id]

        # Selling price is based on cost plus markup
        unit_price = round(cost_price * random.uniform(1.25, 2.8), 2)

        quantity = random.choices(
            population=[1, 2, 3, 4, 5],
            weights=[55, 25, 12, 5, 3],
            k=1,
        )[0]

        gross_sales = unit_price * quantity

        # Most orders have no/small discount, but some have bigger promotions
        discount_rate = random.choices(
            population=[0, 0.05, 0.10, 0.15, 0.25, 0.40],
            weights=[45, 20, 15, 10, 7, 3],
            k=1,
        )[0]

        discount_amount = round(gross_sales * discount_rate, 2)

        # Introduce a few suspicious discounts
        if random.random() < 0.003:
            discount_amount = round(gross_sales * random.uniform(0.70, 1.20), 2)

        order_date = random_date(START_DATE, END_DATE)

        customer_id = random.choice(customer_ids)

        # Some guest checkout / missing customer IDs
        if random.random() < 0.025:
            customer_id = None

        rows.append(
            {
                "order_id": f"ORD-{i:06d}",
                "order_date": maybe_messy_date(order_date),
                "customer_id": customer_id,
                "store_id": random.choice(store_ids),
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_amount": discount_amount,
                "payment_method": random.choice(PAYMENT_METHODS),
                "sales_channel": random.choice(SALES_CHANNELS),
            }
        )

    orders = pd.DataFrame(rows)

    # Add duplicate order rows to simulate export duplication
    duplicate_sample = orders.sample(frac=0.01, random_state=42)
    orders = pd.concat([orders, duplicate_sample], ignore_index=True)

    # Shuffle rows
    orders = orders.sample(frac=1, random_state=42).reset_index(drop=True)

    return orders


# -----------------------------
# Generate returns
# -----------------------------

def generate_returns(orders: pd.DataFrame) -> pd.DataFrame:
    rows = []

    # Around 7% of order lines are returned
    return_candidates = orders.drop_duplicates(subset=["order_id", "product_id"]).sample(
        frac=0.07,
        random_state=42,
    )

    for i, (_, order) in enumerate(return_candidates.iterrows(), start=1):
        try:
            parsed_order_date = pd.to_datetime(order["order_date"], dayfirst=False, errors="coerce")

            if pd.isna(parsed_order_date):
                parsed_order_date = pd.to_datetime(order["order_date"], dayfirst=True, errors="coerce")

            if pd.isna(parsed_order_date):
                parsed_order_date = START_DATE

            return_date = parsed_order_date.to_pydatetime() + timedelta(days=random.randint(1, 45))

        except Exception:
            return_date = random_date(START_DATE, END_DATE)

        refunded_amount = max(
            0,
            round((order["quantity"] * order["unit_price"]) - order["discount_amount"], 2),
        )

        rows.append(
            {
                "return_id": f"RET-{i:06d}",
                "order_id": order["order_id"],
                "product_id": order["product_id"],
                "return_date": maybe_messy_date(return_date),
                "return_reason": random.choice(RETURN_REASONS),
                "refunded_amount": refunded_amount,
            }
        )

    return pd.DataFrame(rows)


# -----------------------------
# Generate marketing spend
# -----------------------------

def generate_marketing_spend() -> pd.DataFrame:
    rows = []

    campaign_templates = [
        "Winter Sale",
        "Summer Deals",
        "Back to School",
        "Flash Promo",
        "VIP Retargeting",
        "New Customer Acquisition",
        "Holiday Campaign",
    ]

    current_date = START_DATE

    while current_date <= END_DATE:
        for channel in MARKETING_CHANNELS:
            # Not every channel runs every day
            if random.random() < 0.72:
                spend = round(random.uniform(100, 2500), 2)
                impressions = random.randint(3000, 90000)
                clicks = random.randint(100, min(impressions, 6000))

                conversions = random.randint(0, max(1, int(clicks * 0.12)))

                # Some campaigns spend money but generate no conversions
                if random.random() < 0.08:
                    conversions = 0

                avg_order_value = random.uniform(40, 180)
                attributed_revenue = round(conversions * avg_order_value, 2)

                rows.append(
                    {
                        "date": maybe_messy_date(current_date),
                        "channel": channel,
                        "campaign_name": f"{random.choice(campaign_templates)} - {channel}",
                        "spend": spend,
                        "clicks": clicks,
                        "impressions": impressions,
                        "conversions": conversions,
                        "attributed_revenue": attributed_revenue,
                    }
                )

        current_date += timedelta(days=1)

    return pd.DataFrame(rows)


# -----------------------------
# Generate targets
# -----------------------------

def generate_targets() -> pd.DataFrame:
    rows = []

    months = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")

    for month in months:
        for region in REGIONS:
            # A few missing targets to simulate incomplete planning data
            if random.random() < 0.04:
                continue

            revenue_target = round(random.uniform(220000, 520000), 2)
            profit_target = round(revenue_target * random.uniform(0.22, 0.36), 2)

            rows.append(
                {
                    "month": month.strftime("%Y-%m"),
                    "region": region,
                    "revenue_target": revenue_target,
                    "profit_target": profit_target,
                }
            )

    return pd.DataFrame(rows)


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    print("Generating synthetic retail dataset...")

    products = generate_products()
    stores = generate_stores()
    customers = generate_customers()
    orders = generate_orders(products, stores, customers)
    returns = generate_returns(orders)
    marketing_spend = generate_marketing_spend()
    targets = generate_targets()

    write_csv(products, "products.csv")
    write_csv(stores, "stores.csv")
    write_csv(customers, "customers.csv")
    write_csv(orders, "orders.csv")
    write_csv(returns, "returns.csv")
    write_csv(marketing_spend, "marketing_spend.csv")
    write_csv(targets, "targets.csv")

    print("Dataset generation completed successfully.")


if __name__ == "__main__":
    main()
