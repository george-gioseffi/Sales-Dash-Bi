# DAX Measures

This measure library assumes the following model names in Power BI:

- `fact_sales`
- `fact_targets`
- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_geography`
- `dim_region`
- `dim_channel`
- `dim_sales_rep`

`dim_date[Date]` should be marked as the official date column before using time-intelligence measures.

## Core Metrics

### 1. Total Sales

```DAX
Total Sales =
SUM ( fact_sales[SalesAmount] )
```

Description: Net sales after discount.  
Usage: Main KPI cards, trend lines, category and region comparisons.

### 2. Gross Sales

```DAX
Gross Sales =
SUM ( fact_sales[GrossSalesAmount] )
```

Description: Sales before discount.  
Usage: Discount analysis and gross-to-net bridge logic.

### 3. Total Profit

```DAX
Total Profit =
SUM ( fact_sales[ProfitAmount] )
```

Description: Total profit contribution.  
Usage: KPI cards, profitability pages, scatter plots, and ranking visuals.

### 4. Total Cost

```DAX
Total Cost =
SUM ( fact_sales[CostAmount] )
```

Description: Total cost absorbed by sold items.  
Usage: Margin calculations and revenue-to-cost comparisons.

### 5. Discount Amount

```DAX
Discount Amount =
SUM ( fact_sales[DiscountAmount] )
```

Description: Absolute value given away through discounting.  
Usage: Discount monitoring cards and profitability diagnostics.

### 6. Total Orders

```DAX
Total Orders =
DISTINCTCOUNT ( fact_sales[OrderID] )
```

Description: Number of distinct orders.  
Usage: KPI cards, average order value, and channel efficiency analysis.

### 7. Total Quantity

```DAX
Total Quantity =
SUM ( fact_sales[Quantity] )
```

Description: Total units sold.  
Usage: Volume analysis, product mix, and low-margin volume checks.

### 8. Total Customers

```DAX
Total Customers =
DISTINCTCOUNT ( dim_customer[CustomerKey] )
```

Description: Distinct customers in current filter context.  
Usage: Customer mix cards and sales-per-customer analysis.

### 9. Average Order Value

```DAX
Average Order Value =
DIVIDE ( [Total Sales], [Total Orders] )
```

Description: Average sales value per order.  
Usage: Executive overview and channel comparison.

### 10. Average Unit Price

```DAX
Average Unit Price =
DIVIDE ( [Total Sales], [Total Quantity] )
```

Description: Average realized revenue per unit sold.  
Usage: Product mix and pricing diagnostics.

## Profitability

### 11. Profit Margin %

```DAX
Profit Margin % =
DIVIDE ( [Total Profit], [Total Sales] )
```

Description: Profit generated for each currency unit of sales.  
Usage: Margin cards, category comparison, and channel efficiency.

### 12. Discount %

```DAX
Discount % =
DIVIDE ( [Discount Amount], [Gross Sales] )
```

Description: Share of gross sales conceded as discount.  
Usage: Executive KPI, discount-to-margin analysis, and price policy review.

### 13. Returned Lines

```DAX
Returned Lines =
SUM ( fact_sales[ReturnedFlag] )
```

Description: Count of lines flagged as returned.  
Usage: Return tracking and channel operational diagnostics.

### 14. Return Rate %

```DAX
Return Rate % =
DIVIDE ( [Returned Lines], COUNTROWS ( fact_sales ) )
```

Description: Returned line share in the current filter context.  
Usage: KPI cards and channel/service quality checks.

### 15. Profit per Order

```DAX
Profit per Order =
DIVIDE ( [Total Profit], [Total Orders] )
```

Description: Average profit generated per order.  
Usage: Channel efficiency and profitability benchmarking.

### 16. Sales per Customer

```DAX
Sales per Customer =
DIVIDE ( [Total Sales], [Total Customers] )
```

Description: Average revenue generated per active customer.  
Usage: Segment and customer concentration analysis.

## Time Intelligence

### 17. Sales PY

```DAX
Sales PY =
CALCULATE ( [Total Sales], DATEADD ( dim_date[Date], -1, YEAR ) )
```

Description: Sales in the same period last year.  
Usage: YoY cards, trend visuals, and annual performance comparison.

### 18. Sales YoY %

```DAX
Sales YoY % =
DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )
```

Description: Year-over-year sales growth rate.  
Usage: Executive overview and trend analysis.

### 19. Profit PY

```DAX
Profit PY =
CALCULATE ( [Total Profit], DATEADD ( dim_date[Date], -1, YEAR ) )
```

Description: Profit in the same period last year.  
Usage: YoY margin storyline and profitability trend analysis.

### 20. Profit YoY %

```DAX
Profit YoY % =
DIVIDE ( [Total Profit] - [Profit PY], [Profit PY] )
```

Description: Year-over-year profit growth rate.  
Usage: Profitability page and executive summary.

### 21. Sales PM

```DAX
Sales PM =
CALCULATE ( [Total Sales], DATEADD ( dim_date[Date], -1, MONTH ) )
```

Description: Sales in the previous month.  
Usage: Month-over-month trend diagnostics.

### 22. Sales MoM

```DAX
Sales MoM =
[Total Sales] - [Sales PM]
```

Description: Absolute sales change versus previous month.  
Usage: Trend cards and acceleration or slowdown views.

### 23. Profit PM

```DAX
Profit PM =
CALCULATE ( [Total Profit], DATEADD ( dim_date[Date], -1, MONTH ) )
```

Description: Profit in the previous month.  
Usage: Profit trend tracking.

### 24. Profit MoM

```DAX
Profit MoM =
[Total Profit] - [Profit PM]
```

Description: Absolute profit change versus previous month.  
Usage: Trend cards and profitability movement analysis.

### 25. Running Sales

```DAX
Running Sales =
CALCULATE (
    [Total Sales],
    FILTER (
        ALLSELECTED ( dim_date[Date] ),
        dim_date[Date] <= MAX ( dim_date[Date] )
    )
)
```

Description: Cumulative sales over the visible date range.  
Usage: Running trend lines and year progress views.

### 26. Running Profit

```DAX
Running Profit =
CALCULATE (
    [Total Profit],
    FILTER (
        ALLSELECTED ( dim_date[Date] ),
        dim_date[Date] <= MAX ( dim_date[Date] )
    )
)
```

Description: Cumulative profit over the visible date range.  
Usage: Profit accumulation and contribution storytelling.

## Targets

### 27. Sales Target

```DAX
Sales Target =
SUM ( fact_targets[SalesTargetAmount] )
```

Description: Planned sales amount from the target table.  
Usage: KPI cards, bullet charts, and target tracking visuals.

### 28. Sales vs Target Variance

```DAX
Sales vs Target Variance =
[Total Sales] - [Sales Target]
```

Description: Absolute gap between actual sales and target.  
Usage: Executive cards and variance bars.

### 29. Target Attainment %

```DAX
Target Attainment % =
DIVIDE ( [Total Sales], [Sales Target] )
```

Description: Actual performance as a percentage of target.  
Usage: KPI cards, conditional formatting, and trend review.

### 30. Sales vs Target Variance %

```DAX
Sales vs Target Variance % =
DIVIDE ( [Sales vs Target Variance], [Sales Target] )
```

Description: Relative variance versus plan.  
Usage: Executive target commentary and regional performance comparison.

## Ranking And Contribution

### 31. % of Total Sales

```DAX
% of Total Sales =
DIVIDE (
    [Total Sales],
    CALCULATE (
        [Total Sales],
        REMOVEFILTERS ( dim_product ),
        REMOVEFILTERS ( dim_customer ),
        REMOVEFILTERS ( dim_geography ),
        REMOVEFILTERS ( dim_region ),
        REMOVEFILTERS ( dim_channel ),
        REMOVEFILTERS ( dim_sales_rep )
    )
)
```

Description: Share of sales contribution within the current date context.  
Usage: Contribution bars, matrices, and Pareto-style analysis.

### 32. % of Total Profit

```DAX
% of Total Profit =
DIVIDE (
    [Total Profit],
    CALCULATE (
        [Total Profit],
        REMOVEFILTERS ( dim_product ),
        REMOVEFILTERS ( dim_customer ),
        REMOVEFILTERS ( dim_geography ),
        REMOVEFILTERS ( dim_region ),
        REMOVEFILTERS ( dim_channel ),
        REMOVEFILTERS ( dim_sales_rep )
    )
)
```

Description: Share of profit contribution within the current date context.  
Usage: Profit concentration and mix analysis.

### 33. Rank Region by Sales

```DAX
Rank Region by Sales =
RANKX ( ALL ( dim_region[Region] ), [Total Sales], , DESC, DENSE )
```

Description: Sales ranking across regions.  
Usage: Regional comparison tables and conditional formatting.

### 34. Rank Category by Profit

```DAX
Rank Category by Profit =
RANKX ( ALL ( dim_product[Category] ), [Total Profit], , DESC, DENSE )
```

Description: Profit ranking across categories.  
Usage: Category scorecards and profitability matrices.

