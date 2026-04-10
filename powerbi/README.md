# Power BI Build Notes

## Status

The repository is prepared for a PBIP-style workflow, but a fully generated `.pbip` artifact was not created inside this environment because the final report canvas still requires Power BI Desktop assembly.

What is ready:

- Reproducible raw and processed datasets
- Star schema exports
- DAX measure library
- Theme JSON
- Dashboard blueprint
- Dashboard preview renders in `screenshots/`
- Final report assembly guidance in `powerbi/final-dashboard-handoff.md`

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

## Portfolio Preview Assets

The repository now includes six static dashboard previews generated from the actual project data:

```bash
python scripts/generate_dashboard_previews.py
```

These images are intended to support the GitHub presentation layer until native Power BI Desktop screenshots replace them under the same filenames.

## Suggested PBIP Naming

- Report name: `Sales Performance Analytics`
- Folder name: `powerbi/SalesPerformanceAnalytics/`
- Optional PBIP file: `powerbi/Sales Performance Analytics.pbip`

## Practical Limitation

Because the report file is not generated here, the final PBIP or PBIX artifact, interactive page wiring, and native Power BI screenshot exports still depend on opening Power BI Desktop once on the local machine.

This limitation is intentional and honest. Microsoft documents that PBIX-to-PBIP conversion and PBIR creation are performed through Power BI Desktop's Save As workflow, not through a supported terminal-only conversion path.
