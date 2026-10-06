"""Regression checks for the greedy vertex-cover approximation."""

from __future__ import annotations

from itertools import combinations

from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.limits.approximation import vertex_cover_two_approximation


def _minimum_cover_size(vertices: list[int], edges: list[tuple[int, int]]) -> int:
    for size in range(len(vertices) + 1):
        for selection in combinations(vertices, size):
            candidate = set(selection)
            if all(first in candidate or second in candidate for first, second in edges):
                return size
    raise AssertionError("a vertex cover must exist")


def test_greedy_cover_is_valid_and_within_twice_optimum_for_small_graphs() -> None:
    possible_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    for edge_mask in range(1 << len(possible_edges)):
        edges = [
            edge
            for bit, edge in enumerate(possible_edges)
            if edge_mask & (1 << bit)
        ]
        graph: Graph = Graph()
        for vertex in range(4):
            graph.add_vertex(vertex)
        for source, target in edges:
            graph.add_edge(source, target, 1)

        cover = vertex_cover_two_approximation(graph)
        optimum = _minimum_cover_size(list(range(4)), edges)

        assert all(source in cover or target in cover for source, target in edges)
        assert len(cover) <= 2 * optimum


def test_greedy_cover_handles_reciprocal_edges_and_self_loops() -> None:
    graph: Graph = Graph()
    graph.add_edge("a", "b", 1)
    graph.add_edge("b", "a", 1)
    graph.add_edge("c", "c", 1)

    cover = vertex_cover_two_approximation(graph)

    assert "a" in cover or "b" in cover
    assert "c" in cover
