from itertools import combinations   # for brute force subsets


def knapsack_bruteforce(values, weights, capacity):
    # Tries every subset. Only good for small inputs.
    n = len(values)
    best_value = 0
    best_items = []

    for r in range(n + 1):
        for combo in combinations(range(n), r):
            total_w = sum(weights[i] for i in combo)
            total_v = sum(values[i] for i in combo)

            if total_w <= capacity and total_v > best_value:
                best_value = total_v
                best_items = list(combo)

    return best_value, best_items


def knapsack_dp(values, weights, capacity):
    # Bottom up DP. Fast and exact.
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruct chosen items
    chosen = []
    w = capacity
    i = n
    while i > 0:
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
        i -= 1

    chosen.reverse()
    return dp[n][capacity], chosen


def knapsack_greedy(values, weights, capacity):
    # Greedy 0-1 knapsack by value to weight ratio.
    # This is a heuristic, not always optimal.
    n = len(values)
    indices = list(range(n))
    indices.sort(key=lambda i: values[i] / weights[i], reverse=True)

    total_value = 0
    total_weight = 0
    chosen = []

    for i in indices:
        if total_weight + weights[i] <= capacity:
            chosen.append(i)
            total_weight += weights[i]
            total_value += values[i]

    return total_value, chosen