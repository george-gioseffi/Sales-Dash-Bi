# Reproduction Guide

## 1. Install Requirements

```bash
pip install -r requirements.txt
```

## 2. Rebuild The Data Assets

```bash
python scripts/run_full_build.py
```

Expected outputs:

- Raw tables in `data/raw/`
- Star-schema tables in `data/processed/`

## 3. Build The Report In Power BI Desktop

1. Open Power BI Desktop.
2. Load all CSVs from `data/processed/`.
3. Rename tables to the model names documented in `docs/dax-measures.md`.
4. Create the relationships listed in `docs/data-model.md`.
5. Mark `dim_date[Date]` as the model date table.
6. Sort `dim_date[Month Name]` by `dim_date[Month Number]`.
7. Create the DAX measures from `docs/dax-measures.md`.
8. Import the theme from `assets/theme/sales-performance-theme.json`.
9. Build the pages from `docs/dashboard-blueprint.md`.
10. Export screenshots into `screenshots/`.

## 4. Generate Portfolio Preview Images

If you want immediate GitHub-ready visuals before exporting native Power BI screenshots:

```bash
python scripts/generate_dashboard_previews.py
```

## 5. Recommended Slicer Design

- Global slicers: Date, Region, Sales Channel, Category
- Diagnostic slicers where relevant: Segment, SubCategory

## 6. Final Manual Steps

These steps still require Power BI Desktop:

- Final page composition
- Bookmark and tooltip configuration
- Screenshot export
- Optional PBIP save and commit
