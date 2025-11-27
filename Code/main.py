# Lets the user pick algorithm + dataset size, then runs and times it.

from pathlib import Path
import time
from data_loader import load_products
from algorithms import knapsack_bruteforce, knapsack_dp


def choose_algorithm():
    # Simple text menu for algorithm choice
    print("Choose algorithm:")
    print("1) Brute force")
    print("2) Dynamic programming")
    print("3) Both")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        return "brute"
    elif choice == "2":
        return "dp"
    else:
        return "both"


def choose_dataset_size():
    # Simple text menu for dataset size
    print("\nChoose dataset size:")
    print("1) Tiny")
    print("2) Small")
    print("3) Medium")
    print("4) Large")
    print("5) Huge (full dataset)")
    choice = input("Enter 1–5: ").strip()

    mapping = {
        "1": "tiny",
        "2": "small",
        "3": "medium",
        "4": "large",
        "5": "huge"
    }
    return mapping.get(choice, "huge")


def slice_dataset(products, size_label):
    # Use fractions of the full dataset for different sizes
    n = len(products)
    fractions = {
        "tiny": 0.05,
        "small": 0.10,
        "medium": 0.25,
        "large": 0.50,
        "huge": 1.00
    }
    frac = fractions.get(size_label, 1.0)
    k = max(1, int(n * frac))
    subset = products[:k]
    return subset


def run_bruteforce(values, weights, capacity, products):
    # Runs brute force and prints results + time
    print("\n=== Brute Force ===")
    if len(values) > 25:
        print(f"Note: {len(values)} items may be slow for brute force.")

    start = time.perf_counter()
    best_val, indices = knapsack_bruteforce(values, weights, capacity)
    end = time.perf_counter()

    total_cost = sum(products[i].price for i in indices)
    print(f"Value: {best_val}")
    print(f"Cost: ${total_cost:.2f}")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Items chosen:")
    for i in indices:
        p = products[i]
        print(f"  {p.id} | {p.category} | ${p.price:.2f} | util {p.utility}")


def run_dp(values, weights, capacity, products):
    # Runs DP and prints results + time
    print("\n=== Dynamic Programming ===")
    start = time.perf_counter()
    best_val, indices = knapsack_dp(values, weights, capacity)
    end = time.perf_counter()

    total_cost = sum(products[i].price for i in indices)
    print(f"Value: {best_val}")
    print(f"Cost: ${total_cost:.2f}")
    print(f"Runtime: {end - start:.6f} seconds")
    print("Items chosen:")
    for i in indices:
        p = products[i]
        print(f"  {p.id} | {p.category} | ${p.price:.2f} | util {p.utility}")


def main():
    # Point to the CSV file 
    root = Path(__file__).resolve().parents[1]
    csv_file = root / "data" / "retail_knapsack_dataset.csv"

    products_all = load_products(csv_file)
    print(f"Full dataset has {len(products_all)} items.\n")

    algo = choose_algorithm()
    size_label = choose_dataset_size()

    products = slice_dataset(products_all, size_label)
    print(f"\nUsing '{size_label}' dataset with {len(products)} items.\n")

    # Build knapsack inputs from the chosen slice
    values = [p.utility for p in products]
    weights = [int(round(p.price * 100)) for p in products]  # dollars → cents
    capacity_dollars = 100
    capacity = capacity_dollars * 100

    print(f"Capacity: ${capacity_dollars}\n")

    if algo in ("brute", "both"):
        run_bruteforce(values, weights, capacity, products)

    if algo in ("dp", "both"):
        run_dp(values, weights, capacity, products)


if __name__ == "__main__":
    main()