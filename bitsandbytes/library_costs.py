"""Built-in Python costs used in production algorithms.

This module does not reimplement CPython. It wraps ``collections.deque``,
``heapq``, and ``bisect`` so each lesson cites the library operation whose
cost matters.

Worked trace (``bfs_layer_sizes`` from source ``0``):

* Queue ``[0]``. Dequeue 0, enqueue unvisited neighbors 1 and 2 → layer size 2.
* Dequeue 1 and 2, enqueue 3 → next layer size 1.
* Dequeue 3, no new vertices → done. Layers ``[1, 2, 1]``.
"""

from __future__ import annotations

import bisect
import heapq
from collections import deque
from collections.abc import Hashable, Mapping, Sequence
from typing import TypeVar

T = TypeVar("T")
Vertex = TypeVar("Vertex", bound=Hashable)


def bfs_layer_sizes(
    adjacency: Mapping[Vertex, Sequence[Vertex]],
    start: Vertex,
) -> list[int]:
    """Return the size of each BFS layer starting at ``start``.

    Uses ``collections.deque`` because both ``append`` and ``popleft`` are
    O(1). Using ``list.pop(0)`` would make each dequeue O(n) and the whole
    search quadratic in the number of vertices.

    Cost
    ----
    Let V be reachable vertices and E be edges inspected. Each vertex is
    dequeued once and each edge checked once: O(V + E) time. The deque holds
    at most V labels: O(V) extra memory.
    """

    if start not in adjacency:
        return []
    visited: set[Vertex] = {start}
    queue: deque[Vertex] = deque([start])
    layers: list[int] = []
    while queue:
        width = len(queue)
        layers.append(width)
        for _ in range(width):
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    return layers


def top_k_smallest(values: Sequence[int], k: int) -> list[int]:
    """Return the ``k`` smallest integers in ascending order.

    ``heapq.nsmallest`` keeps a size-k heap and scans the input once.

    Cost
    ----
    Let n be ``len(values)``. Building the heap is O(n log k) time and O(k)
    extra memory. Sorting the whole list would be O(n log n).
    """

    if k < 0:
        raise ValueError("k cannot be negative.")
    if k == 0:
        return []
    return heapq.nsmallest(k, values)


def insert_into_sorted(sorted_values: list[T], item: T) -> None:
    """Insert ``item`` into ``sorted_values`` while keeping non-decreasing order.

    ``bisect.insort`` performs one binary search and one list insert. The
    insert shifts elements and costs O(n) for a list of length n.

    Cost
    ----
    O(n) time for the shift, O(n) extra memory briefly while CPython moves
    references. The search alone is O(log n).
    """

    bisect.insort(sorted_values, item)


def timsort_sorted(values: Sequence[T]) -> list[T]:
    """Return a new list sorted with Timsort (``list.sort``).

    Timsort is O(n log n) worst case, stable, and adaptive on partially
    sorted runs. This function copies first so the input is unchanged.

    Cost
    ----
    Copy is O(n). Sort is O(n log n) time. The copy uses O(n) extra memory.
    """

    copy = list(values)
    copy.sort()
    return copy


def list_pop_front_cost_demo(length: int) -> int:
    """Return how many reference moves ``pop(0)`` performs on a list of ``length``.

    CPython shifts every remaining element one slot toward index 0. That is
    why a queue should use ``deque.popleft``, not ``list.pop(0)``.

    Cost
    ----
    O(1) to compute the answer. The pedagogical ``pop(0)`` itself would be
    O(length) if you executed it.
    """

    if length < 0:
        raise ValueError("length cannot be negative.")
    return length - 1 if length else 0
