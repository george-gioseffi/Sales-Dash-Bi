from __future__ import annotations

from build_star_schema import build_star_schema
from build_targets_table import build_targets
from generate_sales_dataset import generate_sales_transactions


def main() -> None:
    sales = generate_sales_transactions()
    targets = build_targets()
    build_star_schema()
    print(
        "Project build complete: "
        f"{len(sales):,} sales lines and {len(targets):,} target rows generated."
    )


if __name__ == "__main__":
    main()
