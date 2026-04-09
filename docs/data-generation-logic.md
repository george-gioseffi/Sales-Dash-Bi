# Data Generation Logic

## Overview

The dataset is synthetic but intentionally business-realistic. It was generated with fixed seeds to make the project reproducible while preserving consistent commercial behavior across time, geography, channels, and product mix.

Core generation scripts:

- `scripts/generate_sales_dataset.py`
- `scripts/build_targets_table.py`
- `scripts/build_star_schema.py`
- `scripts/run_full_build.py`

## Time Range

- Coverage: January 1, 2024 to December 31, 2025
- Granularity: transactional sales line items
- Calendar horizon: 24 full months to support YoY and MoM analysis

## Commercial Logic Embedded In The Data

### Seasonality

- November and December were intentionally modeled as stronger revenue months.
- February and mid-year periods are slightly softer.
- A moderate 2025 growth factor was applied to simulate year-over-year expansion.

### Regional Contrast

- `Southeast` carries the highest sales weight and the most aggressive pricing pressure.
- `South` performs as a strong secondary market with healthy revenue and stable margin.
- `Northeast`, `Midwest`, and `North` contribute lower volume with differentiated margin and target profiles.

### Channel Behavior

- `Online` drives the highest order volume and the highest return rate.
- `Retail Stores` balance volume and margin with more moderate discounting.
- `Distributors` move larger quantities but absorb heavier discount pressure.
- `Direct Sales` contributes less total volume than Online, but delivers stronger margin and profit per order.

### Product Economics

- Technology products carry the largest revenue contribution, especially laptops and monitors.
- Printers and tables were intentionally modeled with thinner economics and higher discount sensitivity.
- Office supply sub-categories were modeled as lower-ticket but structurally healthier on margin.

### Discount And Margin Interaction

- Discounts are not random. They vary by region, channel, segment, season, and product sensitivity.
- Higher-discount lines preserve the original cost basis, which naturally compresses profit margin.
- This makes it possible to analyze whether top-line sales are being bought at the expense of profitability.

### Targets

- Targets are stored separately at the `month x region x sales channel` grain.
- They are calibrated against actual run-rate with stretch factors by region, channel, and seasonality.
- Result: target attainment averages close to plan level, with both overperformance and underperformance across combinations instead of artificially perfect results.

## Reproducibility

- Random seed: `42`
- Rebuild command:

```bash
python scripts/run_full_build.py
```

