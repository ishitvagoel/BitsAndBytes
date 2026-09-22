"""Graph algorithms beyond the teaching scan-based Dijkstra."""

from __future__ import annotations

from collections.abc import Hashable
from typing import TypeVar

from bitsandbytes.deques.linked_deque import LinkedDeque
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.heaps.priority_queue import PriorityQueue
from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.union_find.disjoint_set import DisjointSet

Vertex = TypeVar("Vertex", bound=Hashable)


class UndirectedGraph(Graph):
    """Weighted graph whose ``add_edge`` inserts both directions."""

    def add_edge(self, source: Vertex, target: Vertex, weight: int) -> None:
        """Add an undirected edge between ``source`` and ``target``.

        Cost
        ----
        Two directed inserts: O(1) expected each.
        """

        super().add_edge(source, target, weight)
        super().add_edge(target, source, weight)


def bfs_distances_and_parents(
    graph: Graph,
    start: Vertex,
) -> tuple[dict[Vertex, int], dict[Vertex, Vertex | None]]:
    """Return shortest-hop distances and parent pointers from ``start``.

    Cost
    ----
    O(V + E) time, O(V) extra memory for maps and the queue.
    """

    distances: dict[Vertex, int] = {start: 0}
    parents: dict[Vertex, Vertex | None] = {start: None}
    queue: LinkedQueue[Vertex] = LinkedQueue()
    queue.enqueue(start)
    while not queue.is_empty:
        vertex = queue.dequeue()
        for neighbor, _weight in graph.neighbors(vertex):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[vertex] + 1
            parents[neighbor] = vertex
            queue.enqueue(neighbor)
    return distances, parents


def topological_order(graph: Graph) -> list[Vertex]:
    """Return a topological order, or raise if a cycle exists.

    Cost
    ----
    O(V + E) time and O(V) memory for indegrees and the queue.
    """

    indegree: dict[Vertex, int] = {vertex: 0 for vertex in graph.vertices()}
    for vertex in graph.vertices():
        for neighbor, _weight in graph.neighbors(vertex):
            indegree[neighbor] = indegree.get(neighbor, 0) + 1
    queue: LinkedQueue[Vertex] = LinkedQueue()
    for vertex, degree in indegree.items():
        if degree == 0:
            queue.enqueue(vertex)
    order: list[Vertex] = []
    while not queue.is_empty:
        vertex = queue.dequeue()
        order.append(vertex)
        for neighbor, _weight in graph.neighbors(vertex):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.enqueue(neighbor)
    if len(order) != len(indegree):
        raise ValueError("graph contains a cycle")
    return order


def connected_components(graph: Graph) -> list[list[Vertex]]:
    """Return connected components treating edges as undirected.

    Cost
    ----
    O(V + E) time, O(V) extra memory.
    """

    visited: set[Vertex] = set()
    components: list[list[Vertex]] = []
    for start in graph.vertices():
        if start in visited:
            continue
        stack = [start]
        component: list[Vertex] = []
        while stack:
            vertex = stack.pop()
            if vertex in visited:
                continue
            visited.add(vertex)
            component.append(vertex)
            for neighbor, _weight in graph.neighbors(vertex):
                if neighbor not in visited:
                    stack.append(neighbor)
        components.append(component)
    return components


def bellman_ford_distances(
    graph: Graph,
    start: Vertex,
) -> dict[Vertex, int]:
    """Return shortest-path distances allowing negative edges if no cycle.

    Cost
    ----
    O(VE) relaxations. O(V) extra memory.
    """

    distances: dict[Vertex, int] = {vertex: 10**18 for vertex in graph.vertices()}
    distances[start] = 0
    vertex_list = graph.vertices()
    for _ in range(len(vertex_list) - 1):
        updated = False
        for vertex in vertex_list:
            if distances[vertex] >= 10**18:
                continue
            for neighbor, weight in graph.neighbors(vertex):
                candidate = distances[vertex] + weight
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    updated = True
        if not updated:
            break
    for vertex in vertex_list:
        if distances[vertex] >= 10**18:
            continue
        for neighbor, weight in graph.neighbors(vertex):
            if distances[vertex] + weight < distances[neighbor]:
                raise ValueError("negative-weight cycle reachable from start")
    return {vertex: dist for vertex, dist in distances.items() if dist < 10**18}


def dag_shortest_paths(graph: Graph, start: Vertex) -> dict[Vertex, int]:
    """One pass after topological sort; negative weights allowed.

    Cost
    ----
    Topological sort plus one relaxation per edge: O(V + E).
    """

    order = topological_order(graph)
    distances: dict[Vertex, int] = {vertex: 10**18 for vertex in graph.vertices()}
    distances[start] = 0
    for vertex in order:
        if distances[vertex] >= 10**18:
            continue
        for neighbor, weight in graph.neighbors(vertex):
            candidate = distances[vertex] + weight
            if candidate < distances.get(neighbor, 10**18):
                distances[neighbor] = candidate
    return {vertex: dist for vertex, dist in distances.items() if dist < 10**18}


def dijkstra_distances_heap(
    graph: Graph,
    start: Vertex,
) -> dict[Vertex, int]:
    """Dijkstra with a binary heap and index map: O((V + E) log V).

    The scan-based ``dijkstra_distances`` in ``adjacency_list`` stays as the
    teaching O(V²) version.
    """

    best: dict[Vertex, int] = {start: 0}
    queue: PriorityQueue[Vertex] = PriorityQueue()
    tokens: dict[Vertex, int] = {start: queue.push(0, start)}
    settled: set[Vertex] = set()
    while queue:
        distance, vertex = queue.pop()
        if vertex in settled:
            continue
        settled.add(vertex)
        for neighbor, weight in graph.neighbors(vertex):
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights.")
            tentative = distance + weight
            if neighbor not in best or tentative < best[neighbor]:
                best[neighbor] = tentative
                if neighbor in tokens:
                    queue.decrease_key(tokens[neighbor], tentative)
                else:
                    tokens[neighbor] = queue.push(tentative, neighbor)
    return best


def kruskal_minimum_spanning_weight(
    graph: UndirectedGraph,
) -> int:
    """Return total weight of a minimum spanning tree via Kruskal.

    Cost
    ----
    O(E log E) to sort edges plus nearly O(E α(V)) unions.
    """

    edges: list[tuple[int, Vertex, Vertex]] = []
    seen: set[tuple[Vertex, Vertex]] = set()
    vertices = graph.vertices()
    index = {vertex: position for position, vertex in enumerate(vertices)}
    dsu = DisjointSet(len(vertices))
    for source in vertices:
        for target, weight in graph.neighbors(source):
            pair = (source, target) if source <= target else (target, source)
            if pair in seen:
                continue
            seen.add(pair)
            edges.append((weight, pair[0], pair[1]))
    edges.sort()
    total = 0
    for weight, first, second in edges:
        if dsu.connected(index[first], index[second]):
            continue
        dsu.union(index[first], index[second])
        total += weight
    return total


def prim_minimum_spanning_weight(
    graph: UndirectedGraph,
    start: Vertex,
) -> int:
    """Return total weight of a minimum spanning tree via Prim from ``start``.

    Cost
    ----
    O((V + E) log V) with the binary heap and ``decrease_key``.
    """

    visited: set[Vertex] = {start}
    queue: PriorityQueue[tuple[Vertex, Vertex]] = PriorityQueue()
    tokens: dict[tuple[Vertex, Vertex], int] = {}
    for neighbor, weight in graph.neighbors(start):
        edge = (start, neighbor)
        tokens[edge] = queue.push(weight, edge)
    total = 0
    while queue and len(visited) < len(graph.vertices()):
        weight, (_source, target) = queue.pop()
        if target in visited:
            continue
        visited.add(target)
        total += weight
        for neighbor, next_weight in graph.neighbors(target):
            if neighbor in visited:
                continue
            edge = (target, neighbor)
            if edge in tokens:
                queue.decrease_key(tokens[edge], next_weight)
            else:
                tokens[edge] = queue.push(next_weight, edge)
    return total


def is_bipartite(graph: Graph) -> bool:
    """Return whether the undirected view of ``graph`` is 2-colorable.

    Cost
    ----
    O(V + E) BFS coloring.
    """

    color: dict[Vertex, int] = {}
    for start in graph.vertices():
        if start in color:
            continue
        queue: LinkedQueue[Vertex] = LinkedQueue()
        queue.enqueue(start)
        color[start] = 0
        while not queue.is_empty:
            vertex = queue.dequeue()
            for neighbor, _weight in graph.neighbors(vertex):
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.enqueue(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
    return True


def has_directed_cycle(graph: Graph) -> bool:
    """Return whether ``graph`` contains a directed cycle.

    Cost
    ----
    O(V + E) DFS with three colors.
    """

    white, gray, black = 0, 1, 2
    state: dict[Vertex, int] = {vertex: white for vertex in graph.vertices()}

    def visit(vertex: Vertex) -> bool:
        state[vertex] = gray
        for neighbor, _weight in graph.neighbors(vertex):
            if state[neighbor] == gray:
                return True
            if state[neighbor] == white and visit(neighbor):
                return True
        state[vertex] = black
        return False

    return any(state[vertex] == white and visit(vertex) for vertex in graph.vertices())


def kosaraju_strongly_connected_components(
    graph: Graph,
) -> list[list[Vertex]]:
    """Return strongly connected components using Kosaraju's algorithm.

    Cost
    ----
    O(V + E) time, O(V) extra memory.
    """

    order: list[Vertex] = []
    visited: set[Vertex] = set()

    def dfs_finish(vertex: Vertex) -> None:
        visited.add(vertex)
        for neighbor, _weight in graph.neighbors(vertex):
            if neighbor not in visited:
                dfs_finish(neighbor)
        order.append(vertex)

    for vertex in graph.vertices():
        if vertex not in visited:
            dfs_finish(vertex)

    reversed_graph: dict[Vertex, list[Vertex]] = {vertex: [] for vertex in graph.vertices()}
    for source in graph.vertices():
        for target, _weight in graph.neighbors(source):
            reversed_graph[target].append(source)

    visited.clear()
    components: list[list[Vertex]] = []

    def dfs_collect(vertex: Vertex, component: list[Vertex]) -> None:
        visited.add(vertex)
        component.append(vertex)
        for neighbor in reversed_graph[vertex]:
            if neighbor not in visited:
                dfs_collect(neighbor, component)

    for vertex in reversed(order):
        if vertex not in visited:
            component: list[Vertex] = []
            dfs_collect(vertex, component)
            components.append(component)
    return components


def zero_one_bfs_distances(graph: Graph, start: Vertex) -> dict[Vertex, int]:
    """Shortest paths when every edge weight is 0 or 1 using a deque.

    Cost
    ----
    O(V + E) time, O(V) memory.
    """

    distances: dict[Vertex, int] = {start: 0}
    deque: LinkedDeque[Vertex] = LinkedDeque()
    deque.append_right(start)
    while len(deque):
        vertex = deque.pop_left()
        for neighbor, weight in graph.neighbors(vertex):
            if weight not in (0, 1):
                raise ValueError("zero_one_bfs requires weights 0 or 1")
            candidate = distances[vertex] + weight
            if neighbor not in distances or candidate < distances[neighbor]:
                distances[neighbor] = candidate
                if weight == 0:
                    deque.append_left(neighbor)
                else:
                    deque.append_right(neighbor)
    return distances


def floyd_warshall(graph: Graph) -> dict[Vertex, dict[Vertex, int]]:
    """All-pairs shortest paths with the Floyd-Warshall recurrence.

    Cost
    ----
    O(V³) time, O(V²) memory.
    """

    vertices = graph.vertices()
    dist: dict[Vertex, dict[Vertex, int]] = {
        source: {target: 10**18 for target in vertices} for source in vertices
    }
    for vertex in vertices:
        dist[vertex][vertex] = 0
    for source in vertices:
        for target, weight in graph.neighbors(source):
            dist[source][target] = min(dist[source][target], weight)
    for middle in vertices:
        for source in vertices:
            for target in vertices:
                through = dist[source][middle] + dist[middle][target]
                if through < dist[source][target]:
                    dist[source][target] = through
    return dist
