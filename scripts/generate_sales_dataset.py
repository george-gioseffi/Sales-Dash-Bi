from __future__ import annotations

from datetime import timedelta

import numpy as np
import pandas as pd

from project_config import (
    CHANNEL_SEGMENT_COMPATIBILITY,
    CHANNELS,
    COMPANY_NOUNS,
    COMPANY_PREFIXES,
    FIRST_NAMES,
    GEOGRAPHY,
    LAST_NAMES,
    MONTH_SEASONALITY,
    PRODUCTS,
    RAW_DIR,
    REGION_COST_ADJ,
    REGION_CUSTOMER_WEIGHTS,
    REGION_DISCOUNT_ADJ,
    REGION_FACTORS,
    REGION_PRICE_ADJ,
    SALES_REPS,
    SEED,
    SEGMENTS,
    YEAR_GROWTH,
    ensure_directories,
)


def build_product_catalog() -> pd.DataFrame:
    return pd.DataFrame(PRODUCTS)


def build_channel_catalog() -> pd.DataFrame:
    return pd.DataFrame(CHANNELS)


def generate_customers(rng: np.random.Generator, customer_count: int = 260) -> pd.DataFrame:
    segment_names = [item["Segment"] for item in SEGMENTS]
    segment_weights = [item["Weight"] for item in SEGMENTS]
    region_names = list(REGION_CUSTOMER_WEIGHTS)
    region_weights = [REGION_CUSTOMER_WEIGHTS[region] for region in region_names]

    rows: list[dict[str, object]] = []
    for index in range(1, customer_count + 1):
        segment = rng.choice(segment_names, p=segment_weights)
        region = rng.choice(region_names, p=region_weights)
        location = rng.choice(GEOGRAPHY[region])
        customer_id = f"C{index:04d}"

        if segment == "Consumer":
            first_name = rng.choice(FIRST_NAMES)
            last_name = rng.choice(LAST_NAMES)
            customer_name = f"{first_name} {last_name}"
        else:
            prefix = rng.choice(COMPANY_PREFIXES)
            noun = rng.choice(COMPANY_NOUNS)
            suffix = "Ltd." if segment == "Small Business" else "S.A."
            customer_name = f"{prefix} {noun} {suffix}"

        rows.append(
            {
                "Customer ID": customer_id,
                "Customer Name": customer_name,
                "Segment": segment,
                "Country": "Brazil",
                "Region": region,
                "State": location["State"],
                "City": location["City"],
            }
        )

    customers = pd.DataFrame(rows).drop_duplicates(subset=["Customer Name", "City"], keep="first")
    customers = customers.reset_index(drop=True)
    customers["Customer ID"] = [f"C{i:04d}" for i in range(1, len(customers) + 1)]
    return customers


def build_sales_rep_lookup() -> pd.DataFrame:
    return pd.DataFrame(SALES_REPS)


def month_order_target(month_start: pd.Timestamp) -> int:
    base = 170
    seasonal_factor = MONTH_SEASONALITY[month_start.month]
    growth_factor = YEAR_GROWTH[month_start.year]
    return int(round(base * seasonal_factor * growth_factor))


def choose_customer_for_channel(
    customers_by_region: dict[str, pd.DataFrame],
    channel_name: str,
    region: str,
    rng: np.random.Generator,
) -> pd.Series:
    region_customers = customers_by_region[region]
    compatibility = CHANNEL_SEGMENT_COMPATIBILITY[channel_name]
    weights = region_customers["Segment"].map(compatibility).astype(float).to_numpy()
    weights = weights / weights.sum()
    customer_idx = rng.choice(region_customers.index.to_numpy(), p=weights)
    return region_customers.loc[customer_idx]


def choose_sales_rep_for_region(region: str, rng: np.random.Generator, sales_reps: pd.DataFrame) -> str:
    region_reps = sales_reps[sales_reps["Home Region"] == region]
    if region_reps.empty:
        region_reps = sales_reps
    return rng.choice(region_reps["Sales Rep"].to_numpy())


def generate_sales_transactions() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    ensure_directories()

    customers = generate_customers(rng=rng)
    products = build_product_catalog()
    channels = build_channel_catalog()
    sales_reps = build_sales_rep_lookup()

    customers_by_region = {
        region: frame.reset_index(drop=True)
        for region, frame in customers.groupby("Region", sort=False)
    }

    month_starts = pd.date_range("2024-01-01", "2025-12-31", freq="MS")

    region_names = list(REGION_FACTORS)
    region_weights = np.array([REGION_FACTORS[region] for region in region_names], dtype=float)
    region_weights = region_weights / region_weights.sum()

    channel_names = channels["Sales Channel"].tolist()
    channel_weights = channels["Volume Weight"].to_numpy(dtype=float)
    channel_weights = channel_weights / channel_weights.sum()

    product_weights = products["Demand Weight"].to_numpy(dtype=float)
    product_weights = product_weights / product_weights.sum()

    segment_discount_lookup = {
        item["Segment"]: item["Discount Bias"]
        for item in SEGMENTS
    }
    channel_rows = channels.set_index("Sales Channel").to_dict(orient="index")
    product_rows = products.set_index("Product ID").to_dict(orient="index")

    records: list[dict[str, object]] = []
    order_sequence = 1

    for month_start in month_starts:
        orders_in_month = month_order_target(month_start)
        month_end = (month_start + pd.offsets.MonthEnd(0)).day
        promo_bias = 0.018 if month_start.month in (11, 12) else 0.0

        for _ in range(orders_in_month):
            order_id = f"ORD-{month_start.year}{month_start.month:02d}-{order_sequence:05d}"
            order_sequence += 1

            region = rng.choice(region_names, p=region_weights)
            channel_name = rng.choice(channel_names, p=channel_weights)
            customer = choose_customer_for_channel(
                customers_by_region=customers_by_region,
                channel_name=channel_name,
                region=region,
                rng=rng,
            )

            order_day = int(rng.integers(1, month_end + 1))
            order_date = pd.Timestamp(year=month_start.year, month=month_start.month, day=order_day)
            ship_days = max(1, int(round(rng.normal(channel_rows[channel_name]["Lead Days"], 1.1))))
            ship_date = order_date + timedelta(days=ship_days)
            sales_rep = choose_sales_rep_for_region(region=region, rng=rng, sales_reps=sales_reps)

            line_count = int(rng.choice([1, 2, 3, 4], p=[0.26, 0.41, 0.23, 0.10]))
            selected_products = rng.choice(
                products["Product ID"].to_numpy(),
                size=line_count,
                replace=False,
                p=product_weights,
            )

            for line_number, product_id in enumerate(selected_products, start=1):
                product = product_rows[product_id]
                quantity_multiplier = 1.0
                if customer["Segment"] == "Enterprise":
                    quantity_multiplier *= 1.45
                elif customer["Segment"] == "Small Business":
                    quantity_multiplier *= 1.18

                if channel_name == "Distributors":
                    quantity_multiplier *= 1.70
                elif channel_name == "Direct Sales":
                    quantity_multiplier *= 1.12

                quantity_base = product["Quantity Base"] * quantity_multiplier
                quantity = max(1, int(round(rng.poisson(quantity_base) + 1)))

                base_price = product["Base Price"]
                price_noise = rng.normal(1.0, 0.045)
                unit_price = base_price * REGION_PRICE_ADJ[region] * price_noise
                unit_price = round(max(unit_price, base_price * 0.82), 2)

                base_discount = (
                    channel_rows[channel_name]["Discount Bias"]
                    + REGION_DISCOUNT_ADJ[region]
                    + segment_discount_lookup[customer["Segment"]]
                    + promo_bias
                )
                discount_noise = rng.normal(0.0, 0.012)
                discount = base_discount + discount_noise
                discount *= product["Discount Sensitivity"]
                discount = float(np.clip(discount, 0.00, 0.22))

                gross_sales = unit_price * quantity
                sales_amount = gross_sales * (1 - discount)

                unit_cost = (
                    base_price
                    * product["Base Cost Ratio"]
                    * REGION_COST_ADJ[region]
                    * channel_rows[channel_name]["Cost Bias"]
                    * rng.normal(1.0, 0.025)
                )
                total_cost = unit_cost * quantity
                profit = sales_amount - total_cost

                return_probability = (
                    channel_rows[channel_name]["Return Bias"]
                    + product["Return Bias"]
                    + (0.004 if customer["Segment"] == "Consumer" else 0.0)
                )
                returned_flag = int(rng.random() < min(return_probability, 0.08))

                records.append(
                    {
                        "Order ID": order_id,
                        "Order Line Number": line_number,
                        "Order Date": order_date.normalize(),
                        "Ship Date": ship_date.normalize(),
                        "Customer ID": customer["Customer ID"],
                        "Customer Name": customer["Customer Name"],
                        "Segment": customer["Segment"],
                        "Country": customer["Country"],
                        "Region": region,
                        "State": customer["State"],
                        "City": customer["City"],
                        "Product ID": product_id,
                        "Product Name": product["Product Name"],
                        "Category": product["Category"],
                        "Sub-Category": product["Sub-Category"],
                        "Sales Amount": round(sales_amount, 2),
                        "Quantity": quantity,
                        "Unit Price": round(unit_price, 2),
                        "Gross Sales Amount": round(gross_sales, 2),
                        "Discount": round(discount, 4),
                        "Discount Amount": round(gross_sales - sales_amount, 2),
                        "Cost": round(total_cost, 2),
                        "Profit": round(profit, 2),
                        "Sales Channel": channel_name,
                        "Sales Rep": sales_rep,
                        "Returned Flag": returned_flag,
                    }
                )

    sales = pd.DataFrame(records)
    sales = sales.sort_values(["Order Date", "Order ID", "Order Line Number"]).reset_index(drop=True)

    customers.to_csv(RAW_DIR / "customers_master.csv", index=False)
    products.to_csv(RAW_DIR / "products_master.csv", index=False)
    build_channel_catalog().to_csv(RAW_DIR / "channels_master.csv", index=False)
    build_sales_rep_lookup().to_csv(RAW_DIR / "sales_reps_master.csv", index=False)
    sales.to_csv(RAW_DIR / "sales_transactions.csv", index=False)

    return sales


if __name__ == "__main__":
    sales_df = generate_sales_transactions()
    print(
        f"Generated {len(sales_df):,} sales rows across "
        f"{sales_df['Order ID'].nunique():,} orders."
    )
