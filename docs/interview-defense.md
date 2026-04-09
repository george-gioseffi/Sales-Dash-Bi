# Interview Defense

## Why did you use a star schema?

Because the report combines transactional sales and monthly targets, a star schema keeps the model easier to reason about, improves DAX behavior, and makes the semantic layer much more scalable than a single denormalized table.

## Why separate sales and targets?

They are different business processes with different grains. Sales are transactional at order-line level, while targets are monthly planning data by region and channel. Separating them preserves analytical accuracy.

## Why focus on profit margin instead of only revenue?

Revenue alone can hide inefficient growth. In this project, some high-volume sub-categories such as printers and tables contribute meaningful sales but underperform on margin, which is exactly the kind of issue leadership needs to see.

## Why did you choose these visuals?

I prioritized visuals that answer business questions quickly: KPI cards for executive summary, line charts for trend, bars for ranking, and a scatter plot for the sales-versus-profit relationship. Every chart has a decision purpose.

## What business decisions can this dashboard support?

It supports pricing review, regional focus allocation, channel prioritization, portfolio optimization, and target management. The model is designed to help leadership decide where to push, where to protect margin, and where to intervene.

## How would you evolve this project?

I would add budget and forecast scenarios, customer retention logic, rep-level quotas, inventory coverage, and a profitability waterfall. I would also package the final report as PBIP with deployment-ready metadata.

## Why did you add a separate region dimension?

Targets are defined at regional grain, while geography drilldown goes to city and state. A separate region dimension prevents target duplication and keeps actual-versus-target analysis clean.

