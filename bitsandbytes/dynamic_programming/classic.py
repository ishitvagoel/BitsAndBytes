"""Bottom-up dynamic programming classics.

Each function fills a table in dependency order. Memoized recursion is not the
required form; the word-RAM Fibonacci uses a fixed modulus so each cell is one
machine word.
"""

from __future__ import annotations

from collections.abc import Hashable, Mapping, Sequence

from bitsandbytes.graphs.adjacency_list import Graph


def fibonacci_modulo(n: int, mod: int = 10**9 + 7) -> int:
    """Return F(n) modulo ``mod`` with a bottom-up table.

    Cost
    ----
    O(n) word operations, O(n) extra memory for the table (O(1) memory
    variant keeps only two previous values in O(n) time).
    """

    if n < 0:
        raise ValueError("n cannot be negative.")
    if mod < 1:
        raise ValueError("mod must be positive.")
    if n == 0:
        return 0
    if n == 1:
        return 1 % mod
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, (previous + current) % mod
    return current


def min_coin_change(coins: Sequence[int], amount: int) -> int:
    """Return the minimum number of coins to make ``amount``, or -1 if impossible.

    Cost
    ----
    O(amount × len(coins)) time, O(amount) memory.
    """

    table = [amount + 1] * (amount + 1)
    table[0] = 0
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                table[value] = min(table[value], table[value - coin] + 1)
    return -1 if table[amount] > amount else table[amount]


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """Return maximum value for 0/1 knapsack with integer capacity ``capacity``.

    Cost
    ----
    O(nW) time and O(W) memory with one rolling row where n = len(weights).
    """

    row = [0] * (capacity + 1)
    for index, weight in enumerate(weights):
        value = values[index]
        for cap in range(capacity, weight - 1, -1):
            row[cap] = max(row[cap], row[cap - weight] + value)
    return row[capacity]


def longest_common_subsequence(first: str, second: str) -> int:
    """Return the length of a longest common subsequence.

    Cost
    ----
    O(nm) time and O(min(n, m)) memory with one row.
    """

    if len(first) < len(second):
        first, second = second, first
    previous = [0] * (len(second) + 1)
    for char_a in first:
        current = [0]
        for index, char_b in enumerate(second, start=1):
            if char_a == char_b:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current
    return previous[-1]


def edit_distance(first: str, second: str) -> int:
    """Return Levenshtein edit distance.

    Cost
    ----
    O(nm) time, O(min(n, m)) memory.
    """

    if len(first) < len(second):
        first, second = second, first
    previous = list(range(len(second) + 1))
    for char_a in first:
        current = [previous[0] + 1]
        for index, char_b in enumerate(second, start=1):
            cost = 0 if char_a == char_b else 1
            current.append(
                min(
                    previous[index] + 1,
                    current[-1] + 1,
                    previous[index - 1] + cost,
                )
            )
        previous = current
    return previous[-1]


def lis_length_quadratic(values: Sequence[int]) -> int:
    """Return longest increasing subsequence length in O(n²) time.

    Cost
    ----
    O(n²) time, O(n) memory.
    """

    if not values:
        return 0
    best = [1] * len(values)
    for index, value in enumerate(values):
        for earlier in range(index):
            if values[earlier] < value:
                best[index] = max(best[index], best[earlier] + 1)
    return max(best)


def lis_length_patience(values: Sequence[int]) -> int:
    """Return LIS length in O(n log n) using patience sorting piles.

    Cost
    ----
    O(n log n) time from binary search on pile tops, O(n) memory.
    """

    import bisect

    piles: list[int] = []
    for value in values:
        position = bisect.bisect_left(piles, value)
        if position == len(piles):
            piles.append(value)
        else:
            piles[position] = value
    return len(piles)


def max_non_adjacent_sum(values: Sequence[int]) -> int:
    """Return max sum of a subset with no adjacent elements.

    Cost
    ----
    O(n) time, O(1) memory (two rolling totals).
    """

    include = 0
    exclude = 0
    for value in values:
        include, exclude = exclude + value, max(include, exclude)
    return max(include, exclude)


def word_break_possible(text: str, dictionary: Sequence[str]) -> bool:
    """Return whether ``text`` can be segmented into dictionary words.

    Cost
    ----
    O(n · d) for n = len(text) and d dictionary size (hash lookups expected
    O(1)).
    """

    words = set(dictionary)
    reachable = [False] * (len(text) + 1)
    reachable[0] = True
    for end in range(1, len(text) + 1):
        for start in range(end):
            if reachable[start] and text[start:end] in words:
                reachable[end] = True
                break
    return reachable[len(text)]


def dag_dp_longest_path(graph: Graph, start: Hashable) -> int:
    """Return longest-path weight from ``start`` on a DAG.

    Cost
    ----
    One topological pass: O(V + E).
    """

    from bitsandbytes.graphs.algorithms import topological_order

    order = topological_order(graph)
    best: dict[Hashable, int] = {vertex: float("-inf") for vertex in graph.vertices()}
    best[start] = 0
    for vertex in order:
        if best[vertex] == float("-inf"):
            continue
        for neighbor, weight in graph.neighbors(vertex):
            best[neighbor] = max(best[neighbor], best[vertex] + weight)
    return int(max(best.values()))


def unbounded_knapsack_max_value(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> int:
    """Return max value when each item can be used many times.

    Cost
    ----
    O(nW) time, O(W) memory — same table shape as bounded coin change.
    """

    row = [0] * (capacity + 1)
    for index, weight in enumerate(weights):
        value = values[index]
        for cap in range(weight, capacity + 1):
            row[cap] = max(row[cap], row[cap - weight] + value)
    return row[capacity]
