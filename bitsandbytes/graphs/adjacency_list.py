"""Graphs as adjacency lists.

Vertices are hashable labels. Each edge is ``(neighbor, weight)``. Depth-first
search uses a stack (or recursion). Breadth-first search uses a queue.
Dijkstra's algorithm uses a min-heap keyed by tentative distance; here the
smallest tentative distance is chosen by scanning the unsettled set, which is
O(V) per step and O(V^2) overall, honest for a first teaching version on
small graphs.
"""

from __future__ import annotations

from collections.abc import Hashable
from typing import TypeVar

from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.stacks.algorithm_stack import AlgorithmStack

Vertex = TypeVar("Vertex", bound=Hashable)


class Graph:
    """Directed weighted graph stored as adjacency lists."""

    def __init__(self) -> None:
        """Create an empty graph.

        Cost
        ----
        One empty dictionary: O(1).
        """

        self._adjacency: dict[Vertex, list[tuple[Vertex, int]]] = {}

    def add_vertex(self, vertex: Vertex) -> None:
        """Ensure ``vertex`` exists.

        Cost
        ----
        One dict insertion if missing: O(1) expected.
        """

        self._adjacency.setdefault(vertex, [])

    def add_edge(self, source: Vertex, target: Vertex, weight: int) -> None:
        """Add a directed edge from ``source`` to ``target``.

        Cost
        ----
        Two vertex lookups and one list append: O(1) expected amortized.
        """

        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source].append((target, weight))

    def neighbors(self, vertex: Vertex) -> list[tuple[Vertex, int]]:
        """Return outgoing edges from ``vertex``.

        Cost
        ----
        One dict lookup and returning the list reference: O(1) expected.
        """

        return self._adjacency[vertex]

    def vertices(self) -> list[Vertex]:
        """Return all vertex labels.

        Cost
        ----
        Copying dict keys is O(V) for V vertices.
        """

        return list(self._adjacency)


def depth_first_order(
    graph: Graph,
    start: Vertex,
) -> list[Vertex]:
    """Return vertices reachable from ``start`` in depth-first order.

    Cost
    ----
    Let V be reachable vertices and E be outgoing edges explored. Each vertex
    is pushed once on the stack and each edge is inspected once: O(V + E)
    time. The stack and visited set hold at most V entries: O(V) extra memory.
    """

    order: list[Vertex] = []
    visited: set[Vertex] = set()
    stack: AlgorithmStack[Vertex] = AlgorithmStack()
    stack.push(start)
    while not stack.is_empty:
        vertex = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)
        for neighbor, _weight in reversed(graph.neighbors(vertex)):
            if neighbor not in visited:
                stack.push(neighbor)
    return order


def breadth_first_order(
    graph: Graph,
    start: Vertex,
) -> list[Vertex]:
    """Return vertices reachable from ``start`` in breadth-first order.

    Cost
    ----
    Each vertex is enqueued once and each edge inspected once: O(V + E) time.
    The queue holds at most V labels: O(V) extra memory.
    """

    order: list[Vertex] = []
    visited: set[Vertex] = {start}
    queue: LinkedQueue[Vertex] = LinkedQueue()
    queue.enqueue(start)
    while not queue.is_empty:
        vertex = queue.dequeue()
        order.append(vertex)
        for neighbor, _weight in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
    return order


def dijkstra_distances(
    graph: Graph,
    start: Vertex,
) -> dict[Vertex, int]:
    """Return shortest-path distances from ``start`` with non-negative weights.

    This teaching version scans all unsettled vertices to pick the smallest
    tentative distance. That scan is O(V) per settled vertex, so total time
    is O(V^2) on V vertices. A binary min-heap would reduce the extraction
    step to O(log V) and the whole algorithm to O((V + E) log V).

    Cost
    ----
    The outer loop runs V times. Each iteration scans at most V entries in
    ``best`` and relaxes every outgoing edge of the chosen vertex. Worst-case
    time O(V^2 + E). The ``best`` map stores one integer per reachable
    vertex: O(V) extra memory.
    """

    best: dict[Vertex, int] = {start: 0}
    settled: set[Vertex] = set()
    vertex_count = len(graph.vertices())
    while len(settled) < vertex_count:
        candidate: Vertex | None = None
        candidate_distance: int | None = None
        for vertex, distance in best.items():
            if vertex in settled:
                continue
            if candidate is None or distance < candidate_distance:
                candidate = vertex
                candidate_distance = distance
        if candidate is None or candidate_distance is None:
            break
        settled.add(candidate)
        for neighbor, weight in graph.neighbors(candidate):
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")
            tentative = candidate_distance + weight
            if neighbor not in best or tentative < best[neighbor]:
                best[neighbor] = tentative
    return best
