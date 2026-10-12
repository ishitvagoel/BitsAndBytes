"""Literal checks for the lesson trace helpers."""

from bitsandbytes.complexity import (
    RecurrenceShape,
    growth_table,
    pair_comparison_count,
    recursion_tree_levels,
)
from bitsandbytes.dynamic_programming.classic import fibonacci_modulo, min_coin_change
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import (
    dijkstra_distances_heap,
    topological_order,
)
from bitsandbytes.library_costs import list_pop_front_cost_demo
from bitsandbytes.sorting.insertion_sort import insertion_sort
from bitsandbytes.sorting.selection_and_radix import (
    binary_search_on_answer,
    counting_sort,
    quickselect,
)
from bitsandbytes.tracing import TraceEvent


def test_pair_comparison_count_emits_each_pair() -> None:
    events: list[TraceEvent] = []
    assert pair_comparison_count([3, 1, 2], trace_sink=events.append) == 3
    assert [event.kind for event in events] == ["compare", "compare", "compare"]
    assert events[-1].values["count"] == 3


def test_growth_table_row_for_64() -> None:
    assert growth_table((64,)) == [(64, 384, 4096)]


def test_recursion_tree_levels_for_8() -> None:
    rows = recursion_tree_levels(8, RecurrenceShape.MERGE_DIVIDE)
    assert rows[0] == (1, 8, 8)
    assert len(rows) == 4


def test_insertion_sort_events_name_the_key() -> None:
    events: list[TraceEvent] = []
    assert insertion_sort([3, 1, 2], trace_sink=events.append) == [1, 2, 3]
    assert [event.kind for event in events] == ["start", "insert", "insert"]
    assert events[1].values["key"] == 1


def test_pop_front_demo_counts_slides() -> None:
    events: list[TraceEvent] = []
    assert list_pop_front_cost_demo(4, trace_sink=events.append) == 3
    assert events[-1].values["moved"] == 3


def test_binary_search_on_answer_tests_6_3_4() -> None:
    piles = [3, 6, 7, 11]
    events: list[TraceEvent] = []

    def feasible(rate: int) -> bool:
        return sum((pile + rate - 1) // rate for pile in piles) <= 8

    assert binary_search_on_answer(1, max(piles), feasible, trace_sink=events.append) == 4
    assert [event.values["middle"] for event in events] == [6, 3, 4]
    assert events[0].kind == "test"


def test_counting_sort_and_quickselect_events() -> None:
    placed: list[TraceEvent] = []
    assert counting_sort([3, 1, 2, 1], maximum=3, trace_sink=placed.append) == [1, 1, 2, 3]
    assert placed[0].kind == "place" and placed[0].values["digit"] == 1
    selected: list[TraceEvent] = []
    assert quickselect([3, 1, 4, 2], 0, trace_sink=selected.append) == 1
    assert selected[0].kind == "partition"


def test_fibonacci_and_coins_emit_steps() -> None:
    steps: list[TraceEvent] = []
    assert fibonacci_modulo(6, 1000, trace_sink=steps.append) == 8
    assert steps[-1].values["current"] == 8
    coins: list[TraceEvent] = []
    assert min_coin_change([1, 3, 4], 6, trace_sink=coins.append) == 2
    assert coins[-1].kind == "amount" and coins[-1].values["coins"] == 2


def test_topo_and_dijkstra_emit_vertices() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 4)
    graph.add_edge("B", "C", 2)
    settled: list[TraceEvent] = []
    assert dijkstra_distances_heap(graph, "A", trace_sink=settled.append)["C"] == 3
    assert settled[0].kind == "settle" and settled[0].values["vertex"] == "A"
    dag = Graph()
    dag.add_edge("A", "B", 1)
    dag.add_edge("A", "C", 1)
    dag.add_edge("B", "D", 1)
    dag.add_edge("C", "D", 1)
    emitted: list[TraceEvent] = []
    assert topological_order(dag, trace_sink=emitted.append) == ["A", "B", "C", "D"]
    assert [event.values["vertex"] for event in emitted][0] == "A"


def test_vertex_cover_events_name_both_ends() -> None:
    from bitsandbytes.limits.approximation import vertex_cover_two_approximation

    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("C", "D", 1)
    events: list[TraceEvent] = []
    assert sorted(vertex_cover_two_approximation(graph, trace_sink=events.append)) == ["A", "B", "C", "D"]
    assert events[1].kind == "pair" and events[1].values["source"] == "A"
