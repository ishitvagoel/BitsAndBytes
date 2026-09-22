"""Graph search."""

from bitsandbytes.graphs import (
    Graph,
    breadth_first_order,
    depth_first_order,
    dijkstra_distances,
)


def test_depth_first_and_breadth_first_orders() -> None:
    graph = Graph()
    for label in "ABCDE":
        graph.add_vertex(label)
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 1)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "E", 1)
    assert depth_first_order(graph, "A") == ["A", "B", "D", "C", "E"]
    assert breadth_first_order(graph, "A") == ["A", "B", "C", "D", "E"]


def test_dijkstra_distances_on_weighted_graph() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    assert dijkstra_distances(graph, "A") == {"A": 0, "C": 2, "B": 3, "D": 8}
