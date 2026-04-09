# Power BI Build Notes

## Status

The repository is prepared for a PBIP-style workflow, but a fully generated `.pbip` artifact was not created inside this environment because Power BI Desktop is required for the final report file generation and packaging.

What is ready:

- Reproducible raw and processed datasets
- Star schema exports
- DAX measure library
- Theme JSON
- Dashboard blueprint
- Screenshot capture instructions

## Recommended Build Flow In Power BI Desktop

1. Create a new Power BI Desktop file.
2. Import all CSV files from `data/processed/`.
3. Rename the imported tables to the documented model names.
4. Build the relationships from `docs/data-model.md`.
5. Mark `dim_date[Date]` as the date table.
6. Sort `dim_date[Month Name]` by `dim_date[Month Number]`.
7. Create the DAX measures from `docs/dax-measures.md`.
8. Import `assets/theme/sales-performance-theme.json`.
9. Build pages following `docs/dashboard-blueprint.md`.
10. Save the report as PBIP if desired and export screenshots to `screenshots/`.

## Suggested PBIP Naming

- Report name: `Sales Performance Analytics`
- Folder name: `powerbi/SalesPerformanceAnalytics/`
- Optional PBIP file: `powerbi/Sales Performance Analytics.pbip`

## Practical Limitation

Because the report file is not generated here, the final dashboard pages, bookmarks, tooltip pages, and screenshots still depend on opening Power BI Desktop once on the local machine.

