from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch

from project_config import PROJECT_ROOT


SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
RAW_DIR = PROJECT_ROOT / "data" / "raw"

BG = "#F7F6F3"
PANEL = "#FFFFFF"
TEXT = "#1F2933"
MUTED = "#6B7280"
BORDER = "#E6E1D9"
NAVY = "#123B5D"
GREEN = "#2C6E49"
RED = "#D1495B"
SLATE = "#7C8EA3"
GOLD = "#E8A24C"
TEAL = "#81B29A"


def fmt_currency(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def fmt_int(value: float) -> str:
    return f"{int(round(value)):,}"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(
        RAW_DIR / "sales_transactions.csv",
        parse_dates=["Order Date", "Ship Date"],
    )
    targets = pd.read_csv(
        RAW_DIR / "monthly_targets.csv",
        parse_dates=["Target Month"],
    )

    sales["MonthStart"] = sales["Order Date"].dt.to_period("M").dt.to_timestamp()
    sales["Year"] = sales["Order Date"].dt.year
    sales["Month Label"] = sales["MonthStart"].dt.strftime("%b %y")
    return sales, targets


def build_metrics(sales: pd.DataFrame, targets: pd.DataFrame) -> dict[str, pd.DataFrame | float]:
    monthly_sales = (
        sales.groupby("MonthStart", as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum"),
            DiscountAmount=("Discount Amount", "sum"),
            GrossSales=("Gross Sales Amount", "sum"),
            ReturnedLines=("Returned Flag", "sum"),
        )
        .sort_values("MonthStart")
    )
    monthly_targets = (
        targets.groupby("Target Month", as_index=False)["Sales Target"]
        .sum()
        .rename(columns={"Target Month": "MonthStart", "Sales Target": "SalesTarget"})
        .sort_values("MonthStart")
    )
    monthly = monthly_sales.merge(monthly_targets, on="MonthStart", how="left")
    monthly["TargetAttainment"] = monthly["Sales"] / monthly["SalesTarget"]
    monthly["Variance"] = monthly["Sales"] - monthly["SalesTarget"]
    monthly["SalesYoY"] = monthly["Sales"].pct_change(12)
    monthly["ProfitYoY"] = monthly["Profit"].pct_change(12)

    region = (
        sales.groupby("Region", as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            DiscountPct=("Discount", "mean"),
        )
        .sort_values("Sales", ascending=False)
    )
    region["Margin"] = region["Profit"] / region["Sales"]
    region["ProfitPerOrder"] = region["Profit"] / region["Orders"]

    channel = (
        sales.groupby("Sales Channel", as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
            DiscountPct=("Discount", "mean"),
            ReturnedFlag=("Returned Flag", "mean"),
        )
        .sort_values("Sales", ascending=False)
    )
    channel["Margin"] = channel["Profit"] / channel["Sales"]
    channel["ProfitPerOrder"] = channel["Profit"] / channel["Orders"]
    channel["SalesShare"] = channel["Sales"] / channel["Sales"].sum()

    category = (
        sales.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            DiscountPct=("Discount", "mean"),
        )
        .sort_values("Sales", ascending=False)
    )
    category["Margin"] = category["Profit"] / category["Sales"]
    category["SalesShare"] = category["Sales"] / category["Sales"].sum()

    subcategory = (
        sales.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            DiscountPct=("Discount", "mean"),
        )
        .sort_values("Sales", ascending=False)
    )
    subcategory["Margin"] = subcategory["Profit"] / subcategory["Sales"]

    segment = (
        sales.groupby("Segment", as_index=False)
        .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"))
        .sort_values("Sales", ascending=False)
    )
    segment["Margin"] = segment["Profit"] / segment["Sales"]

    segment_year = (
        sales.groupby(["Segment", "Year"], as_index=False)
        .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"))
    )
    segment_pivot = segment_year.pivot(index="Segment", columns="Year", values="Sales")
    segment_growth = (
        ((segment_pivot[2025] / segment_pivot[2024]) - 1)
        .sort_values(ascending=False)
        .rename("YoYGrowth")
        .reset_index()
    )

    product = (
        sales.groupby("Product Name", as_index=False)
        .agg(
            Sales=("Sales Amount", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
        )
        .sort_values("Sales", ascending=False)
    )
    product["Margin"] = product["Profit"] / product["Sales"]
    product["CumulativeSalesShare"] = product["Sales"].cumsum() / product["Sales"].sum()
    product["Rank"] = np.arange(1, len(product) + 1)

    month_channel = (
        sales.groupby(["MonthStart", "Sales Channel"], as_index=False)["Sales Amount"]
        .sum()
        .rename(columns={"Sales Amount": "Sales"})
    )
    region_channel_sales = (
        sales.pivot_table(
            index="Region",
            columns="Sales Channel",
            values="Sales Amount",
            aggfunc="sum",
        )
        .fillna(0)
    )
    region_channel_margin = (
        sales.pivot_table(
            index="Region",
            columns="Sales Channel",
            values="Profit",
            aggfunc="sum",
        )
        / sales.pivot_table(
            index="Region",
            columns="Sales Channel",
            values="Sales Amount",
            aggfunc="sum",
        )
    ).fillna(0)

    monthly_region = (
        sales.groupby(["MonthStart", "Region"], as_index=False)["Sales Amount"]
        .sum()
        .rename(columns={"Sales Amount": "Sales"})
    )
    monthly_region_2025 = monthly_region[monthly_region["MonthStart"].dt.year == 2025]
    monthly_region_2025 = monthly_region_2025.pivot(
        index="Region", columns="MonthStart", values="Sales"
    ).fillna(0)

    actual_targets = (
        sales.groupby(["MonthStart", "Region", "Sales Channel"], as_index=False)["Sales Amount"]
        .sum()
        .rename(columns={"Sales Amount": "ActualSales"})
    )
    actual_targets = actual_targets.merge(
        targets.rename(columns={"Target Month": "MonthStart", "Sales Target": "SalesTarget"}),
        on=["MonthStart", "Region", "Sales Channel"],
        how="left",
    )
    actual_targets["Attainment"] = actual_targets["ActualSales"] / actual_targets["SalesTarget"]

    region_attainment = (
        actual_targets.groupby("Region", as_index=False)
        .agg(ActualSales=("ActualSales", "sum"), SalesTarget=("SalesTarget", "sum"))
        .sort_values("ActualSales", ascending=False)
    )
    region_attainment["Attainment"] = region_attainment["ActualSales"] / region_attainment["SalesTarget"]

    channel_attainment = (
        actual_targets.groupby("Sales Channel", as_index=False)
        .agg(ActualSales=("ActualSales", "sum"), SalesTarget=("SalesTarget", "sum"))
        .sort_values("ActualSales", ascending=False)
    )
    channel_attainment["Attainment"] = channel_attainment["ActualSales"] / channel_attainment["SalesTarget"]

    yearly = (
        sales.groupby("Year", as_index=False)
        .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    )
    yearly["Margin"] = yearly["Profit"] / yearly["Sales"]

    kpis = {
        "total_sales": sales["Sales Amount"].sum(),
        "total_profit": sales["Profit"].sum(),
        "profit_margin": sales["Profit"].sum() / sales["Sales Amount"].sum(),
        "total_orders": sales["Order ID"].nunique(),
        "aov": sales.groupby("Order ID")["Sales Amount"].sum().mean(),
        "return_rate": sales["Returned Flag"].mean(),
        "target_attainment": monthly["Sales"].sum() / monthly["SalesTarget"].sum(),
        "discount_pct": sales["Discount Amount"].sum() / sales["Gross Sales Amount"].sum(),
        "profit_per_order": sales["Profit"].sum() / sales["Order ID"].nunique(),
        "total_customers": sales["Customer ID"].nunique(),
        "sales_per_customer": sales["Sales Amount"].sum() / sales["Customer ID"].nunique(),
        "top_10_share": product.head(10)["Sales"].sum() / product["Sales"].sum(),
        "enterprise_growth": float(
            segment_growth.loc[segment_growth["Segment"] == "Enterprise", "YoYGrowth"].iloc[0]
        ),
        "sales_target": monthly["SalesTarget"].sum(),
        "target_variance": monthly["Sales"].sum() - monthly["SalesTarget"].sum(),
        "sales_yoy": float(
            (yearly.loc[yearly["Year"] == 2025, "Sales"].iloc[0] / yearly.loc[yearly["Year"] == 2024, "Sales"].iloc[0]) - 1
        ),
        "profit_yoy": float(
            (yearly.loc[yearly["Year"] == 2025, "Profit"].iloc[0] / yearly.loc[yearly["Year"] == 2024, "Profit"].iloc[0]) - 1
        ),
    }

    return {
        "monthly": monthly,
        "region": region,
        "channel": channel,
        "category": category,
        "subcategory": subcategory,
        "segment": segment,
        "segment_year": segment_year,
        "segment_growth": segment_growth,
        "product": product,
        "month_channel": month_channel,
        "region_channel_sales": region_channel_sales,
        "region_channel_margin": region_channel_margin,
        "monthly_region_2025": monthly_region_2025,
        "region_attainment": region_attainment,
        "channel_attainment": channel_attainment,
        "kpis": kpis,
    }


def style_page() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.facecolor": PANEL,
            "figure.facecolor": BG,
            "axes.edgecolor": BORDER,
            "axes.labelcolor": TEXT,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": TEXT,
            "axes.titleweight": "bold",
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "grid.color": BORDER,
            "grid.alpha": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
        }
    )


def add_page_header(fig: plt.Figure, title: str, subtitle: str, filters: list[str]) -> None:
    fig.text(0.03, 0.965, title, fontsize=24, fontweight="bold", color=TEXT)
    fig.text(0.03, 0.938, subtitle, fontsize=10.5, color=MUTED)
    fig.text(0.97, 0.965, " | ".join(filters), ha="right", fontsize=9.5, color=MUTED)


def add_card(ax: plt.Axes, title: str, value: str, accent: str, subtitle: str | None = None) -> None:
    ax.set_axis_off()
    text_color = "#FFFFFF" if accent in {NAVY, GREEN, RED, SLATE} else TEXT
    meta_color = "#F1F5F9" if accent in {NAVY, GREEN, RED, SLATE} else MUTED
    card = FancyBboxPatch(
        (0, 0),
        1,
        1,
        boxstyle="round,pad=0.012,rounding_size=18",
        linewidth=0.8,
        edgecolor=accent,
        facecolor=accent,
        transform=ax.transAxes,
        clip_on=True,
    )
    ax.add_patch(card)
    ax.text(0.05, 0.60, title, fontsize=10, color=meta_color, transform=ax.transAxes)
    ax.text(0.05, 0.26, value, fontsize=22, fontweight="bold", color=text_color, transform=ax.transAxes)
    if subtitle:
        ax.text(0.05, 0.08, subtitle, fontsize=9, color=meta_color, transform=ax.transAxes)


def setup_panel(ax: plt.Axes, title: str, subtitle: str | None = None) -> None:
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", linewidth=0.6)
    ax.set_title(title, loc="left", pad=12, fontsize=12, fontweight="bold")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=9, color=MUTED)


def label_barh(ax: plt.Axes, values: pd.Series, formatter=fmt_currency) -> None:
    offset = values.max() * 0.01
    for index, value in enumerate(values):
        ax.text(value + offset, index, formatter(value), va="center", fontsize=8.5, color=MUTED)


def format_month_axis(ax: plt.Axes) -> None:
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")


def create_executive_overview(metrics: dict[str, object]) -> None:
    monthly = metrics["monthly"]
    region = metrics["region"]
    category = metrics["category"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Executive Overview",
        "Clean executive snapshot of revenue scale, margin quality, target delivery, and primary growth drivers.",
        ["Date", "Region", "Sales Channel", "Category"],
    )
    grid = fig.add_gridspec(12, 14, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Total Sales", fmt_currency(kpis["total_sales"]), NAVY, "Net revenue"),
        ("Total Profit", fmt_currency(kpis["total_profit"]), GREEN, "Contribution after cost"),
        ("Profit Margin %", fmt_pct(kpis["profit_margin"]), GREEN, "Revenue quality"),
        ("Total Orders", fmt_int(kpis["total_orders"]), SLATE, "Distinct orders"),
        ("Average Order Value", fmt_currency(kpis["aov"]), NAVY, "Average ticket size"),
        ("Return Rate %", fmt_pct(kpis["return_rate"]), RED, "Returned line share"),
        ("Target Attainment %", fmt_pct(kpis["target_attainment"]), GOLD, "Actual vs plan"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 2 : idx * 2 + 2]), *card)

    ax1 = fig.add_subplot(grid[2:7, 0:8])
    setup_panel(ax1, "Monthly Sales And Profit Trend", "Sales and profit direction across the 24-month window")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.7, label="Sales")
    ax1.fill_between(monthly["MonthStart"], monthly["Sales"], color=NAVY, alpha=0.10)
    ax1.set_ylabel("Sales")
    format_month_axis(ax1)
    ax1b = ax1.twinx()
    ax1b.plot(monthly["MonthStart"], monthly["Profit"], color=GREEN, linewidth=2.1, label="Profit")
    ax1b.set_ylabel("Profit")
    ax1.legend(loc="upper left", frameon=False)
    ax1b.legend(loc="upper right", frameon=False)

    ax2 = fig.add_subplot(grid[2:7, 8:14])
    setup_panel(ax2, "Actual Sales Vs Target", "Monthly actuals compared with the target plan")
    ax2.plot(monthly["MonthStart"], monthly["SalesTarget"], color=SLATE, linewidth=2.0, linestyle="--", label="Target")
    ax2.plot(monthly["MonthStart"], monthly["Sales"], color=GOLD, linewidth=2.5, label="Actual")
    ax2.fill_between(monthly["MonthStart"], monthly["SalesTarget"], monthly["Sales"], color=GOLD, alpha=0.12)
    format_month_axis(ax2)
    ax2.legend(loc="upper left", frameon=False)

    ax3 = fig.add_subplot(grid[7:12, 0:7])
    setup_panel(ax3, "Top Regions By Sales", "Revenue leaders with margin context")
    region_plot = region.sort_values("Sales", ascending=True)
    ax3.barh(region_plot["Region"], region_plot["Sales"], color=NAVY, alpha=0.92)
    label_barh(ax3, region_plot["Sales"])
    ax3.set_xlabel("Sales")
    for i, row in enumerate(region_plot.itertuples(index=False)):
        ax3.text(row.Sales * 0.02, i, f"Margin {row.Margin * 100:.1f}%", va="center", color="white", fontsize=8.5)

    ax4 = fig.add_subplot(grid[7:12, 7:14])
    setup_panel(ax4, "Category Contribution", "Sales contribution and profitability by category")
    category_plot = category.sort_values("Sales", ascending=True)
    colors = [NAVY, SLATE, TEAL]
    ax4.barh(category_plot["Category"], category_plot["Sales"], color=colors)
    label_barh(ax4, category_plot["Sales"])
    for i, row in enumerate(category_plot.itertuples(index=False)):
        ax4.text(row.Sales * 0.64, i, f"{row.Margin * 100:.1f}% margin", va="center", color="white", fontsize=9)

    fig.savefig(SCREENSHOTS_DIR / "01-executive-overview.png", facecolor=BG)
    plt.close(fig)


def create_sales_analysis(metrics: dict[str, object]) -> None:
    monthly = metrics["monthly"]
    category = metrics["category"]
    subcategory = metrics["subcategory"]
    region = metrics["region"]
    channel = metrics["channel"]
    month_channel = metrics["month_channel"]
    region_channel_sales = metrics["region_channel_sales"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Sales Analysis",
        "Revenue driver view across time, category mix, region scale, and channel contribution.",
        ["Date", "Region", "Sales Channel", "Segment"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Total Sales", fmt_currency(kpis["total_sales"]), NAVY, "Net revenue"),
        ("Total Orders", fmt_int(kpis["total_orders"]), SLATE, "Distinct orders"),
        ("Average Order Value", fmt_currency(kpis["aov"]), GOLD, "Ticket size"),
        ("Total Quantity", fmt_int(monthly["Quantity"].sum()), TEAL, "Units sold"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:6])
    setup_panel(ax1, "Sales Over Time", "Monthly sales trend")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.6)
    ax1.fill_between(monthly["MonthStart"], monthly["Sales"], color=NAVY, alpha=0.12)
    format_month_axis(ax1)

    ax2 = fig.add_subplot(grid[2:6, 6:12])
    setup_panel(ax2, "Sales Mix By Channel Over Time", "Monthly channel contribution")
    pivot = month_channel.pivot(index="MonthStart", columns="Sales Channel", values="Sales").fillna(0)
    ax2.stackplot(
        pivot.index,
        pivot.T.values,
        labels=pivot.columns,
        colors=[NAVY, SLATE, GOLD, TEAL],
        alpha=0.92,
    )
    format_month_axis(ax2)
    ax2.legend(loc="upper left", frameon=False, ncol=2)

    ax3 = fig.add_subplot(grid[6:9, 0:4])
    setup_panel(ax3, "Sales By Category", "Top-level revenue mix")
    cat = category.sort_values("Sales", ascending=True)
    ax3.barh(cat["Category"], cat["Sales"], color=[TEAL, SLATE, NAVY])
    label_barh(ax3, cat["Sales"])

    ax4 = fig.add_subplot(grid[6:9, 4:8])
    setup_panel(ax4, "Top Sub-Categories By Sales", "Largest revenue pockets")
    sub = subcategory.head(8).sort_values("Sales", ascending=True)
    ax4.barh(sub["Sub-Category"], sub["Sales"], color=NAVY)
    label_barh(ax4, sub["Sales"])

    ax5 = fig.add_subplot(grid[6:9, 8:12])
    setup_panel(ax5, "Sales By Region", "Regional revenue scale")
    reg = region.sort_values("Sales", ascending=True)
    ax5.barh(reg["Region"], reg["Sales"], color=SLATE)
    label_barh(ax5, reg["Sales"])

    ax6 = fig.add_subplot(grid[9:12, 0:4])
    setup_panel(ax6, "Sales By Channel", "Channel mix")
    ch = channel.sort_values("Sales", ascending=True)
    ax6.barh(ch["Sales Channel"], ch["Sales"], color=GOLD)
    label_barh(ax6, ch["Sales"])

    ax7 = fig.add_subplot(grid[9:12, 4:12])
    setup_panel(ax7, "Region x Channel Sales Matrix", "Heatmap of revenue concentration")
    sns.heatmap(
        region_channel_sales / 1_000_000,
        cmap=sns.light_palette(NAVY, as_cmap=True),
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        cbar=False,
        ax=ax7,
    )
    ax7.set_xlabel("")
    ax7.set_ylabel("")

    fig.savefig(SCREENSHOTS_DIR / "02-sales-analysis.png", facecolor=BG)
    plt.close(fig)


def create_profitability_analysis(metrics: dict[str, object]) -> None:
    subcategory = metrics["subcategory"]
    category = metrics["category"]
    channel = metrics["channel"]
    region = metrics["region"]
    product = metrics["product"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Profitability Analysis",
        "Revenue quality view highlighting margin conversion, discount pressure, and weak economic pockets.",
        ["Date", "Region", "Category", "Sales Channel"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.9)

    cards = [
        ("Total Profit", fmt_currency(kpis["total_profit"]), GREEN, "Contribution after cost"),
        ("Profit Margin %", fmt_pct(kpis["profit_margin"]), GREEN, "Average revenue quality"),
        ("Discount %", fmt_pct(kpis["discount_pct"]), RED, "Gross-to-net pressure"),
        ("Profit per Order", fmt_currency(kpis["profit_per_order"]), NAVY, "Efficiency by order"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Margin By Category", "High sales do not always translate into strong margin")
    cat = category.sort_values("Margin", ascending=True)
    ax1.barh(cat["Category"], cat["Margin"], color=[SLATE, GOLD, GREEN])
    label_barh(ax1, cat["Margin"], formatter=lambda value: f"{value * 100:.1f}%")
    ax1.set_xlim(0, max(cat["Margin"]) * 1.18)

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Sales Vs Profit By Sub-Category", "Bubble position reveals high volume with weak conversion")
    ax2.scatter(
        subcategory["Sales"],
        subcategory["Profit"],
        s=subcategory["DiscountPct"] * 6500,
        c=subcategory["Margin"],
        cmap=sns.blend_palette([RED, GOLD, GREEN], as_cmap=True),
        alpha=0.85,
        edgecolors="white",
        linewidth=1,
    )
    for _, row in subcategory.iterrows():
        ax2.annotate(row["Sub-Category"], (row["Sales"], row["Profit"]), fontsize=8, alpha=0.9)
    ax2.set_xlabel("Sales")
    ax2.set_ylabel("Profit")

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Discount Vs Margin", "Sub-categories with heavier discounting tend to lose margin")
    sns.scatterplot(
        data=subcategory,
        x="DiscountPct",
        y="Margin",
        hue="Category",
        size="Sales",
        palette=[NAVY, SLATE, TEAL],
        sizes=(60, 420),
        alpha=0.9,
        ax=ax3,
    )
    ax3.legend(loc="lower left", fontsize=7.5, frameon=False)
    ax3.set_xlabel("Average Discount %")
    ax3.set_ylabel("Profit Margin %")
    ax3.xaxis.set_major_formatter(lambda x, pos: f"{x * 100:.1f}%")
    ax3.yaxis.set_major_formatter(lambda y, pos: f"{y * 100:.1f}%")

    ax4 = fig.add_subplot(grid[6:12, 0:4])
    setup_panel(ax4, "Low-Margin High-Volume Products", "Products that deserve pricing or assortment review")
    low_margin = product.sort_values(["Margin", "Sales"], ascending=[True, False]).head(8)
    low_margin = low_margin.sort_values("Margin", ascending=True)
    ax4.barh(low_margin["Product Name"], low_margin["Margin"], color=RED)
    label_barh(ax4, low_margin["Margin"], formatter=lambda value: f"{value * 100:.1f}%")
    ax4.set_xlim(0, max(low_margin["Margin"]) * 1.35)

    ax5 = fig.add_subplot(grid[6:12, 4:8])
    setup_panel(ax5, "Profit By Channel", "Channel profit bars annotated with margin")
    ch = channel.sort_values("Profit", ascending=True)
    ax5.barh(ch["Sales Channel"], ch["Profit"], color=GREEN)
    label_barh(ax5, ch["Profit"])
    for i, row in enumerate(ch.itertuples(index=False)):
        ax5.text(row.Profit * 0.02, i, f"{row.Margin * 100:.1f}% margin", va="center", color="white", fontsize=8.5)

    ax6 = fig.add_subplot(grid[6:12, 8:12])
    setup_panel(ax6, "Margin By Region", "Regional margin stability")
    reg = region.sort_values("Margin", ascending=True)
    ax6.barh(reg["Region"], reg["Margin"], color=SLATE)
    label_barh(ax6, reg["Margin"], formatter=lambda value: f"{value * 100:.1f}%")
    ax6.set_xlim(0, max(reg["Margin"]) * 1.2)

    fig.savefig(SCREENSHOTS_DIR / "03-profitability-analysis.png", facecolor=BG)
    plt.close(fig)


def create_customer_product_insights(metrics: dict[str, object]) -> None:
    segment = metrics["segment"]
    segment_growth = metrics["segment_growth"]
    product = metrics["product"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Customer & Product Insights",
        "Mix view of customer segments, product concentration, and the items that truly pull performance.",
        ["Date", "Segment", "Category", "Region"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Total Customers", fmt_int(kpis["total_customers"]), NAVY, "Active customers"),
        ("Sales per Customer", fmt_currency(kpis["sales_per_customer"]), TEAL, "Average account value"),
        ("Top 10 Product Share", fmt_pct(kpis["top_10_share"]), GOLD, "Sales concentration"),
        ("Enterprise Growth", fmt_pct(kpis["enterprise_growth"]), GREEN, "2025 vs 2024"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Segment Sales And Profit", "Side-by-side contribution by segment")
    seg = segment.set_index("Segment")[["Sales", "Profit"]]
    seg.plot(kind="bar", ax=ax1, color=[NAVY, GREEN], width=0.72)
    ax1.legend(frameon=False)
    ax1.tick_params(axis="x", rotation=0)

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Segment Growth", "Year-over-year sales growth by segment")
    growth = segment_growth.sort_values("YoYGrowth", ascending=True)
    ax2.barh(growth["Segment"], growth["YoYGrowth"], color=GOLD)
    label_barh(ax2, growth["YoYGrowth"], formatter=lambda value: f"{value * 100:.1f}%")
    ax2.set_xlim(0, max(growth["YoYGrowth"]) * 1.25)

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Top Products By Sales", "Revenue leaders")
    top_sales = product.head(10).sort_values("Sales", ascending=True)
    ax3.barh(top_sales["Product Name"], top_sales["Sales"], color=NAVY)
    label_barh(ax3, top_sales["Sales"])

    ax4 = fig.add_subplot(grid[6:12, 0:6])
    setup_panel(ax4, "Top Products By Profit", "Profit leaders in the product portfolio")
    top_profit = product.sort_values("Profit", ascending=False).head(10).sort_values("Profit", ascending=True)
    ax4.barh(top_profit["Product Name"], top_profit["Profit"], color=GREEN)
    label_barh(ax4, top_profit["Profit"])

    ax5 = fig.add_subplot(grid[6:12, 6:12])
    setup_panel(ax5, "Revenue Concentration Curve", "Cumulative sales share of ranked products")
    pareto = product.head(15)
    ax5.plot(pareto["Rank"], pareto["CumulativeSalesShare"], color=NAVY, linewidth=2.5)
    ax5.scatter(pareto["Rank"], pareto["CumulativeSalesShare"], color=GOLD, s=40, zorder=3)
    ax5.axhline(0.80, color=RED, linestyle="--", linewidth=1.2)
    ax5.set_ylim(0, 1.0)
    ax5.set_xlabel("Product Rank")
    ax5.set_ylabel("Cumulative Sales Share")
    ax5.yaxis.set_major_formatter(lambda value, pos: f"{value * 100:.0f}%")

    fig.savefig(SCREENSHOTS_DIR / "04-customer-product-insights.png", facecolor=BG)
    plt.close(fig)


def create_geography_channel_performance(metrics: dict[str, object]) -> None:
    region = metrics["region"]
    channel = metrics["channel"]
    region_channel_sales = metrics["region_channel_sales"]
    region_channel_margin = metrics["region_channel_margin"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Geography & Channel Performance",
        "Comparison of regional scale, margin efficiency, and channel execution quality.",
        ["Date", "Region", "Sales Channel", "Segment"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Total Sales", fmt_currency(kpis["total_sales"]), NAVY, "Portfolio scale"),
        ("Total Profit", fmt_currency(kpis["total_profit"]), GREEN, "Profit contribution"),
        ("Profit Margin %", fmt_pct(kpis["profit_margin"]), GREEN, "Revenue quality"),
        ("Profit per Order", fmt_currency(kpis["profit_per_order"]), GOLD, "Efficiency"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Sales By Region", "Revenue leaders")
    reg_sales = region.sort_values("Sales", ascending=True)
    ax1.barh(reg_sales["Region"], reg_sales["Sales"], color=NAVY)
    label_barh(ax1, reg_sales["Sales"])

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Profit Margin By Region", "Regional efficiency")
    reg_margin = region.sort_values("Margin", ascending=True)
    ax2.barh(reg_margin["Region"], reg_margin["Margin"], color=GREEN)
    label_barh(ax2, reg_margin["Margin"], formatter=lambda value: f"{value * 100:.1f}%")
    ax2.set_xlim(0, max(reg_margin["Margin"]) * 1.2)

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Channel Contribution", "Sales share by channel")
    ch_share = channel.sort_values("SalesShare", ascending=True)
    ax3.barh(ch_share["Sales Channel"], ch_share["SalesShare"], color=GOLD)
    label_barh(ax3, ch_share["SalesShare"], formatter=lambda value: f"{value * 100:.1f}%")
    ax3.set_xlim(0, max(ch_share["SalesShare"]) * 1.2)

    ax4 = fig.add_subplot(grid[6:9, 0:6])
    setup_panel(ax4, "Region x Channel Sales", "Revenue concentration by operating mix")
    sns.heatmap(
        region_channel_sales / 1_000_000,
        cmap=sns.light_palette(NAVY, as_cmap=True),
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        cbar=False,
        ax=ax4,
    )
    ax4.set_xlabel("")
    ax4.set_ylabel("")

    ax5 = fig.add_subplot(grid[6:9, 6:12])
    setup_panel(ax5, "Region x Channel Margin", "Margin stability by territory and route-to-market")
    sns.heatmap(
        region_channel_margin,
        cmap=sns.light_palette(GREEN, as_cmap=True),
        annot=True,
        fmt=".1%",
        linewidths=0.5,
        cbar=False,
        ax=ax5,
    )
    ax5.set_xlabel("")
    ax5.set_ylabel("")

    ax6 = fig.add_subplot(grid[9:12, 0:12])
    setup_panel(ax6, "Profit Per Order By Channel", "Channel efficiency without relying only on total volume")
    ch_eff = channel.sort_values("ProfitPerOrder", ascending=True)
    ax6.barh(ch_eff["Sales Channel"], ch_eff["ProfitPerOrder"], color=[SLATE, GOLD, NAVY, GREEN])
    label_barh(ax6, ch_eff["ProfitPerOrder"])

    fig.savefig(SCREENSHOTS_DIR / "05-geography-channel-performance.png", facecolor=BG)
    plt.close(fig)


def create_targets_trends(metrics: dict[str, object]) -> None:
    monthly = metrics["monthly"]
    region_attainment = metrics["region_attainment"]
    channel_attainment = metrics["channel_attainment"]
    monthly_region_2025 = metrics["monthly_region_2025"]
    kpis = metrics["kpis"]

    fig = plt.figure(figsize=(19.2, 10.8), dpi=110)
    fig.patch.set_facecolor(BG)
    add_page_header(
        fig,
        "Targets & Trends",
        "Managerial performance view focused on plan attainment, variance control, and momentum.",
        ["Date", "Region", "Sales Channel"],
    )
    grid = fig.add_gridspec(12, 15, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.9)

    cards = [
        ("Sales Target", fmt_currency(kpis["sales_target"]), SLATE, "Planned revenue"),
        ("Target Attainment %", fmt_pct(kpis["target_attainment"]), GOLD, "Actual vs plan"),
        ("Variance", fmt_currency(kpis["target_variance"]), RED if kpis["target_variance"] < 0 else GREEN, "Sales - target"),
        ("Sales YoY %", fmt_pct(kpis["sales_yoy"]), NAVY, "2025 vs 2024"),
        ("Profit YoY %", fmt_pct(kpis["profit_yoy"]), GREEN, "2025 vs 2024"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:8])
    setup_panel(ax1, "Actual Vs Target By Month", "Monthly actual sales against the target curve")
    ax1.plot(monthly["MonthStart"], monthly["SalesTarget"], color=SLATE, linewidth=2.0, linestyle="--", label="Target")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.6, label="Actual")
    ax1.fill_between(monthly["MonthStart"], monthly["SalesTarget"], monthly["Sales"], color=NAVY, alpha=0.10)
    format_month_axis(ax1)
    ax1.legend(loc="upper left", frameon=False)

    ax2 = fig.add_subplot(grid[2:6, 8:15])
    setup_panel(ax2, "Monthly Variance", "Positive and negative plan gaps")
    variance_colors = [GREEN if value >= 0 else RED for value in monthly["Variance"]]
    ax2.bar(monthly["MonthStart"], monthly["Variance"], color=variance_colors, width=20)
    ax2.axhline(0, color=BORDER, linewidth=1)
    format_month_axis(ax2)

    ax3 = fig.add_subplot(grid[6:9, 0:5])
    setup_panel(ax3, "Target Attainment By Region", "Regions above and below plan")
    reg = region_attainment.sort_values("Attainment", ascending=True)
    colors = [GREEN if value >= 1 else RED for value in reg["Attainment"]]
    ax3.barh(reg["Region"], reg["Attainment"], color=colors)
    label_barh(ax3, reg["Attainment"], formatter=lambda value: f"{value * 100:.1f}%")
    ax3.set_xlim(0, max(reg["Attainment"]) * 1.2)

    ax4 = fig.add_subplot(grid[6:9, 5:10])
    setup_panel(ax4, "Target Attainment By Channel", "Commercial execution by route-to-market")
    ch = channel_attainment.sort_values("Attainment", ascending=True)
    colors = [GREEN if value >= 1 else RED for value in ch["Attainment"]]
    ax4.barh(ch["Sales Channel"], ch["Attainment"], color=colors)
    label_barh(ax4, ch["Attainment"], formatter=lambda value: f"{value * 100:.1f}%")
    ax4.set_xlim(0, max(ch["Attainment"]) * 1.2)

    ax5 = fig.add_subplot(grid[6:9, 10:15])
    setup_panel(ax5, "MoM And YoY Momentum", "Acceleration and slowdown in the monthly cycle")
    ax5.plot(monthly["MonthStart"], monthly["SalesYoY"], color=NAVY, linewidth=2.1, label="Sales YoY %")
    ax5.plot(monthly["MonthStart"], monthly["ProfitYoY"], color=GREEN, linewidth=2.1, label="Profit YoY %")
    ax5.axhline(0, color=BORDER, linewidth=1)
    ax5.yaxis.set_major_formatter(lambda value, pos: f"{value * 100:.0f}%")
    format_month_axis(ax5)
    ax5.legend(loc="upper left", frameon=False)

    ax6 = fig.add_subplot(grid[9:12, 0:15])
    setup_panel(ax6, "2025 Monthly Sales Heatmap By Region", "Consistency view across the latest year")
    sns.heatmap(
        monthly_region_2025 / 1_000,
        cmap=sns.light_palette(NAVY, as_cmap=True),
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar=False,
        ax=ax6,
    )
    ax6.set_xlabel("")
    ax6.set_ylabel("")
    ax6.set_xticklabels([pd.to_datetime(label.get_text()).strftime("%b") for label in ax6.get_xticklabels()], rotation=0)

    fig.savefig(SCREENSHOTS_DIR / "06-targets-trends.png", facecolor=BG)
    plt.close(fig)


def main() -> None:
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    style_page()
    sales, targets = load_data()
    metrics = build_metrics(sales, targets)

    create_executive_overview(metrics)
    create_sales_analysis(metrics)
    create_profitability_analysis(metrics)
    create_customer_product_insights(metrics)
    create_geography_channel_performance(metrics)
    create_targets_trends(metrics)
    print("Generated six dashboard preview images in the screenshots folder.")


if __name__ == "__main__":
    main()
