# Presentation Script

This project simulates a national company operating across Brazil through online, retail, distributor, and direct sales channels. The business sells technology, furniture, and office supply products, and the main challenge was to understand not just where revenue comes from, but where it converts efficiently into profit and where commercial execution is missing target.

I built the project end to end. First, I generated a reproducible synthetic dataset with 9,586 transaction rows covering two full years, from January 2024 through December 2025. I also created a separate monthly target table at the month, region, and channel grain so the report could support real target-attainment analysis instead of only descriptive sales reporting.

From a modeling perspective, I used a star schema with `fact_sales` and `fact_targets` at the center, supported by date, product, customer, geography, region, channel, and sales rep dimensions. I kept order date as the active reporting calendar and preserved ship date for future logistics analysis. I also introduced a dedicated region dimension so target analysis would stay accurate even though sales geography can drill down to city and state.

On the KPI side, I designed the measure layer around four questions: how big is the business, how profitable is it, how is it trending, and are we meeting plan. That includes metrics such as Total Sales, Total Profit, Profit Margin, Average Order Value, Discount %, Return Rate, YoY growth, MoM movement, Sales Target, Target Attainment, and ranking measures for regions and categories.

The most interesting insights come from the mix. Sales grew almost 13% in 2025, but profit grew more slowly and margin softened from 25.1% to 24.5%, which suggests growth came with some efficiency pressure. Southeast is the largest revenue region, but it also shows the lowest average target attainment among regions, making it a scale market that still deserves tighter commercial control. On the product side, technology dominates sales, but printers and tables are clear examples of volume that does not convert well into profit. Channel analysis also shows that Direct Sales brings less volume than Online, but produces stronger margin and more profit per order.

If I were presenting this to leadership, my recommendations would be to review discount policy in low-margin sub-categories, protect and scale the most efficient channels, and monitor regional execution with more focus on target consistency rather than only topline sales. Overall, the goal of this project was to show strong Power BI thinking across data generation, modeling, DAX, business framing, and dashboard design.

