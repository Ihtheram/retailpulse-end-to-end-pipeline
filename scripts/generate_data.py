"""
generate_data.py
Generates synthetic retail CSV data for the RetailPulse pipeline.

Output files (written to data/sample/):
  - customers.csv  (~50K rows)
  - products.csv   (~5K rows)
  - orders.csv     (~500K rows)

Usage:
  python scripts/generate_data.py
"""

import os
import random
import csv
from datetime import datetime, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
NUM_CUSTOMERS = 50_000
NUM_PRODUCTS  = 5_000
NUM_ORDERS    = 500_000
OUTPUT_DIR    = os.path.join(os.path.dirname(__file__), "..", "data", "sample")

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
    "Linda", "William", "Barbara", "David", "Elizabeth", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Liam",
    "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Sophia", "Lucas",
    "Isabella", "Mason", "Mia", "Ethan", "Charlotte", "Aiden", "Amelia",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
]

CITIES = [
    ("New York", "US"), ("Los Angeles", "US"), ("Chicago", "US"),
    ("Houston", "US"), ("Phoenix", "US"), ("Philadelphia", "US"),
    ("London", "GB"), ("Manchester", "GB"), ("Birmingham", "GB"),
    ("Toronto", "CA"), ("Vancouver", "CA"), ("Montreal", "CA"),
    ("Sydney", "AU"), ("Melbourne", "AU"), ("Brisbane", "AU"),
    ("Berlin", "DE"), ("Munich", "DE"), ("Hamburg", "DE"),
    ("Paris", "FR"), ("Lyon", "FR"), ("Marseille", "FR"),
    ("Tokyo", "JP"), ("Osaka", "JP"), ("Kyoto", "JP"),
    ("Mumbai", "IN"), ("Delhi", "IN"), ("Bangalore", "IN"),
]

PRODUCT_CATEGORIES = {
    "Electronics":   ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch",
                      "Keyboard", "Monitor", "Webcam", "Speaker", "Charger"],
    "Clothing":      ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress",
                      "Hoodie", "Shorts", "Boots", "Socks", "Hat"],
    "Home & Kitchen":["Coffee Maker", "Blender", "Toaster", "Vacuum", "Lamp",
                      "Pillow", "Blanket", "Cookware Set", "Air Fryer", "Knife Set"],
    "Books":         ["Fiction Novel", "Self-Help Book", "Cookbook", "History Book",
                      "Science Book", "Biography", "Children's Book", "Textbook",
                      "Travel Guide", "Art Book"],
    "Sports":        ["Yoga Mat", "Dumbbells", "Running Shoes", "Water Bottle",
                      "Resistance Bands", "Bicycle Helmet", "Tennis Racket",
                      "Basketball", "Swim Goggles", "Camping Tent"],
    "Beauty":        ["Moisturizer", "Shampoo", "Conditioner", "Lip Balm",
                      "Sunscreen", "Face Mask", "Perfume", "Nail Polish",
                      "Eye Cream", "Body Lotion"],
}

PRICE_RANGES = {
    "Electronics":    (49.99,  1999.99),
    "Clothing":       (9.99,   299.99),
    "Home & Kitchen": (14.99,  499.99),
    "Books":          (4.99,   79.99),
    "Sports":         (9.99,   399.99),
    "Beauty":         (4.99,   149.99),
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def random_date(start_year: int = 2020, end_year: int = 2024) -> str:
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")


def round2(value: float) -> float:
    return round(value, 2)


# ── Generators ────────────────────────────────────────────────────────────────
def generate_customers(n: int) -> list[dict]:
    print(f"  Generating {n:,} customers …")
    customers = []
    for i in range(1, n + 1):
        city, country = random.choice(CITIES)
        customers.append({
            "customer_id":  i,
            "name":         f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "city":         city,
            "country":      country,
            "signup_date":  random_date(2018, 2023),
        })
    return customers


def generate_products(n: int) -> list[dict]:
    print(f"  Generating {n:,} products …")
    products = []
    categories = list(PRODUCT_CATEGORIES.keys())
    for i in range(1, n + 1):
        category = random.choice(categories)
        name     = random.choice(PRODUCT_CATEGORIES[category])
        lo, hi   = PRICE_RANGES[category]
        products.append({
            "product_id": i,
            "name":       f"{name} {random.randint(1, 999):03d}",
            "category":   category,
            "price":      round2(random.uniform(lo, hi)),
            "stock_qty":  random.randint(0, 5000),
        })
    return products


def generate_orders(n: int, num_customers: int, num_products: int,
                    products: list[dict]) -> list[dict]:
    print(f"  Generating {n:,} orders …")
    # Build a quick price lookup
    price_map = {p["product_id"]: p["price"] for p in products}
    orders = []
    for i in range(1, n + 1):
        product_id  = random.randint(1, num_products)
        unit_price  = price_map[product_id]
        quantity    = random.randint(1, 10)
        orders.append({
            "order_id":    i,
            "customer_id": random.randint(1, num_customers),
            "product_id":  product_id,
            "quantity":    quantity,
            "amount":      round2(unit_price * quantity),
            "order_date":  random_date(2020, 2024),
            "status":      random.choice(["completed", "completed", "completed",
                                          "returned", "pending"]),
        })
    return orders


# ── Writers ───────────────────────────────────────────────────────────────────
def write_csv(rows: list[dict], filepath: str) -> None:
    if not rows:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  ✅ Written → {filepath}  ({len(rows):,} rows, {size_mb:.1f} MB)")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    print("\n🛒 RetailPulse — Synthetic Data Generator")
    print("=" * 50)

    random.seed(42)   # reproducible output

    customers = generate_customers(NUM_CUSTOMERS)
    products  = generate_products(NUM_PRODUCTS)
    orders    = generate_orders(NUM_ORDERS, NUM_CUSTOMERS, NUM_PRODUCTS, products)

    print("\nWriting CSV files …")
    write_csv(customers, os.path.join(OUTPUT_DIR, "customers.csv"))
    write_csv(products,  os.path.join(OUTPUT_DIR, "products.csv"))
    write_csv(orders,    os.path.join(OUTPUT_DIR, "orders.csv"))

    print("\n✅ All done! Files are in:", os.path.abspath(OUTPUT_DIR))
    print("Next step: upload to S3 with:")
    print(f"  aws s3 cp data/sample/ s3://<your-bucket>/raw/retail/ --recursive\n")


if __name__ == "__main__":
    main()