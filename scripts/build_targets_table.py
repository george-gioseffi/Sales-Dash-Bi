from __future__ import annotations

import numpy as np
import pandas as pd

from project_config import RAW_DIR, SEED, ensure_directories


def build_targets() -> pd.DataFrame:
    ensure_directories()
    rng = np.random.default_rng(SEED + 17)

    sales = pd.read_csv(RAW_DIR / "sales_transactions.csv", parse_dates=["Order Date"])
    sales["Target Month"] = sales["Order Date"].dt.to_period("M").dt.to_timestamp()

    monthly_actuals = (
        sales.groupby(["Target Month", "Region", "Sales Channel"], as_index=False)
        .agg({"Sales Amount": "sum"})
        .rename(
            columns={
                "Sales Amount": "ActualSalesAmount",
                "Sales Channel": "SalesChannel",
                "Target Month": "TargetMonth",
            }
        )
    )

    targets = monthly_actuals.copy()

    region_stretch = {
        "Southeast": 1.030,
        "South": 1.015,
        "Northeast": 0.995,
        "Midwest": 0.985,
        "North": 0.990,
    }
    channel_stretch = {
        "Online": 1.010,
        "Retail Stores": 0.998,
        "Distributors": 1.018,
        "Direct Sales": 1.022,
    }
    month_adjustment = {
        1: 1.005,
        2: 0.985,
        3: 0.995,
        4: 1.000,
        5: 1.005,
        6: 1.002,
        7: 0.995,
        8: 1.000,
        9: 1.008,
        10: 1.015,
        11: 1.020,
        12: 1.018,
    }

    target_values: list[float] = []
    for row in targets.itertuples(index=False):
        stretch_factor = (
            region_stretch[row.Region]
            * channel_stretch[row.SalesChannel]
            * month_adjustment[row.TargetMonth.month]
        )
        variance_noise = rng.normal(1.0, 0.030)
        target_values.append(round(float(row.ActualSalesAmount * stretch_factor * variance_noise), 2))

    targets["Sales Target"] = target_values
    targets = targets.rename(
        columns={"TargetMonth": "Target Month", "SalesChannel": "Sales Channel"}
    )
    targets = targets[["Target Month", "Region", "Sales Channel", "Sales Target"]]
    targets = targets.sort_values(["Target Month", "Region", "Sales Channel"]).reset_index(drop=True)
    targets.to_csv(RAW_DIR / "monthly_targets.csv", index=False)
    return targets


if __name__ == "__main__":
    targets_df = build_targets()
    print(f"Generated {len(targets_df):,} monthly target rows.")
