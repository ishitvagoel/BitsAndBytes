"""Extended graph algorithms."""

from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import (
    UndirectedGraph,
    bellman_ford_distances,
    bfs_distances_and_parents,
    dag_shortest_paths,
    dijkstra_distances_heap,
    floyd_warshall,
    is_bipartite,
    kruskal_minimum_spanning_weight,
    topological_order,
    zero_one_bfs_distances,
)


def test_topological_and_dag_paths() -> None:
    graph: Graph = Graph()
    graph.add_edge("a", "b", 1)
    graph.add_edge("a", "c", 4)
    graph.add_edge("b", "d", 2)
    graph.add_edge("c", "d", 1)
    order = topological_order(graph)
    assert order.index("a") < order.index("d")
    distances = dag_shortest_paths(graph, "a")
    assert distances["d"] == 3


def test_bfs_distances_and_heap_dijkstra() -> None:
    graph: Graph = Graph()
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 2)
    distances, parents = bfs_distances_and_parents(graph, 0)
    assert distances[2] == 2
    assert parents[2] == 1
    weighted = Graph()
    weighted.add_edge(0, 1, 5)
    weighted.add_edge(0, 2, 1)
    weighted.add_edge(2, 1, 1)
    assert dijkstra_distances_heap(weighted, 0)[1] == 2


def test_bellman_ford_negative_edge() -> None:
    graph: Graph = Graph()
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, -2)
    graph.add_edge(0, 2, 4)
    assert bellman_ford_distances(graph, 0)[2] == -1


def test_kruskal_and_bipartite_and_zero_one_and_floyd() -> None:
    graph = UndirectedGraph()
    graph.add_edge("a", "b", 1)
    graph.add_edge("b", "c", 2)
    graph.add_edge("a", "c", 4)
    assert kruskal_minimum_spanning_weight(graph) == 3
    line = UndirectedGraph()
    line.add_edge("a", "b", 1)
    line.add_edge("b", "c", 1)
    assert is_bipartite(line)
    binary = Graph()
    binary.add_edge(0, 1, 0)
    binary.add_edge(1, 2, 1)
    assert zero_one_bfs_distances(binary, 0)[2] == 1
    tiny: Graph = Graph()
    tiny.add_edge(0, 1, 3)
    assert floyd_warshall(tiny)[0][1] == 3
