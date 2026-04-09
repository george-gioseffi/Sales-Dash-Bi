# Quality Checks

The following checks were used to validate the generated data before documenting the dashboard.

## Structural Checks

| Check | Result |
| --- | --- |
| Sales transaction rows | 9,586 |
| Distinct orders | 4,407 |
| Distinct customers | 257 |
| Distinct products | 28 |
| Distinct regions | 5 |
| Distinct channels | 4 |
| Monthly target rows | 480 |
| Calendar rows | 731 |

## Validation Results

| Validation | Result |
| --- | --- |
| Null scan on key sales columns | Passed: 0 nulls |
| Null scan on amount columns | Passed: 0 nulls |
| Date range validation | Passed: 2024-01-01 to 2025-12-31 |
| Ship date before order date | Passed: 0 rows |
| Negative sales values | Passed: 0 rows |
| Negative cost values | Passed: 0 rows |
| Gross sales lower than net sales | Passed: 0 rows |
| Profit consistency check (`Sales - Cost = Profit`) | Passed: 100% of rows within tolerance |
| Target completeness by month-region-channel | Passed: 480 of 480 expected rows |

## Business Sanity Checks

- Sales growth from 2024 to 2025 is positive but not extreme: `+12.99%`
- Profit growth is positive but slower than sales growth: `+10.20%`
- Profit margin softened from `25.07%` to `24.45%`, creating a believable pricing and mix discussion
- Overall target attainment averages `98.18%`, with both over-target and under-target combinations
- Return rate is low but non-zero at `1.74%`, with Online showing the highest operational return pressure

