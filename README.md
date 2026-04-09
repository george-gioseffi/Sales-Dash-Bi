# Sales Performance Analytics | Power BI + DAX + Power Query

An end-to-end Power BI portfolio project built as a realistic commercial analytics case. The project combines reproducible synthetic data generation, dimensional modeling, a structured DAX library, and a dashboard blueprint designed for executive decision-making.

## Overview

This case simulates a national company operating across Brazil in B2B and B2C channels. The business needs a reliable way to monitor revenue, profitability, discounts, targets, regional execution, and product mix without relying on fragmented spreadsheets.

The repository is designed to be strong even outside Power BI Desktop: the data pipeline is reproducible, the semantic model is documented, and the dashboard logic is fully specified for GitHub review.

## Business Problem

Leadership needs to answer questions such as:

- Which regions and channels are driving profitable growth?
- Are discounts accelerating healthy sales or eroding margin?
- Which products create revenue volume but destroy profitability?
- Are monthly targets being met consistently?
- Where should commercial teams focus to improve efficiency?

See the full question set in [docs/business-questions.md](docs/business-questions.md).

## Objectives

- Build a business-realistic sales analytics dataset with reproducible logic
- Model sales and targets in a clean star schema
- Create a DAX layer that supports executive and diagnostic analysis
- Define a professional multi-page dashboard blueprint
- Package the project for GitHub, interview discussion, and portfolio review

## Analytical Focus Areas

- Revenue performance
- Profitability and margin quality
- Discount pressure
- Target attainment
- Regional and channel performance
- Product and customer mix
- Monthly, MoM, and YoY trend analysis

## Dataset

The dataset is synthetic, but intentionally structured around realistic commercial behavior.

### Snapshot

| Metric | Value |
| --- | --- |
| Date range | 2024-01-01 to 2025-12-31 |
| Sales rows | 9,586 |
| Orders | 4,407 |
| Customers | 257 |
| Products | 28 |
| Regions | 5 |
| Channels | 4 |
| Monthly target rows | 480 |

### Business Scale Summary

| KPI | Value |
| --- | --- |
| Total Sales | 7.92M |
| Total Profit | 1.96M |
| Profit Margin % | 24.74% |
| Average Order Value | 1,796.12 |
| Average Discount % | 4.00% |
| Return Rate % | 1.74% |
| Average Target Attainment % | 98.18% |

Generation details are documented in [docs/data-generation-logic.md](docs/data-generation-logic.md).

## Data Model

The model uses two fact tables:

- `fact_sales` at the order-line grain
- `fact_targets` at the month x region x channel grain

Supported by these dimensions:

- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_geography`
- `dim_region`
- `dim_channel`
- `dim_sales_rep`

Why this structure:

- It keeps transactional and planning data separate
- It supports clean variance analysis
- It makes DAX easier to scale and explain

See [docs/data-model.md](docs/data-model.md) and [docs/modeling-rationale.md](docs/modeling-rationale.md).

## KPIs

The DAX layer covers core metrics, profitability, time intelligence, targets, and ranking.

Representative measures:

- Total Sales
- Total Profit
- Total Cost
- Average Order Value
- Profit Margin %
- Discount %
- Return Rate %
- Sales PY
- Sales YoY %
- Profit YoY %
- Running Sales
- Sales Target
- Target Attainment %
- Sales vs Target Variance
- Rank Region by Sales
- Rank Category by Profit

The full measure library is available in [docs/dax-measures.md](docs/dax-measures.md).

## Dashboard Pages

| Page | Purpose |
| --- | --- |
| Executive Overview | Executive snapshot of revenue, profit, margin, target status, and main growth drivers |
| Sales Analysis | Revenue trends, product drivers, and channel contribution |
| Profitability Analysis | Margin quality, discount impact, and weak economics by product mix |
| Customer & Product Insights | Segment growth, concentration, and top products |
| Geography & Channel Performance | Regional comparison and cross-channel efficiency |
| Targets & Trends | Actual vs target, variance, MoM, and YoY momentum |
| Methodology | Optional page for business context, model, and KPI definitions |

See [docs/dashboard-blueprint.md](docs/dashboard-blueprint.md), [docs/page-by-page-kpi-map.md](docs/page-by-page-kpi-map.md), and [docs/design-decisions.md](docs/design-decisions.md).

## Key Insights

- Sales grew 12.99% in 2025, but profit grew only 10.20%, softening margin from 25.07% to 24.45%.
- Southeast is the largest market by revenue, yet it underperforms other regions on target attainment and carries the highest average discount rate.
- Technology drives the business, but some high-volume products such as printers and tables show poor profit conversion.
- Direct Sales contributes less volume than Online, but delivers better margin and stronger profit per order.
- Enterprise is the fastest-growing segment, indicating upside in larger-value commercial accounts.
- The top 10 products represent 72.48% of total sales, creating clear concentration risk and opportunity.

Full takeaways live in [docs/final-insights.md](docs/final-insights.md).

## Recommendations

- Review discounting policy in printers, tables, and selected laptop lines
- Protect and scale the economics of Direct Sales
- Recalibrate commercial focus in Southeast to improve plan attainment
- Double down on Enterprise growth where order value and mix are healthier
- Monitor online returns during high-promotion periods

## Project Structure

```text
powerbi-sales-performance-analytics/
|- assets/
|  |- theme/
|- data/
|  |- raw/
|  |- processed/
|- docs/
|- powerbi/
|- screenshots/
|- scripts/
|- .gitignore
|- LICENSE
|- README.md
|- requirements.txt
```

## How To Open / Reproduce

### Rebuild The Data

```bash
pip install -r requirements.txt
python scripts/run_full_build.py
```

### Build The Report

1. Import the CSV files from `data/processed/` into Power BI Desktop.
2. Create relationships from [docs/data-model.md](docs/data-model.md).
3. Mark `dim_date[Date]` as the official date table.
4. Create the DAX measures from [docs/dax-measures.md](docs/dax-measures.md).
5. Import the theme from `assets/theme/sales-performance-theme.json`.
6. Build report pages from [docs/dashboard-blueprint.md](docs/dashboard-blueprint.md).

The full step-by-step guide is in [docs/reproduction-guide.md](docs/reproduction-guide.md).

### Generate Portfolio Preview Images

```bash
python scripts/generate_dashboard_previews.py
```

For the final Power BI Desktop handoff, use [powerbi/final-dashboard-handoff.md](powerbi/final-dashboard-handoff.md).

## Dashboard Preview

The repository now includes six portfolio-ready preview renders generated from the actual dataset and aligned to the final page blueprint. These can be replaced one-for-one with native Power BI Desktop exports later.

| Executive Overview | Sales Analysis |
| --- | --- |
| ![Executive Overview](screenshots/01-executive-overview.png) | ![Sales Analysis](screenshots/02-sales-analysis.png) |

| Profitability Analysis | Customer & Product Insights |
| --- | --- |
| ![Profitability Analysis](screenshots/03-profitability-analysis.png) | ![Customer & Product Insights](screenshots/04-customer-product-insights.png) |

| Geography & Channel Performance | Targets & Trends |
| --- | --- |
| ![Geography & Channel Performance](screenshots/05-geography-channel-performance.png) | ![Targets & Trends](screenshots/06-targets-trends.png) |

See [screenshots/README.md](screenshots/README.md) for the export and replacement workflow.

## Skills Demonstrated

- Power BI project framing
- Synthetic business data generation
- Dimensional modeling
- DAX design
- Power Query planning
- Executive dashboard architecture
- Documentation for GitHub and interviews
- Business storytelling and recommendation writing

## Future Improvements

- Add a fully assembled PBIP artifact
- Replace preview renders with native Power BI Desktop exports
- Include forecast and budget scenarios
- Add drillthrough pages and tooltip design
- Track customer retention and repeat purchase behavior
- Introduce rep-level quota analysis and incentive views
