# Data Dictionary

## Raw Tables

### `sales_transactions.csv`

| Column | Type | Description |
| --- | --- | --- |
| Order ID | text | Unique order identifier at header level |
| Order Line Number | whole number | Line number within the order |
| Order Date | date | Transaction date used for the main reporting calendar |
| Ship Date | date | Fulfillment date, available for logistics analysis |
| Customer ID | text | Natural key for the customer |
| Customer Name | text | Customer display name |
| Segment | text | Customer segment: Consumer, Small Business, or Enterprise |
| Country | text | Country name |
| Region | text | Commercial region |
| State | text | State code |
| City | text | City name |
| Product ID | text | Natural key for the product |
| Product Name | text | Product display name |
| Category | text | High-level product category |
| Sub-Category | text | Product sub-category |
| Sales Amount | decimal | Net sales after discount |
| Quantity | whole number | Units sold on the line |
| Unit Price | decimal | Selling price before quantity multiplication |
| Gross Sales Amount | decimal | Gross sales before discount |
| Discount | decimal | Discount percentage applied to the line |
| Discount Amount | decimal | Value of the discount granted |
| Cost | decimal | Estimated cost amount for the line |
| Profit | decimal | Sales minus cost |
| Sales Channel | text | Channel used for the sale |
| Sales Rep | text | Assigned sales representative |
| Returned Flag | whole number | Binary return indicator |

### `monthly_targets.csv`

| Column | Type | Description |
| --- | --- | --- |
| Target Month | date | First day of the target month |
| Region | text | Regional target assignment |
| Sales Channel | text | Channel target assignment |
| Sales Target | decimal | Monthly sales target amount |

### `customers_master.csv`

| Column | Type | Description |
| --- | --- | --- |
| Customer ID | text | Customer key |
| Customer Name | text | Customer name |
| Segment | text | Business segment |
| Country | text | Country |
| Region | text | Home region |
| State | text | Home state |
| City | text | Home city |

### `products_master.csv`

| Column | Type | Description |
| --- | --- | --- |
| Product ID | text | Product key |
| Product Name | text | Product name |
| Category | text | Product category |
| Sub-Category | text | Product sub-category |
| Base Price | decimal | Synthetic baseline list price used during generation |
| Base Cost Ratio | decimal | Baseline cost profile used during generation |
| Discount Sensitivity | decimal | Relative sensitivity to price cuts |
| Demand Weight | decimal | Relative frequency in transaction generation |
| Quantity Base | decimal | Baseline quantity profile |
| Return Bias | decimal | Product-specific return bias |

### `channels_master.csv`

| Column | Type | Description |
| --- | --- | --- |
| Sales Channel | text | Channel name |
| Volume Weight | decimal | Relative order allocation |
| Discount Bias | decimal | Channel-specific discount pressure |
| Cost Bias | decimal | Channel-specific cost adjustment |
| Return Bias | decimal | Channel-specific return tendency |
| Lead Days | decimal | Average shipping lead time |

### `sales_reps_master.csv`

| Column | Type | Description |
| --- | --- | --- |
| Sales Rep | text | Sales representative name |
| Home Region | text | Main operating region |

## Processed Model Tables

### `fact_sales.csv`

Each row represents one order line at the `order x product x order date` grain.

| Column | Type | Description |
| --- | --- | --- |
| SalesKey | whole number | Surrogate row key |
| OrderID | text | Order identifier |
| OrderLineNumber | whole number | Line position inside the order |
| OrderDateKey | whole number | Active date key |
| ShipDateKey | whole number | Inactive shipment date key |
| CustomerKey | whole number | Link to `dim_customer` |
| GeographyKey | whole number | Link to `dim_geography` |
| RegionKey | whole number | Link to `dim_region` for regional target alignment |
| ProductKey | whole number | Link to `dim_product` |
| ChannelKey | whole number | Link to `dim_channel` |
| SalesRepKey | whole number | Link to `dim_sales_rep` |
| SalesAmount | decimal | Net sales |
| GrossSalesAmount | decimal | Gross sales before discount |
| DiscountAmount | decimal | Discount amount |
| DiscountPct | decimal | Discount percentage |
| Quantity | whole number | Units sold |
| UnitPrice | decimal | Unit selling price |
| CostAmount | decimal | Cost amount |
| ProfitAmount | decimal | Profit amount |
| ReturnedFlag | whole number | Return indicator |

### `fact_targets.csv`

Each row represents a monthly target at the `month x region x channel` grain.

| Column | Type | Description |
| --- | --- | --- |
| TargetKey | whole number | Surrogate key |
| DateKey | whole number | Link to `dim_date` |
| RegionKey | whole number | Link to `dim_region` |
| ChannelKey | whole number | Link to `dim_channel` |
| SalesTargetAmount | decimal | Monthly target amount |

### `dim_date.csv`

| Column | Type | Description |
| --- | --- | --- |
| DateKey | whole number | Surrogate key in `YYYYMMDD` format |
| Date | date | Calendar date |
| Year | whole number | Calendar year |
| Quarter | text | Quarter label |
| Month Number | whole number | Month number for sorting |
| Month Name | text | Month display label |
| Year-Month | text | Month grain label |
| Week Number | whole number | ISO week |
| Is Current Year | whole number | Flag for the max year in the dataset |

### `dim_product.csv`

| Column | Type | Description |
| --- | --- | --- |
| ProductKey | whole number | Surrogate key |
| ProductID | text | Natural product identifier |
| ProductName | text | Product name |
| Category | text | Category |
| SubCategory | text | Sub-category |

### `dim_customer.csv`

| Column | Type | Description |
| --- | --- | --- |
| CustomerKey | whole number | Surrogate key |
| CustomerID | text | Natural customer identifier |
| CustomerName | text | Customer name |
| Segment | text | Customer segment |
| GeographyKey | whole number | Home geography key |

### `dim_geography.csv`

| Column | Type | Description |
| --- | --- | --- |
| GeographyKey | whole number | Surrogate key |
| Country | text | Country |
| Region | text | Region |
| State | text | State |
| City | text | City |

### `dim_region.csv`

| Column | Type | Description |
| --- | --- | --- |
| RegionKey | whole number | Surrogate key |
| Country | text | Country |
| Region | text | Region |

### `dim_channel.csv`

| Column | Type | Description |
| --- | --- | --- |
| ChannelKey | whole number | Surrogate key |
| SalesChannel | text | Channel name |

### `dim_sales_rep.csv`

| Column | Type | Description |
| --- | --- | --- |
| SalesRepKey | whole number | Surrogate key |
| SalesRep | text | Sales representative |
| HomeRegion | text | Rep home region |

