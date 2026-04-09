from __future__ import annotations

import pandas as pd

from project_config import DATE_END, DATE_START, PROCESSED_DIR, RAW_DIR, ensure_directories


def build_dim_date() -> pd.DataFrame:
    dates = pd.date_range(DATE_START, DATE_END, freq="D")
    max_year = pd.Timestamp(DATE_END).year
    dim_date = pd.DataFrame({"Date": dates})
    dim_date["DateKey"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["Year"] = dim_date["Date"].dt.year
    dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
    dim_date["Month Number"] = dim_date["Date"].dt.month
    dim_date["Month Name"] = dim_date["Date"].dt.strftime("%B")
    dim_date["Year-Month"] = dim_date["Date"].dt.strftime("%Y-%m")
    dim_date["Week Number"] = dim_date["Date"].dt.isocalendar().week.astype(int)
    dim_date["Is Current Year"] = (dim_date["Year"] == max_year).astype(int)
    return dim_date[
        [
            "DateKey",
            "Date",
            "Year",
            "Quarter",
            "Month Number",
            "Month Name",
            "Year-Month",
            "Week Number",
            "Is Current Year",
        ]
    ]


def build_star_schema() -> None:
    ensure_directories()

    sales = pd.read_csv(
        RAW_DIR / "sales_transactions.csv",
        parse_dates=["Order Date", "Ship Date"],
    )
    targets = pd.read_csv(
        RAW_DIR / "monthly_targets.csv",
        parse_dates=["Target Month"],
    )

    region = (
        sales[["Country", "Region"]]
        .drop_duplicates()
        .sort_values(["Region"])
        .reset_index(drop=True)
    )
    region["RegionKey"] = region.index + 1

    geography = (
        sales[["Country", "Region", "State", "City"]]
        .drop_duplicates()
        .sort_values(["Region", "State", "City"])
        .reset_index(drop=True)
    )
    geography = geography.merge(region, on=["Country", "Region"], how="left")
    geography["GeographyKey"] = geography.index + 1

    customer = (
        sales[
            ["Customer ID", "Customer Name", "Segment", "Country", "Region", "State", "City"]
        ]
        .drop_duplicates()
        .merge(geography, on=["Country", "Region", "State", "City"], how="left")
        .sort_values(["Customer ID"])
        .reset_index(drop=True)
    )
    customer["CustomerKey"] = customer.index + 1

    product = (
        sales[["Product ID", "Product Name", "Category", "Sub-Category"]]
        .drop_duplicates()
        .sort_values(["Category", "Sub-Category", "Product ID"])
        .reset_index(drop=True)
    )
    product["ProductKey"] = product.index + 1

    channel = (
        sales[["Sales Channel"]]
        .drop_duplicates()
        .sort_values(["Sales Channel"])
        .reset_index(drop=True)
    )
    channel["ChannelKey"] = channel.index + 1

    sales_rep = (
        sales[["Sales Rep", "Region"]]
        .drop_duplicates()
        .sort_values(["Sales Rep"])
        .reset_index(drop=True)
    )
    sales_rep["SalesRepKey"] = sales_rep.index + 1

    fact_sales = sales.merge(product, on=["Product ID", "Product Name", "Category", "Sub-Category"], how="left")
    fact_sales = fact_sales.merge(customer, on=["Customer ID", "Customer Name", "Segment", "Country", "Region", "State", "City"], how="left")
    fact_sales = fact_sales.merge(channel, on=["Sales Channel"], how="left")
    fact_sales = fact_sales.merge(sales_rep, on=["Sales Rep", "Region"], how="left")
    fact_sales["OrderDateKey"] = fact_sales["Order Date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales["ShipDateKey"] = fact_sales["Ship Date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales["SalesKey"] = range(1, len(fact_sales) + 1)

    fact_sales = fact_sales[
        [
            "SalesKey",
            "Order ID",
            "Order Line Number",
            "OrderDateKey",
            "ShipDateKey",
            "CustomerKey",
            "GeographyKey",
            "RegionKey",
            "ProductKey",
            "ChannelKey",
            "SalesRepKey",
            "Sales Amount",
            "Gross Sales Amount",
            "Discount Amount",
            "Discount",
            "Quantity",
            "Unit Price",
            "Cost",
            "Profit",
            "Returned Flag",
        ]
    ].rename(
        columns={
            "Order ID": "OrderID",
            "Order Line Number": "OrderLineNumber",
            "Sales Amount": "SalesAmount",
            "Gross Sales Amount": "GrossSalesAmount",
            "Discount Amount": "DiscountAmount",
            "Discount": "DiscountPct",
            "Unit Price": "UnitPrice",
            "Cost": "CostAmount",
            "Profit": "ProfitAmount",
            "Returned Flag": "ReturnedFlag",
        }
    )

    fact_targets = targets.merge(region[["RegionKey", "Region"]], on="Region", how="left")
    fact_targets = fact_targets.merge(channel, on="Sales Channel", how="left")
    fact_targets["DateKey"] = fact_targets["Target Month"].dt.strftime("%Y%m%d").astype(int)
    fact_targets["TargetKey"] = range(1, len(fact_targets) + 1)
    fact_targets = fact_targets[
        ["TargetKey", "DateKey", "RegionKey", "ChannelKey", "Sales Target"]
    ].rename(columns={"Sales Target": "SalesTargetAmount"})

    dim_date = build_dim_date()

    dim_date.to_csv(PROCESSED_DIR / "dim_date.csv", index=False)
    region[["RegionKey", "Country", "Region"]].to_csv(
        PROCESSED_DIR / "dim_region.csv", index=False
    )
    geography[["GeographyKey", "Country", "Region", "State", "City"]].to_csv(
        PROCESSED_DIR / "dim_geography.csv", index=False
    )
    customer[
        [
            "CustomerKey",
            "Customer ID",
            "Customer Name",
            "Segment",
            "GeographyKey",
        ]
    ].rename(
        columns={
            "Customer ID": "CustomerID",
            "Customer Name": "CustomerName",
        }
    ).to_csv(PROCESSED_DIR / "dim_customer.csv", index=False)
    product[
        ["ProductKey", "Product ID", "Product Name", "Category", "Sub-Category"]
    ].rename(
        columns={
            "Product ID": "ProductID",
            "Product Name": "ProductName",
            "Sub-Category": "SubCategory",
        }
    ).to_csv(PROCESSED_DIR / "dim_product.csv", index=False)
    channel.rename(columns={"Sales Channel": "SalesChannel"}).to_csv(
        PROCESSED_DIR / "dim_channel.csv", index=False
    )
    sales_rep.rename(columns={"Sales Rep": "SalesRep", "Region": "HomeRegion"}).to_csv(
        PROCESSED_DIR / "dim_sales_rep.csv", index=False
    )
    fact_sales.to_csv(PROCESSED_DIR / "fact_sales.csv", index=False)
    fact_targets.to_csv(PROCESSED_DIR / "fact_targets.csv", index=False)

    print(
        "Built star schema with "
        f"{len(fact_sales):,} fact rows, {len(fact_targets):,} target rows and "
        f"{len(dim_date):,} dates."
    )


if __name__ == "__main__":
    build_star_schema()
