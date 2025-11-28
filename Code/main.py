# Lets the user pick algorithm and dataset size, runs in batches, prints average time.

from pathlib import Path
import time
from data_loader import load_products
from algorithms import knapsack_bruteforce, knapsack_dp, knapsack_greedy


def choose_algorithm():
    print("Choose algorithm:")
    print("1) Dynamic programming")
    print("2) Greedy")
    print("3) Brute force")
    print("4) All three (DP -> Greedy -> Brute)")

    choice = input("Enter 1, 2, 3, or 4: ").strip()

    if choice == "1":
        return "dp"
    if choice == "2":
        return "greedy"
    if choice == "3":
        return "brute"
    return "all"


def choose_dataset_size():
    print("\nChoose dataset size:")
    print("1) Tiny")
    print("2) Small")
    print("3) Medium")
    print("4) Large")
    print("5) Huge (full dataset)")

    mapping = {
        "1": "tiny",
        "2": "small",
        "3": "medium",
        "4": "large",
        "5": "huge"
    }

    choice = input("Enter 1 to 5: ").strip()
    return mapping.get(choice, "huge")


def get_batch_runs():
    val = input("\nHow many runs for timing (example 100): ").strip()
    try:
        num = int(val)
        if num <= 0:
            return 1
        return num
    except:
        return 1


def slice_dataset(products, size_label):
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
    return products[:k]


def run_in_batches(name, algo_func, values, weights, capacity, products, runs):
    print(f"\n=== {name} ===")

    total_time = 0.0
    best_val = 0
    best_indices = []

    for _ in range(runs):
        start = time.perf_counter()
        val, indices = algo_func(values, weights, capacity)
        end = time.perf_counter()
        total_time += (end - start)
        best_val = val
        best_indices = indices

    avg = total_time / runs
    total_cost = sum(products[i].price for i in best_indices)

    print(f"Value: {best_val}")
    print(f"Cost: ${total_cost:.2f}")
    print(f"Average runtime over {runs} runs: {avg:.6f} seconds")
    print("Items chosen:")
    for i in best_indices:
        p = products[i]
        print(f"  {p.id} | {p.category} | ${p.price:.2f} | util {p.utility}")


def main():
    root = Path(__file__).resolve().parents[1]
    csv_file = root / "data" / "retail_knapsack_dataset.csv"

    products_all = load_products(csv_file)
    print(f"Full dataset has {len(products_all)} items.\n")

    algo = choose_algorithm()
    size_label = choose_dataset_size()
    runs = get_batch_runs()

    products = slice_dataset(products_all, size_label)
    print(f"\nUsing '{size_label}' dataset with {len(products)} items.")
    print(f"Running each selected algorithm {runs} time(s).\n")

    values = [p.utility for p in products]
    weights = [int(round(p.price * 100)) for p in products]
    capacity_dollars = 100
    capacity = capacity_dollars * 100

    print(f"Capacity: ${capacity_dollars}\n")

    
    if algo in ("dp", "all"):
        run_in_batches("Dynamic Programming", knapsack_dp, values, weights, capacity, products, runs)

    
    if algo in ("greedy", "all"):
        run_in_batches("Greedy", knapsack_greedy, values, weights, capacity, products, runs)

    #
    if algo in ("brute", "all"):
        run_in_batches("Brute Force", knapsack_bruteforce, values, weights, capacity, products, runs)


if __name__ == "__main__":
    main()