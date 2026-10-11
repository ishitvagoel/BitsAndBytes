import random

from bitsandbytes.graphs.adjacency_list import Graph, breadth_first_order
from bitsandbytes.hash_tables.chaining import ChainingHashTable
from bitsandbytes.heaps.heapsort import heapify
from bitsandbytes.linear.dynamic_array import DynamicArray
from bitsandbytes.sorting.merge_sort import merge_sort
from bitsandbytes.sorting.quick_sort import quick_sort
from bitsandbytes.tracing import TraceEvent
from bitsandbytes.trees.bst import BinarySearchTree
from bitsandbytes.union_find.disjoint_set import DisjointSet


def test_merge_sort_emits_the_split_and_each_take():
    events: list[TraceEvent] = []
    assert merge_sort([3, 1], trace_sink=events.append) == [1, 3]
    assert [event.kind for event in events] == ["split", "take", "take"]
    assert events[0].values == {"left": [3], "right": [1]}
    assert events[1].values["value"] == 1
    assert events[2].values["merged"] == [1, 3]


def test_merge_sort_without_a_sink_still_returns_the_sorted_list():
    assert merge_sort([3, 1, 4, 2]) == [1, 2, 3, 4]


def test_heapify_emits_one_sift_per_parent():
    events: list[TraceEvent] = []
    values = [3, 1, 4, 2]
    heapify(values, trace_sink=events.append)
    assert values == [4, 2, 3, 1]
    assert [event.kind for event in events] == ["sift", "sift"]
    assert events[-1].values["values"] == [4, 2, 3, 1]


def test_quick_sort_emits_a_pivot_for_the_seeded_partition():
    events: list[TraceEvent] = []
    values = [3, 1, 4, 2]
    assert quick_sort(values, rng=random.Random(0), trace_sink=events.append) == [1, 2, 3, 4]
    assert events[0].kind == "pivot"
    assert any(event.kind == "swap" for event in events)


def test_breadth_first_order_emits_enqueue_and_dequeue():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 1)
    events: list[TraceEvent] = []
    assert breadth_first_order(graph, "A", trace_sink=events.append) == ["A", "B", "C"]
    assert [event.kind for event in events] == ["enqueue", "dequeue", "enqueue", "enqueue", "dequeue", "dequeue"]
    assert events[0].values["vertex"] == "A"
    assert events[1].values["order"] == ["A"]


def test_bst_insert_emits_the_child_side():
    events: list[TraceEvent] = []
    tree = BinarySearchTree(trace_sink=events.append)
    tree.insert(4)
    tree.insert(2)
    assert [event.values["side"] for event in events] == ["root", "left"]
    assert events[1].values == {"value": 2, "parent": 4, "side": "left"}


def test_chaining_emits_the_bucket_chain():
    events: list[TraceEvent] = []
    table = ChainingHashTable(bucket_count=4, trace_sink=events.append)
    table[0] = 1
    table[4] = 2
    assert events[-1].kind == "bucket"
    assert events[-1].values["chain"] == [(0, 1), (4, 2)]


def test_union_emits_the_parent_link():
    events: list[TraceEvent] = []
    sets = DisjointSet(3, use_heuristics=False, trace_sink=events.append)
    sets.union(0, 1)
    sets.union(1, 2)
    assert [event.values["parents"] for event in events] == [[0, 0, 2], [0, 0, 0]]


def test_dynamic_array_emits_each_resize_copy():
    events: list[TraceEvent] = []
    array = DynamicArray(trace_sink=events.append)
    array.append("a")
    array.append("b")
    array.append("c")
    assert list(array) == ["a", "b", "c"]
    assert [event.values for event in events] == [{"copied": 1, "capacity": 2}, {"copied": 2, "capacity": 4}]
