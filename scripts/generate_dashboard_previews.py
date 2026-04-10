from __future__ import annotations

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

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

MONTH_ABBR_PT = {
    1: "jan",
    2: "fev",
    3: "mar",
    4: "abr",
    5: "mai",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "set",
    10: "out",
    11: "nov",
    12: "dez",
}

REGION_PT = {
    "Southeast": "Sudeste",
    "South": "Sul",
    "Northeast": "Nordeste",
    "Midwest": "Centro-Oeste",
    "North": "Norte",
}

CHANNEL_PT = {
    "Direct Sales": "Vendas Diretas",
    "Distributors": "Distribuidores",
    "Online": "Online",
    "Retail Stores": "Lojas Físicas",
}

SEGMENT_PT = {
    "Consumer": "Consumidor",
    "Small Business": "Pequenas Empresas",
    "Enterprise": "Empresas",
}

CATEGORY_PT = {
    "Furniture": "Móveis",
    "Office Supplies": "Suprimentos de Escritório",
    "Technology": "Tecnologia",
}

SUBCATEGORY_PT = {
    "Accessories": "Acessórios",
    "Binders": "Fichários",
    "Chairs": "Cadeiras",
    "Desks": "Escrivaninhas",
    "Filing": "Arquivo",
    "Labels": "Etiquetas",
    "Laptops": "Laptops",
    "Monitors": "Monitores",
    "Paper": "Papel",
    "Printers": "Impressoras",
    "Storage": "Armazenamento",
    "Tables": "Mesas",
    "Writing": "Escrita",
}


def fmt_currency(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f}M".replace(".", ",")
    if abs_value >= 1_000:
        return f"R$ {value / 1_000:.1f} mil".replace(".", ",")
    return f"R$ {value:,.0f}".replace(",", ".")


def fmt_pct(value: float) -> str:
    return f"{value * 100:.1f}%".replace(".", ",")


def fmt_int(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(
        RAW_DIR / "sales_transactions.csv",
        parse_dates=["Order Date", "Ship Date"],
    )
    targets = pd.read_csv(
        RAW_DIR / "monthly_targets.csv",
        parse_dates=["Target Month"],
    )

    sales["Region"] = sales["Region"].replace(REGION_PT)
    sales["Sales Channel"] = sales["Sales Channel"].replace(CHANNEL_PT)
    sales["Segment"] = sales["Segment"].replace(SEGMENT_PT)
    sales["Category"] = sales["Category"].replace(CATEGORY_PT)
    sales["Sub-Category"] = sales["Sub-Category"].replace(SUBCATEGORY_PT)

    targets["Region"] = targets["Region"].replace(REGION_PT)
    targets["Sales Channel"] = targets["Sales Channel"].replace(CHANNEL_PT)

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
            segment_growth.loc[segment_growth["Segment"] == SEGMENT_PT["Enterprise"], "YoYGrowth"].iloc[0]
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
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda value, pos: f"{MONTH_ABBR_PT[mdates.num2date(value).month]} {str(mdates.num2date(value).year)[2:]}")
    )
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
        "Visão Executiva",
        "Leitura executiva do tamanho da receita, qualidade da margem, entrega contra meta e principais drivers de crescimento.",
        ["Data", "Região", "Canal de Vendas", "Categoria"],
    )
    grid = fig.add_gridspec(12, 14, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Vendas Totais", fmt_currency(kpis["total_sales"]), NAVY, "Receita líquida"),
        ("Lucro Total", fmt_currency(kpis["total_profit"]), GREEN, "Contribuição após custo"),
        ("Margem de Lucro %", fmt_pct(kpis["profit_margin"]), GREEN, "Qualidade da receita"),
        ("Pedidos Totais", fmt_int(kpis["total_orders"]), SLATE, "Pedidos distintos"),
        ("Ticket Médio", fmt_currency(kpis["aov"]), NAVY, "Valor médio por pedido"),
        ("Taxa de Devolução %", fmt_pct(kpis["return_rate"]), RED, "Linhas devolvidas"),
        ("Atingimento de Meta %", fmt_pct(kpis["target_attainment"]), GOLD, "Realizado vs plano"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 2 : idx * 2 + 2]), *card)

    ax1 = fig.add_subplot(grid[2:7, 0:8])
    setup_panel(ax1, "Tendência Mensal de Vendas e Lucro", "Direção de vendas e lucro ao longo dos 24 meses")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.7, label="Vendas")
    ax1.fill_between(monthly["MonthStart"], monthly["Sales"], color=NAVY, alpha=0.10)
    ax1.set_ylabel("Vendas")
    format_month_axis(ax1)
    ax1b = ax1.twinx()
    ax1b.plot(monthly["MonthStart"], monthly["Profit"], color=GREEN, linewidth=2.1, label="Lucro")
    ax1b.set_ylabel("Lucro")
    ax1.legend(loc="upper left", frameon=False)
    ax1b.legend(loc="upper right", frameon=False)

    ax2 = fig.add_subplot(grid[2:7, 8:14])
    setup_panel(ax2, "Vendas Realizadas vs Meta", "Realizado mensal comparado ao plano")
    ax2.plot(monthly["MonthStart"], monthly["SalesTarget"], color=SLATE, linewidth=2.0, linestyle="--", label="Meta")
    ax2.plot(monthly["MonthStart"], monthly["Sales"], color=GOLD, linewidth=2.5, label="Realizado")
    ax2.fill_between(monthly["MonthStart"], monthly["SalesTarget"], monthly["Sales"], color=GOLD, alpha=0.12)
    format_month_axis(ax2)
    ax2.legend(loc="upper left", frameon=False)

    ax3 = fig.add_subplot(grid[7:12, 0:7])
    setup_panel(ax3, "Top Regiões por Vendas", "Líderes de receita com contexto de margem")
    region_plot = region.sort_values("Sales", ascending=True)
    ax3.barh(region_plot["Region"], region_plot["Sales"], color=NAVY, alpha=0.92)
    label_barh(ax3, region_plot["Sales"])
    ax3.set_xlabel("Vendas")
    for i, row in enumerate(region_plot.itertuples(index=False)):
        ax3.text(row.Sales * 0.02, i, f"Margem {str(round(row.Margin * 100, 1)).replace('.', ',')}%", va="center", color="white", fontsize=8.5)

    ax4 = fig.add_subplot(grid[7:12, 7:14])
    setup_panel(ax4, "Contribuição por Categoria", "Participação de vendas e lucratividade por categoria")
    category_plot = category.sort_values("Sales", ascending=True)
    colors = [NAVY, SLATE, TEAL]
    ax4.barh(category_plot["Category"], category_plot["Sales"], color=colors)
    label_barh(ax4, category_plot["Sales"])
    for i, row in enumerate(category_plot.itertuples(index=False)):
        ax4.text(row.Sales * 0.64, i, f"{str(round(row.Margin * 100, 1)).replace('.', ',')}% de margem", va="center", color="white", fontsize=9)

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
        "Análise de Vendas",
        "Leitura dos drivers de receita ao longo do tempo, do mix de categorias, da escala regional e da contribuição por canal.",
        ["Data", "Região", "Canal de Vendas", "Segmento"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Vendas Totais", fmt_currency(kpis["total_sales"]), NAVY, "Receita líquida"),
        ("Pedidos Totais", fmt_int(kpis["total_orders"]), SLATE, "Pedidos distintos"),
        ("Ticket Médio", fmt_currency(kpis["aov"]), GOLD, "Tamanho do ticket"),
        ("Quantidade Total", fmt_int(monthly["Quantity"].sum()), TEAL, "Unidades vendidas"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:6])
    setup_panel(ax1, "Vendas ao Longo do Tempo", "Tendência mensal de vendas")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.6)
    ax1.fill_between(monthly["MonthStart"], monthly["Sales"], color=NAVY, alpha=0.12)
    format_month_axis(ax1)

    ax2 = fig.add_subplot(grid[2:6, 6:12])
    setup_panel(ax2, "Mix de Vendas por Canal ao Longo do Tempo", "Contribuição mensal dos canais")
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
    setup_panel(ax3, "Vendas por Categoria", "Mix de receita em nível principal")
    cat = category.sort_values("Sales", ascending=True)
    ax3.barh(cat["Category"], cat["Sales"], color=[TEAL, SLATE, NAVY])
    label_barh(ax3, cat["Sales"])

    ax4 = fig.add_subplot(grid[6:9, 4:8])
    setup_panel(ax4, "Top Subcategorias por Vendas", "Maiores bolsões de receita")
    sub = subcategory.head(8).sort_values("Sales", ascending=True)
    ax4.barh(sub["Sub-Category"], sub["Sales"], color=NAVY)
    label_barh(ax4, sub["Sales"])

    ax5 = fig.add_subplot(grid[6:9, 8:12])
    setup_panel(ax5, "Vendas por Região", "Escala regional de receita")
    reg = region.sort_values("Sales", ascending=True)
    ax5.barh(reg["Region"], reg["Sales"], color=SLATE)
    label_barh(ax5, reg["Sales"])

    ax6 = fig.add_subplot(grid[9:12, 0:4])
    setup_panel(ax6, "Vendas por Canal", "Mix por canal")
    ch = channel.sort_values("Sales", ascending=True)
    ax6.barh(ch["Sales Channel"], ch["Sales"], color=GOLD)
    label_barh(ax6, ch["Sales"])

    ax7 = fig.add_subplot(grid[9:12, 4:12])
    setup_panel(ax7, "Matrix Região x Canal de Vendas", "Heatmap de concentração de receita")
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
        "Análise de Lucratividade",
        "Leitura da qualidade da receita com foco em conversão de margem, pressão de desconto e bolsões econômicos fracos.",
        ["Data", "Região", "Categoria", "Canal de Vendas"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.9)

    cards = [
        ("Lucro Total", fmt_currency(kpis["total_profit"]), GREEN, "Contribuição após custo"),
        ("Margem de Lucro %", fmt_pct(kpis["profit_margin"]), GREEN, "Qualidade média da receita"),
        ("Desconto %", fmt_pct(kpis["discount_pct"]), RED, "Pressão de bruto para líquido"),
        ("Lucro por Pedido", fmt_currency(kpis["profit_per_order"]), NAVY, "Eficiência por pedido"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Margem por Categoria", "Vender muito nem sempre significa margem forte")
    cat = category.sort_values("Margin", ascending=True)
    ax1.barh(cat["Category"], cat["Margin"], color=[SLATE, GOLD, GREEN])
    label_barh(ax1, cat["Margin"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax1.set_xlim(0, max(cat["Margin"]) * 1.18)

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Sales vs Profit por Subcategoria", "A posição das bolhas revela alto volume com conversão fraca")
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
    ax2.set_xlabel("Vendas")
    ax2.set_ylabel("Lucro")

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Desconto vs Margem", "Subcategorias com desconto mais alto tendem a perder margem")
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
    ax3.set_xlabel("Desconto Médio %")
    ax3.set_ylabel("Margem de Lucro %")
    ax3.xaxis.set_major_formatter(lambda x, pos: f"{x * 100:.1f}%".replace(".", ","))
    ax3.yaxis.set_major_formatter(lambda y, pos: f"{y * 100:.1f}%".replace(".", ","))

    ax4 = fig.add_subplot(grid[6:12, 0:4])
    setup_panel(ax4, "Produtos de Alta Venda e Baixa Margem", "Produtos que merecem revisão de preço ou sortimento")
    low_margin = product.sort_values(["Margin", "Sales"], ascending=[True, False]).head(8)
    low_margin = low_margin.sort_values("Margin", ascending=True)
    ax4.barh(low_margin["Product Name"], low_margin["Margin"], color=RED)
    label_barh(ax4, low_margin["Margin"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax4.set_xlim(0, max(low_margin["Margin"]) * 1.35)

    ax5 = fig.add_subplot(grid[6:12, 4:8])
    setup_panel(ax5, "Lucro por Canal", "Barras de lucro por canal com anotação de margem")
    ch = channel.sort_values("Profit", ascending=True)
    ax5.barh(ch["Sales Channel"], ch["Profit"], color=GREEN)
    label_barh(ax5, ch["Profit"])
    for i, row in enumerate(ch.itertuples(index=False)):
        ax5.text(row.Profit * 0.02, i, f"{str(round(row.Margin * 100, 1)).replace('.', ',')}% de margem", va="center", color="white", fontsize=8.5)

    ax6 = fig.add_subplot(grid[6:12, 8:12])
    setup_panel(ax6, "Margem por Região", "Estabilidade regional de margem")
    reg = region.sort_values("Margin", ascending=True)
    ax6.barh(reg["Region"], reg["Margin"], color=SLATE)
    label_barh(ax6, reg["Margin"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
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
        "Insights de Clientes e Produtos",
        "Leitura do mix de segmentos, da concentração do portfólio e dos itens que realmente puxam performance.",
        ["Data", "Segmento", "Categoria", "Região"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Clientes Totais", fmt_int(kpis["total_customers"]), NAVY, "Clientes ativos"),
        ("Vendas por Cliente", fmt_currency(kpis["sales_per_customer"]), TEAL, "Valor médio por conta"),
        ("Participação do Top 10", fmt_pct(kpis["top_10_share"]), GOLD, "Concentração de vendas"),
        ("Crescimento Empresas", fmt_pct(kpis["enterprise_growth"]), GREEN, "2025 vs 2024"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Vendas e Lucro por Segmento", "Contribuição lado a lado por segmento")
    seg = segment.set_index("Segment")[["Sales", "Profit"]]
    seg.plot(kind="bar", ax=ax1, color=[NAVY, GREEN], width=0.72)
    ax1.legend(frameon=False)
    ax1.tick_params(axis="x", rotation=0)

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Crescimento por Segmento", "Crescimento de vendas ano contra ano por segmento")
    growth = segment_growth.sort_values("YoYGrowth", ascending=True)
    ax2.barh(growth["Segment"], growth["YoYGrowth"], color=GOLD)
    label_barh(ax2, growth["YoYGrowth"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax2.set_xlim(0, max(growth["YoYGrowth"]) * 1.25)

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Top Produtos por Vendas", "Líderes de receita")
    top_sales = product.head(10).sort_values("Sales", ascending=True)
    ax3.barh(top_sales["Product Name"], top_sales["Sales"], color=NAVY)
    label_barh(ax3, top_sales["Sales"])

    ax4 = fig.add_subplot(grid[6:12, 0:6])
    setup_panel(ax4, "Top Produtos por Lucro", "Líderes de lucro no portfólio")
    top_profit = product.sort_values("Profit", ascending=False).head(10).sort_values("Profit", ascending=True)
    ax4.barh(top_profit["Product Name"], top_profit["Profit"], color=GREEN)
    label_barh(ax4, top_profit["Profit"])

    ax5 = fig.add_subplot(grid[6:12, 6:12])
    setup_panel(ax5, "Curva de Concentração de Receita", "Participação acumulada das vendas por ranking de produto")
    pareto = product.head(15)
    ax5.plot(pareto["Rank"], pareto["CumulativeSalesShare"], color=NAVY, linewidth=2.5)
    ax5.scatter(pareto["Rank"], pareto["CumulativeSalesShare"], color=GOLD, s=40, zorder=3)
    ax5.axhline(0.80, color=RED, linestyle="--", linewidth=1.2)
    ax5.set_ylim(0, 1.0)
    ax5.set_xlabel("Ranking do Produto")
    ax5.set_ylabel("Participação Acumulada das Vendas")
    ax5.yaxis.set_major_formatter(lambda value, pos: f"{value * 100:.0f}%".replace(".", ","))

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
        "Performance Geográfica e de Canais",
        "Comparação entre escala regional, eficiência de margem e qualidade de execução por canal.",
        ["Data", "Região", "Canal de Vendas", "Segmento"],
    )
    grid = fig.add_gridspec(12, 12, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.8)

    cards = [
        ("Vendas Totais", fmt_currency(kpis["total_sales"]), NAVY, "Escala do portfólio"),
        ("Lucro Total", fmt_currency(kpis["total_profit"]), GREEN, "Contribuição de lucro"),
        ("Margem de Lucro %", fmt_pct(kpis["profit_margin"]), GREEN, "Qualidade da receita"),
        ("Lucro por Pedido", fmt_currency(kpis["profit_per_order"]), GOLD, "Eficiência"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:4])
    setup_panel(ax1, "Vendas por Região", "Regiões líderes em receita")
    reg_sales = region.sort_values("Sales", ascending=True)
    ax1.barh(reg_sales["Region"], reg_sales["Sales"], color=NAVY)
    label_barh(ax1, reg_sales["Sales"])

    ax2 = fig.add_subplot(grid[2:6, 4:8])
    setup_panel(ax2, "Margem por Região", "Eficiência regional")
    reg_margin = region.sort_values("Margin", ascending=True)
    ax2.barh(reg_margin["Region"], reg_margin["Margin"], color=GREEN)
    label_barh(ax2, reg_margin["Margin"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax2.set_xlim(0, max(reg_margin["Margin"]) * 1.2)

    ax3 = fig.add_subplot(grid[2:6, 8:12])
    setup_panel(ax3, "Contribuição por Canal", "Participação das vendas por canal")
    ch_share = channel.sort_values("SalesShare", ascending=True)
    ax3.barh(ch_share["Sales Channel"], ch_share["SalesShare"], color=GOLD)
    label_barh(ax3, ch_share["SalesShare"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax3.set_xlim(0, max(ch_share["SalesShare"]) * 1.2)

    ax4 = fig.add_subplot(grid[6:9, 0:6])
    setup_panel(ax4, "Vendas por Região x Canal", "Concentração de receita por mix operacional")
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
    setup_panel(ax5, "Margem por Região x Canal", "Estabilidade de margem por território e rota ao mercado")
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
    setup_panel(ax6, "Lucro por Pedido por Canal", "Eficiência do canal sem depender só de volume total")
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
        "Metas e Tendências",
        "Leitura gerencial focada em atingimento do plano, controle de variância e momento do negócio.",
        ["Data", "Região", "Canal de Vendas"],
    )
    grid = fig.add_gridspec(12, 15, left=0.03, right=0.97, top=0.90, bottom=0.05, hspace=1.0, wspace=0.9)

    cards = [
        ("Meta de Vendas", fmt_currency(kpis["sales_target"]), SLATE, "Receita planejada"),
        ("Atingimento de Meta %", fmt_pct(kpis["target_attainment"]), GOLD, "Realizado vs plano"),
        ("Variância", fmt_currency(kpis["target_variance"]), RED if kpis["target_variance"] < 0 else GREEN, "Vendas - meta"),
        ("Vendas YoY %", fmt_pct(kpis["sales_yoy"]), NAVY, "2025 vs 2024"),
        ("Lucro YoY %", fmt_pct(kpis["profit_yoy"]), GREEN, "2025 vs 2024"),
    ]
    for idx, card in enumerate(cards):
        add_card(fig.add_subplot(grid[0:2, idx * 3 : idx * 3 + 3]), *card)

    ax1 = fig.add_subplot(grid[2:6, 0:8])
    setup_panel(ax1, "Realizado vs Meta por Mês", "Vendas realizadas por mês contra a curva de meta")
    ax1.plot(monthly["MonthStart"], monthly["SalesTarget"], color=SLATE, linewidth=2.0, linestyle="--", label="Meta")
    ax1.plot(monthly["MonthStart"], monthly["Sales"], color=NAVY, linewidth=2.6, label="Realizado")
    ax1.fill_between(monthly["MonthStart"], monthly["SalesTarget"], monthly["Sales"], color=NAVY, alpha=0.10)
    format_month_axis(ax1)
    ax1.legend(loc="upper left", frameon=False)

    ax2 = fig.add_subplot(grid[2:6, 8:15])
    setup_panel(ax2, "Variância Mensal", "Desvios positivos e negativos contra o plano")
    variance_colors = [GREEN if value >= 0 else RED for value in monthly["Variance"]]
    ax2.bar(monthly["MonthStart"], monthly["Variance"], color=variance_colors, width=20)
    ax2.axhline(0, color=BORDER, linewidth=1)
    format_month_axis(ax2)

    ax3 = fig.add_subplot(grid[6:9, 0:5])
    setup_panel(ax3, "Atingimento de Meta por Região", "Regiões acima e abaixo do plano")
    reg = region_attainment.sort_values("Attainment", ascending=True)
    colors = [GREEN if value >= 1 else RED for value in reg["Attainment"]]
    ax3.barh(reg["Region"], reg["Attainment"], color=colors)
    label_barh(ax3, reg["Attainment"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax3.set_xlim(0, max(reg["Attainment"]) * 1.2)

    ax4 = fig.add_subplot(grid[6:9, 5:10])
    setup_panel(ax4, "Atingimento de Meta por Canal", "Execução comercial por rota ao mercado")
    ch = channel_attainment.sort_values("Attainment", ascending=True)
    colors = [GREEN if value >= 1 else RED for value in ch["Attainment"]]
    ax4.barh(ch["Sales Channel"], ch["Attainment"], color=colors)
    label_barh(ax4, ch["Attainment"], formatter=lambda value: f"{value * 100:.1f}%".replace(".", ","))
    ax4.set_xlim(0, max(ch["Attainment"]) * 1.2)

    ax5 = fig.add_subplot(grid[6:9, 10:15])
    setup_panel(ax5, "Momento MoM e YoY", "Aceleração e desaceleração no ciclo mensal")
    ax5.plot(monthly["MonthStart"], monthly["SalesYoY"], color=NAVY, linewidth=2.1, label="Vendas YoY %")
    ax5.plot(monthly["MonthStart"], monthly["ProfitYoY"], color=GREEN, linewidth=2.1, label="Lucro YoY %")
    ax5.axhline(0, color=BORDER, linewidth=1)
    ax5.yaxis.set_major_formatter(lambda value, pos: f"{value * 100:.0f}%".replace(".", ","))
    format_month_axis(ax5)
    ax5.legend(loc="upper left", frameon=False)

    ax6 = fig.add_subplot(grid[9:12, 0:15])
    setup_panel(ax6, "Heatmap de Vendas Mensais de 2025 por Região", "Visão de consistência ao longo do último ano")
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
    ax6.set_xticklabels(
        [MONTH_ABBR_PT[pd.to_datetime(label.get_text()).month] for label in ax6.get_xticklabels()],
        rotation=0,
    )

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
    print("Seis imagens de preview do dashboard foram geradas na pasta screenshots.")


if __name__ == "__main__":
    main()
