# Modeling Rationale

## Why A Star Schema

The report is meant to support both executive storytelling and technical interview discussion. A star schema keeps the semantic model readable, improves measure behavior, and avoids the ambiguity that typically appears when multiple descriptive columns live inside a single wide fact table.

## Why Separate Sales And Targets

Sales and targets operate at different grains and should not be blended into one table. Sales are transactional; targets are monthly planning data. Keeping them separate preserves accuracy, simplifies variance measures, and mirrors how planning data is usually handled in real business models.

## Why Add `dim_region`

`dim_geography` is useful for state and city analysis, but target rows exist at region level. Adding `dim_region` prevents target duplication and gives the dashboard a clean executive layer for regional comparison.

## Why Keep Both Order Date And Ship Date

Order date is the primary analytical timeline, while ship date creates room for future fulfillment analysis. Modeling both from the start improves extensibility without complicating the initial dashboard build.

