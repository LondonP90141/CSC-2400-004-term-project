# Reads the CSV file and turns each row into a Product object.

import csv
from pathlib import Path
from models import Product


def load_products(csv_path: str | Path) -> list[Product]:
    products = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Convert fields into correct data types
            products.append(
                Product(
                    id=int(row["id"]),
                    category=row["category"],
                    price=float(row["price"]),
                    utility=int(row["utility"])
                )
            )

    return products