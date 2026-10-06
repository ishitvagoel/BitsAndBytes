"""Approximation algorithms.

Industry
--------
A working engineer distinguishes a proven lower bound from an unresolved
complexity assumption. General minimum vertex cover is NP-hard; no exact
polynomial-time algorithm is known. For a simple approximation, repeatedly
choose an uncovered edge and add its endpoints. The chosen edges are pairwise
vertex-disjoint, giving a 2-approximation.
"""

from __future__ import annotations

from bitsandbytes.graphs.adjacency_list import Graph


def vertex_cover_two_approximation(graph: Graph) -> set:
    """Return a 2-approximate vertex cover by scanning graph edges once.

    An edge here is an adjacency-list entry ``(source, target)``; a directed
    graph is treated as an edge set for vertex-cover purposes. When neither
    endpoint has been selected, add both. Every selected pair is disjoint from
    earlier pairs, so any cover must select at least one endpoint per pair.
    The result selects at most two endpoints per pair and is therefore at
    most twice the optimum. Self-loops add their single endpoint once.

    Cost
    ----
    Let V be the vertices and E the adjacency-list entries. Copying the vertex
    list and inspecting each edge once takes O(V + E) expected time, assuming
    expected O(1) set membership. The returned cover is O(V); ``vertices``
    also creates an O(V) temporary list, so peak extra memory is O(V).
    """

    cover: set = set()
    for source in graph.vertices():
        for target, _weight in graph.neighbors(source):
            if source not in cover and target not in cover:
                cover.add(source)
                cover.add(target)
    return cover
