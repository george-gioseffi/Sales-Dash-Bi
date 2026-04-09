# Technical Notes

## Expected Power Query Transformations

The CSV files are already structured for reporting, but the following Power Query steps are still recommended to keep the semantic model clean and explicit:

1. Apply explicit data types to every imported column.
2. Rename tables to the final model names:
   - `fact_sales`
   - `fact_targets`
   - `dim_date`
   - `dim_product`
   - `dim_customer`
   - `dim_geography`
   - `dim_region`
   - `dim_channel`
   - `dim_sales_rep`
3. Remove unused natural-key columns from report view after relationships are validated.
4. Hide surrogate keys in the report layer.
5. Confirm `ReturnedFlag` is whole number and not text.
6. Confirm percentage fields such as `DiscountPct` are modeled as decimals and formatted as percentages.
7. Sort `dim_date[Month Name]` by `dim_date[Month Number]`.
8. Mark `dim_date` as the model date table using `dim_date[Date]`.

## Modeling Notes

- Use `OrderDateKey` as the active relationship for time intelligence.
- Keep `ShipDateKey` as an inactive relationship for future logistics or delivery timing analysis.
- Use `dim_region` in pages that compare actuals versus targets.
- Use `dim_geography` for state and city drilldown where targets are not the primary focus.

## Suggested Formatting

- Currency: BRL or a neutral currency format, depending on presentation preference
- Percentages: one decimal place for executive pages, two decimals for detail pages
- Quantities and orders: thousand separators, zero decimals

## Power BI Build Sequence

1. Load all processed CSVs from `data/processed/`.
2. Create relationships exactly as defined in `docs/data-model.md`.
3. Mark `dim_date[Date]` as the date table.
4. Import the theme file from `assets/theme/sales-performance-theme.json`.
5. Create DAX measures from `docs/dax-measures.md`.
6. Hide keys and technical columns.
7. Build pages according to `docs/dashboard-blueprint.md`.

