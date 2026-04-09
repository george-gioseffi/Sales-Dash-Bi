# Final Dashboard Handoff

## Audit Summary

### Already Ready

- Reproducible sales and target datasets
- Processed star-schema CSVs in `data/processed/`
- DAX library in `docs/dax-measures.md`
- Model documentation in `docs/data-model.md`
- Visual direction in `docs/dashboard-blueprint.md`
- Theme file in `assets/theme/sales-performance-theme.json`

### Final Gap Closed In This Handoff

- Portfolio-ready dashboard page previews generated from the real dataset
- Exact page build guidance for Power BI Desktop
- Final screenshot naming aligned with the README

## Source-Of-Truth Files

- `README.md`
- `docs/data-model.md`
- `docs/dax-measures.md`
- `docs/dashboard-blueprint.md`
- `docs/design-decisions.md`
- `docs/page-by-page-kpi-map.md`
- `assets/theme/sales-performance-theme.json`
- `screenshots/README.md`

## Datasets To Load

Use the processed tables from `data/processed/`:

- `dim_date.csv`
- `dim_product.csv`
- `dim_customer.csv`
- `dim_geography.csv`
- `dim_region.csv`
- `dim_channel.csv`
- `dim_sales_rep.csv`
- `fact_sales.csv`
- `fact_targets.csv`

## Model Setup

### Table Names

Rename imported Power BI tables exactly as follows:

- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_geography`
- `dim_region`
- `dim_channel`
- `dim_sales_rep`
- `fact_sales`
- `fact_targets`

### Required Relationships

Follow `docs/data-model.md` exactly. The most important points:

- `dim_date[DateKey]` to `fact_sales[OrderDateKey]` as active
- `dim_date[DateKey]` to `fact_sales[ShipDateKey]` as inactive
- `dim_date[DateKey]` to `fact_targets[DateKey]` as active
- `dim_region[RegionKey]` to both `fact_sales[RegionKey]` and `fact_targets[RegionKey]`
- `dim_channel[ChannelKey]` to both `fact_sales[ChannelKey]` and `fact_targets[ChannelKey]`

### Required Date Configuration

- Mark `dim_date[Date]` as the date table
- Sort `dim_date[Month Name]` by `dim_date[Month Number]`

## Visual Build Defaults

- Canvas: `16:9`
- Background: `#F7F6F3`
- Primary color: `#123B5D`
- Positive color: `#2C6E49`
- Negative color: `#D1495B`
- Neutral support: `#7C8EA3`
- Card background: white or theme-driven neutral
- Use one top KPI strip per page
- Keep slicers horizontal where possible

## Page Build Specification

## 1. Executive Overview

### KPI Cards

- Total Sales
- Total Profit
- Profit Margin %
- Total Orders
- Average Order Value
- Return Rate %
- Target Attainment %

### Visuals

- Line chart: `dim_date[Date]` on axis, `Total Sales` and `Total Profit`
- Line chart: `dim_date[Date]` on axis, `Total Sales` and `Sales Target`
- Bar chart: `dim_region[Region]` by `Total Sales`
- Bar chart: `dim_product[Category]` by `Total Sales`

### Slicers

- Date
- Region
- Sales Channel
- Category

## 2. Sales Analysis

### KPI Cards

- Total Sales
- Total Orders
- Average Order Value
- Total Quantity

### Visuals

- Line or area chart: monthly `Total Sales`
- Stacked column or area chart: monthly `Total Sales` by `dim_channel[SalesChannel]`
- Horizontal bar: `dim_product[Category]` by `Total Sales`
- Horizontal bar: `dim_product[SubCategory]` by `Total Sales`
- Horizontal bar: `dim_region[Region]` by `Total Sales`
- Matrix or heatmap: `dim_region[Region]` x `dim_channel[SalesChannel]` with `Total Sales`

### Slicers

- Date
- Region
- Sales Channel
- Segment

## 3. Profitability Analysis

### KPI Cards

- Total Profit
- Profit Margin %
- Discount %
- Profit per Order

### Visuals

- Horizontal bar: `dim_product[Category]` by `Profit Margin %`
- Scatter: `Total Sales` on X, `Total Profit` on Y, grouped by `dim_product[SubCategory]`
- Scatter: `Discount %` on X, `Profit Margin %` on Y, grouped by `dim_product[SubCategory]`
- Horizontal bar: low-margin products by `Profit Margin %`
- Horizontal bar: `dim_channel[SalesChannel]` by `Total Profit`
- Horizontal bar: `dim_region[Region]` by `Profit Margin %`

### Slicers

- Date
- Region
- Category
- Sales Channel

## 4. Customer & Product Insights

### KPI Cards

- Total Customers
- Sales per Customer
- Top 10 Product Share %
- Enterprise Sales YoY %

### Visuals

- Clustered bar: `dim_customer[Segment]` by `Total Sales` and `Total Profit`
- Horizontal bar: segment `Sales YoY %`
- Horizontal bar: top products by `Total Sales`
- Horizontal bar: top products by `Total Profit`
- Line chart: ranked products by cumulative `% of Total Sales`

### Slicers

- Date
- Segment
- Category
- Region

## 5. Geography & Channel Performance

### KPI Cards

- Total Sales
- Total Profit
- Profit Margin %
- Profit per Order

### Visuals

- Horizontal bar: `dim_region[Region]` by `Total Sales`
- Horizontal bar: `dim_region[Region]` by `Profit Margin %`
- Horizontal bar: `dim_channel[SalesChannel]` by `% of Total Sales`
- Matrix or heatmap: region x channel with `Total Sales`
- Matrix or heatmap: region x channel with `Profit Margin %`
- Horizontal bar: `dim_channel[SalesChannel]` by `Profit per Order`

### Slicers

- Date
- Region
- Sales Channel
- Segment

## 6. Targets & Trends

### KPI Cards

- Sales Target
- Target Attainment %
- Sales vs Target Variance
- Sales YoY %
- Profit YoY %

### Visuals

- Line chart: monthly `Total Sales` vs `Sales Target`
- Variance column chart: monthly `Sales vs Target Variance`
- Horizontal bar: `dim_region[Region]` by `Target Attainment %`
- Horizontal bar: `dim_channel[SalesChannel]` by `Target Attainment %`
- Line chart: monthly `Sales YoY %` and `Profit YoY %`
- Matrix or heatmap: 2025 monthly `Total Sales` by region

### Slicers

- Date
- Region
- Sales Channel

## Interaction Rules

- Keep slicers synced only when they help comparisons, especially Date and Region
- Disable cross-highlighting where it creates visual noise
- Leave the most detailed visuals on the bottom half of each page
- Use `dim_region` instead of `dim_geography` on target-sensitive pages

## Screenshot Workflow

Native Power BI exports should use these filenames:

1. `screenshots/01-executive-overview.png`
2. `screenshots/02-sales-analysis.png`
3. `screenshots/03-profitability-analysis.png`
4. `screenshots/04-customer-product-insights.png`
5. `screenshots/05-geography-channel-performance.png`
6. `screenshots/06-targets-trends.png`

## Practical Limitation

Power BI Desktop is installed on this machine, but the report canvas could not be assembled programmatically from the terminal. Because of that, this repository now includes:

- exact build guidance for the Power BI file
- six static dashboard preview renders generated from the real project data

These previews can be replaced one-for-one with native Power BI screenshot exports after the final Desktop assembly.

