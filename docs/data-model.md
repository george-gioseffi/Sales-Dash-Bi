# Data Model

## Modeling Approach

The model follows a star schema centered on transactional sales and monthly targets. The main objective is to keep analytical logic simple, performant, and easy to explain in both technical and business settings.

## Fact Tables

| Table | Grain | Purpose |
| --- | --- | --- |
| `fact_sales` | One order line per product per order date | Core revenue, volume, discount, cost, profit, and return analysis |
| `fact_targets` | One row per month, region, and channel | Target tracking and variance analysis |

### Fact Grain Statements

- `fact_sales`: each row represents a sales line item at the `order x product x order date` grain.
- `fact_targets`: each row represents a monthly target at the `month x region x sales channel` grain.

## Dimension Tables

| Table | Primary Key | Main Role |
| --- | --- | --- |
| `dim_date` | `DateKey` | Shared time intelligence backbone |
| `dim_product` | `ProductKey` | Category, sub-category, and product analysis |
| `dim_customer` | `CustomerKey` | Segment and customer mix analysis |
| `dim_geography` | `GeographyKey` | City and state-level slicing |
| `dim_region` | `RegionKey` | Region-level target alignment and executive comparison |
| `dim_channel` | `ChannelKey` | Channel performance analysis |
| `dim_sales_rep` | `SalesRepKey` | Sales rep comparison |

## Relationships

Recommended Power BI relationships:

| From | To | Cardinality | Status |
| --- | --- | --- | --- |
| `dim_date[DateKey]` | `fact_sales[OrderDateKey]` | 1:* | Active |
| `dim_date[DateKey]` | `fact_sales[ShipDateKey]` | 1:* | Inactive |
| `dim_date[DateKey]` | `fact_targets[DateKey]` | 1:* | Active |
| `dim_product[ProductKey]` | `fact_sales[ProductKey]` | 1:* | Active |
| `dim_customer[CustomerKey]` | `fact_sales[CustomerKey]` | 1:* | Active |
| `dim_geography[GeographyKey]` | `fact_sales[GeographyKey]` | 1:* | Active |
| `dim_region[RegionKey]` | `fact_sales[RegionKey]` | 1:* | Active |
| `dim_region[RegionKey]` | `fact_targets[RegionKey]` | 1:* | Active |
| `dim_channel[ChannelKey]` | `fact_sales[ChannelKey]` | 1:* | Active |
| `dim_channel[ChannelKey]` | `fact_targets[ChannelKey]` | 1:* | Active |
| `dim_sales_rep[SalesRepKey]` | `fact_sales[SalesRepKey]` | 1:* | Active |

## Analytical Assumptions

- `dim_date` should be marked as the date table using `dim_date[Date]`.
- Regional slicers used on target pages should come from `dim_region`, not from `dim_geography`, to preserve target grain integrity.
- `ShipDateKey` is included for future logistics analysis, but the report should use `OrderDateKey` as the default active calendar relationship.
- Returns are modeled as operational flags, not as fully reversed transactions.

