"""Approximation algorithms."""

from __future__ import annotations

from bitsandbytes.graphs.adjacency_list import Graph


def vertex_cover_two_approximation(graph: Graph) -> set:
    """Return a vertex cover within twice the optimum size on any graph.

    Repeatedly take both endpoints of any uncovered edge until none remain.

    Cost
    ----
    O(V + E) time, O(V) memory for the cover set.
    """

    remaining_edges: list[tuple] = []
    for source in graph.vertices():
        for target, _weight in graph.neighbors(source):
            remaining_edges.append((source, target))
    cover: set = set()
    uncovered = set(remaining_edges)
    while uncovered:
        edge = uncovered.pop()
        first, second = edge
        cover.add(first)
        cover.add(second)
        uncovered = {
            candidate
            for candidate in uncovered
            if candidate[0] not in cover and candidate[1] not in cover
        }
    return cover
