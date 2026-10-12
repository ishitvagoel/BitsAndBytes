"""Worked-trace frames computed by calling the library."""

from __future__ import annotations

import random

from bitsandbytes.approximate.structures import BloomFilter
from bitsandbytes.backtracking.search import permutations
from bitsandbytes.complexity import (
    RecurrenceShape,
    growth_table,
    pair_comparison_count,
    recursion_tree_levels,
)
from bitsandbytes.dynamic_programming.classic import fibonacci_modulo, min_coin_change
from bitsandbytes.graphs.adjacency_list import Graph, breadth_first_order
from bitsandbytes.graphs.algorithms import (
    UndirectedGraph,
    dijkstra_distances_heap,
    kruskal_minimum_spanning_weight,
    prim_minimum_spanning_weight,
    topological_order,
)
from bitsandbytes.greedy.classic import interval_scheduling_max_count
from bitsandbytes.hash_tables.chaining import ChainingHashTable
from bitsandbytes.hash_tables.linear_probing import LinearProbingHashTable
from bitsandbytes.heaps.heapsort import heapsort
from bitsandbytes.heaps.priority_queue import PriorityQueue
from bitsandbytes.library_costs import list_pop_front_cost_demo
from bitsandbytes.limits.approximation import vertex_cover_two_approximation
from bitsandbytes.linear.dynamic_array import DynamicArray
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.cycle import find_cycle_start
from bitsandbytes.linked_lists.lru_cache import LRUCache
from bitsandbytes.linked_lists.merge_sorted import merge_sorted
from bitsandbytes.linked_lists.middle import middle_node
from bitsandbytes.linked_lists.nth_from_end import nth_from_end
from bitsandbytes.linked_lists.reverse import reverse_iterative
from bitsandbytes.patterns.arrays import PrefixSum, sliding_window_maximum, two_sum_sorted
from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.range_queries.structures import FenwickTree
from bitsandbytes.sorting.insertion_sort import insertion_sort
from bitsandbytes.sorting.merge_sort import merge_sort
from bitsandbytes.sorting.quick_sort import quick_sort
from bitsandbytes.sorting.selection_and_radix import (
    binary_search_on_answer,
    counting_sort,
    inversion_count,
    quickselect,
)
from bitsandbytes.stacks.infix_postfix import evaluate_infix
from bitsandbytes.stacks.next_greater import next_greater
from bitsandbytes.stacks.stack import Stack
from bitsandbytes.stacks.symbol_balance import symbols_are_balanced
from bitsandbytes.storage.engines import sequential_scan_sum
from bitsandbytes.strings.algorithms import Trie, kmp_search
from bitsandbytes.tracing import TraceEvent
from bitsandbytes.trees.bst import BinarySearchTree
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree
from bitsandbytes.trees.traversals import level_order, preorder
from bitsandbytes.union_find.disjoint_set import DisjointSet


def shot(
    label: str,
    narration: str,
    state: list[tuple[str, str]],
    values: list[object],
    status: str = "active",
) -> dict[str, object]:
    words = narration.split()
    if len(words) > 25:
        raise SystemExit(f"narration is {len(words)} words: {narration}")
    if "recorded" in narration:
        raise SystemExit(narration)
    return {
        "label": label,
        "narration": narration,
        "state": [{"name": name, "value": value} for name, value in state],
        "rows": [{"label": "State", "cells": [{"text": str(item), "status": status} for item in values]}],
    }


def _listen() -> tuple[list[TraceEvent], object]:
    events: list[TraceEvent] = []
    return events, events.append


def _cap(frames: list[dict[str, object]], slug: str) -> list[dict[str, object]]:
    frames = frames[:12]
    if len(frames) < 3:
        raise SystemExit(f"{slug} has {len(frames)} frames")
    for previous, current in zip(frames, frames[1:], strict=False):
        if previous["state"] == current["state"] and previous["narration"] == current["narration"]:
            raise SystemExit(f"{slug} repeats a frame: {current['narration']}")
    return frames


def _insertion(slug: str) -> list[dict[str, object]]:
    events, sink = _listen()
    values = [3, 1, 2]
    assert insertion_sort(values, trace_sink=sink) == [1, 2, 3]
    frames = []
    for event in events:
        if event.kind == "start":
            text = "The input is 3, 1, 2. Nothing is inserted yet."
        elif slug == "loop-invariants":
            text = f"After inserting {event.values['key']}, the prefix through index {event.values['index']} is sorted."
        else:
            text = f"Inserted {event.values['key']}. The list is now {event.values['values']}."
        frames.append(shot(event.kind, text, [("list", str(event.values["values"]))], list(event.values["values"])))
    return frames


def _pop_front(slug: str) -> list[dict[str, object]]:
    events, sink = _listen()
    assert list_pop_front_cost_demo(3, trace_sink=sink) == 2
    frames = []
    for event in events:
        moved = int(event.values["moved"])
        if slug == "cost-models":
            text = f"A list of length 3 has moved {moved} references so far."
        else:
            text = f"Front removal has slid {moved} references toward index 0."
        frames.append(shot("Slide" if moved else "Start", text, [("moved", str(moved))], [moved], "chosen"))
    return frames


def frames_for(slug: str) -> list[dict[str, object]] | None:
    """Return at least three frames, or None when this module does not own the slug."""

    built = _BUILDERS.get(slug)
    if built is None:
        return None
    return _cap(built(), slug)


def _input_size() -> list[dict[str, object]]:
    events, sink = _listen()
    assert pair_comparison_count([3, 1, 2], trace_sink=sink) == 3
    frames = []
    for event in events:
        text = f"Compare {event.values['first']} with {event.values['second']}. The pair count is {event.values['count']}."
        frames.append(shot("Pair", text, [("count", str(event.values["count"]))], [event.values["count"]], "chosen"))
    return frames


def _growth() -> list[dict[str, object]]:
    rows = growth_table((4, 16, 64, 256))
    assert rows[2] == (64, 384, 4096)
    frames = []
    for size, log_term, square in rows:
        text = f"At n = {size}, n log2 n is {log_term} and n squared is {square}."
        frames.append(shot(f"n={size}", text, [("n", str(size))], [size, log_term, square], "chosen"))
    return frames


def _recursion() -> list[dict[str, object]]:
    rows = recursion_tree_levels(8, RecurrenceShape.MERGE_DIVIDE)
    assert rows[0] == (1, 8, 8) and len(rows) == 4
    frames = []
    for index, (count, width, work) in enumerate(rows):
        text = f"Level {index} has {count} calls of size {width}. The level still does {work} work."
        frames.append(shot(f"Level {index}", text, [("work", str(work))], [count, width, work]))
    return frames


def _linked() -> list[dict[str, object]]:
    events, sink = _listen()
    chain = LinkedList()
    chain.append("a")
    chain.append("b")
    chain.append("c")
    chain.remove("b", trace_sink=sink)
    assert list(chain) == ["a", "c"]
    frames = [
        shot("Append", "Append a. The head and the tail are both a.", [("head", "a")], ["a"], "chosen"),
        shot("Append", "Append b. The tail moves to b.", [("tail", "b")], ["a", "b"], "active"),
        shot("Append", "Append c. The chain is a, b, c.", [("size", "3")], ["a", "b", "c"], "active"),
    ]
    for event in events:
        frames.append(shot("Visit", f"The scan visits {event.values['value']} while looking for b.", [("node", str(event.values["value"]))], list(chain) if event.values["value"] == "b" else ["a", "b", "c"]))
    assert list(chain) == ["a", "c"]
    return frames


def _stack() -> list[dict[str, object]]:
    stack = Stack(limit=4)
    held: list[int] = []
    frames = []
    for item in (1, 2, 3):
        assert stack.push(item) == item
        held.append(item)
        frames.append(shot("Push", f"Pushed {item}. The top is {item}.", [("top", str(item))], list(held), "chosen"))
    assert stack.pop() == 3
    held.pop()
    frames.append(shot("Pop", "The first pop returns 3. The top is now 2.", [("top", "2")], list(held), "active"))
    return frames


def _queue() -> list[dict[str, object]]:
    queue = LinkedQueue()
    held: list[str] = []
    frames = []
    for item in ("a", "b", "c"):
        queue.enqueue(item)
        held.append(item)
        frames.append(shot("Enqueue", f"Enqueued {item}. The front is {held[0]}.", [("front", held[0])], list(held)))
    assert queue.dequeue() == "a"
    held.pop(0)
    frames.append(shot("Dequeue", "The first dequeue returns a. The front is now b.", [("front", "b")], list(held), "chosen"))
    return frames


def _merge() -> list[dict[str, object]]:
    events, sink = _listen()
    assert merge_sort([3, 1, 4, 2], trace_sink=sink) == [1, 2, 3, 4]
    frames = []
    for event in events:
        if event.kind == "split":
            values = list(event.values["left"]) + list(event.values["right"])
            text = f"Split into {event.values['left']} and {event.values['right']}."
            frames.append(shot("Split", text, [("left", str(event.values["left"]))], values, "active"))
        else:
            text = f"The merge takes {event.values['value']}. The output is {event.values['merged']}."
            frames.append(shot("Take", text, [("output", str(event.values["merged"]))], list(event.values["merged"]), "chosen"))
    return frames


def _quick() -> list[dict[str, object]]:
    events, sink = _listen()
    values = [3, 1, 4, 2]
    assert quick_sort(values, rng=random.Random(0), trace_sink=sink) == [1, 2, 3, 4]
    frames = []
    for event in events:
        if event.kind == "pivot":
            text = f"Pivot {event.values['value']} sits at index {event.values['index']}."
        else:
            text = f"Swap index {event.values['index']} with the boundary at {event.values['boundary']}."
        frames.append(shot(event.kind, text, [("array", str(event.values["values"]))], list(event.values["values"]), "chosen"))
    return frames


def _graph_walk() -> list[dict[str, object]]:
    events, sink = _listen()
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 1)
    graph.add_edge("B", "D", 1)
    assert breadth_first_order(graph, "A", trace_sink=sink) == ["A", "B", "C", "D"]
    frames = []
    for event in events:
        shown = event.values.get("order", [event.values["vertex"]])
        text = f"{event.kind.capitalize()} {event.values['vertex']}."
        if len(text.split()) < 3:
            text = f"The search marks {event.values['vertex']} during {event.kind}."
        frames.append(shot(str(event.kind), text, [("vertex", str(event.values["vertex"]))], list(shown), "active"))
    return frames


def _bst() -> list[dict[str, object]]:
    events, sink = _listen()
    tree = BinarySearchTree(trace_sink=sink)
    for value in (4, 2, 6, 1):
        tree.insert(value)
    assert tree.inorder() == [1, 2, 4, 6]
    frames = []
    for event in events:
        text = f"{event.values['value']} becomes the {event.values['side']} child of {event.values['parent']}."
        frames.append(shot(str(event.values["side"]), text, [("parent", str(event.values["parent"]))], [event.values["value"]], "chosen"))
    return frames


def _chain() -> list[dict[str, object]]:
    events, sink = _listen()
    table = ChainingHashTable(bucket_count=4, trace_sink=sink)
    table[0] = 1
    table[4] = 2
    assert table[0] == 1 and table[4] == 2
    frames = []
    for event in events:
        if event.kind == "lookup":
            text = f"Lookup of {event.values['key']} returns {event.values['value']}."
            values = [event.values["key"], event.values["value"]]
        else:
            keys = [pair[0] for pair in event.values["chain"]]
            text = f"Key {event.values['key']} joined bucket {event.values['index']}."
            values = keys
        frames.append(shot("Bucket", text, [("index", str(event.values["index"]))], values, "active"))
    return frames


def _union() -> list[dict[str, object]]:
    events, sink = _listen()
    sets = DisjointSet(3, use_heuristics=False, trace_sink=sink)
    sets.union(0, 1)
    sets.union(1, 2)
    assert sets.find(2) == 0
    frames = []
    for event in events:
        text = f"{event.values['child']} now points at {event.values['parent']}."
        frames.append(shot("Link", text, [("parents", str(event.values["parents"]))], list(event.values["parents"]), "chosen"))
    frames.append(shot("Find", "find of 2 walks to the root 0.", [("root", "0")], [0, 0, 0], "done"))
    return frames


def _dynamic_array() -> list[dict[str, object]]:
    events, sink = _listen()
    array = DynamicArray(trace_sink=sink)
    for item in ("a", "b", "c"):
        array.append(item)
    assert list(array) == ["a", "b", "c"] and array.total_copy_cost_for_appends(3) == 3
    frames = []
    for event in events:
        if event.kind == "resize":
            text = f"The grow copied {event.values['copied']} references. Capacity is {event.values['capacity']}."
            values = [event.values["copied"], event.values["capacity"]]
        else:
            text = f"Appended {event.values['item']}. Length is {event.values['length']}."
            values = [event.values["item"], event.values["length"]]
        frames.append(shot(event.kind, text, [(event.kind, str(values[-1]))], values))
    return frames


def _heap() -> list[dict[str, object]]:
    events, sink = _listen()
    values = [3, 1, 4, 2]
    assert heapsort(values, trace_sink=sink) == [1, 2, 3, 4]
    frames = []
    for event in events:
        if event.kind == "sift":
            text = f"Sift-down at index {event.values['index']} leaves {event.values['values']}."
        else:
            text = f"Extract moves the next root. The array is {event.values['values']}."
        frames.append(shot(event.kind, text, [("heap", str(event.values["values"]))], list(event.values["values"]), "active"))
    return frames


def _fibonacci() -> list[dict[str, object]]:
    events, sink = _listen()
    assert fibonacci_modulo(6, 1000, trace_sink=sink) == 8
    frames = []
    for event in events:
        text = f"F({event.values['number']}) is {event.values['current']}. The previous value is {event.values['previous']}."
        frames.append(shot(f"F({event.values['number']})", text, [("current", str(event.values["current"]))], [event.values["previous"], event.values["current"]], "chosen"))
    return frames


def _reverse() -> list[dict[str, object]]:
    events, sink = _listen()
    chain = LinkedList()
    for item in (1, 2, 3):
        chain.append(item)
    reverse_iterative(chain, trace_sink=sink)
    assert list(chain) == [3, 2, 1]
    frames = []
    for event in events:
        text = f"The reversed prefix now starts at {event.values['head']}."
        frames.append(shot("Flip", text, [("head", str(event.values["head"]))], list(event.values["chain"]), "chosen"))
    return frames


def _merge_lists() -> list[dict[str, object]]:
    events, sink = _listen()
    left, right = LinkedList(), LinkedList()
    for item in (1, 4):
        left.append(item)
    for item in (2, 3):
        right.append(item)
    merged = merge_sorted(left, right, trace_sink=sink)
    assert list(merged) == [1, 2, 3, 4]
    frames = []
    taken: list[object] = []
    for event in events:
        taken.append(event.values["value"])
        text = f"The merge takes {event.values['value']}. The result so far is {taken}."
        frames.append(shot("Take", text, [("taken", str(event.values["value"]))], list(taken), "chosen"))
    return frames


def _nth() -> list[dict[str, object]]:
    events, sink = _listen()
    chain = LinkedList()
    for item in (1, 2, 3, 4):
        chain.append(item)
    assert nth_from_end(chain, 2, trace_sink=sink).data == 3
    frames = []
    for event in events:
        if event.kind == "gap":
            text = f"The leader has taken {event.values['step']} steps. It sits on {event.values['leader']}."
        else:
            text = f"Both pointers move. The trailer is on {event.values['trailer']}."
        frames.append(shot(event.kind, text, [("step", str(event.values.get("step", event.values.get("trailer"))))], [1, 2, 3, 4]))
    return frames


def _fast_slow() -> list[dict[str, object]]:
    chain = LinkedList([1, 2, 3, 4, 5])
    middle = middle_node(chain)
    assert middle is not None and middle.data == 3
    even = LinkedList([1, 2, 3, 4])
    even_middle = middle_node(even)
    assert even_middle is not None and even_middle.data == 3
    cycled = LinkedList([1, 2, 3, 4, 5])
    cycled.node_at(4).next = cycled.node_at(2)
    found = find_cycle_start(cycled)
    assert found is not None and found[0] == 3
    return [
        shot("Middle", "The slow pointer on 1 through 5 stops on 3.", [("middle", "3")], [1, 2, 3, 4, 5], "chosen"),
        shot("Even", "The even list 1 through 4 keeps the later middle 3.", [("middle", "3")], [1, 2, 3, 4], "active"),
        shot("Entrance", "The cycle entrance is the node holding 3.", [("index", "3")], [1, 2, 3, 4, 5], "done"),
    ]


def _doubly() -> list[dict[str, object]]:
    from bitsandbytes.doubly_linked_list import DoublyLinkedList

    chain = DoublyLinkedList()
    frames = []
    first = chain.append("a")
    frames.append(shot("Append", "Append a. Head and tail both hold a.", [("head", "a")], ["a"], "chosen"))
    chain.append("b")
    frames.append(shot("Append", "Append b. The tail is now b.", [("tail", "b")], ["a", "b"], "active"))
    assert chain.remove_node(first) == "a"
    frames.append(shot("Unlink", "Removing the known node a leaves b.", [("removed", "a")], ["b"], "done"))
    return frames


def _greater() -> list[dict[str, object]]:
    events, sink = _listen()
    assert next_greater([2, 1, 2, 4, 3], trace_sink=sink) == [4, 2, 4, None, None]
    frames = []
    for event in events:
        text = f"Index {event.values['index']} holds {event.values['value']}. Answers are {event.values['answers']}."
        frames.append(shot("Scan", text, [("index", str(event.values["index"]))], list(event.values["answers"])))
    return frames


def _parsing() -> list[dict[str, object]]:
    assert symbols_are_balanced("([])") is True
    assert symbols_are_balanced("([)]") is False
    assert evaluate_infix("2+3*4") == 14
    return [
        shot("Match", "([]) is balanced. Each closer matches the top opener.", [("ok", "true")], ["(", "[", "]", ")"], "chosen"),
        shot("Cross", "([)] is not balanced. The closer does not match the top.", [("ok", "false")], ["(", "[", ")", "]"], "active"),
        shot("Value", "2+3*4 evaluates to 14. Multiplication runs first.", [("value", "14")], [2, 3, 4, 14], "done"),
    ]


def _counting() -> list[dict[str, object]]:
    events, sink = _listen()
    assert counting_sort([3, 1, 2, 1], maximum=3, trace_sink=sink) == [1, 1, 2, 3]
    frames = []
    for event in events:
        text = f"Place {event.values['count']} copies of {event.values['digit']}. Output is {event.values['output']}."
        frames.append(shot("Place", text, [("digit", str(event.values["digit"]))], list(event.values["output"]), "chosen"))
    return frames


def _select() -> list[dict[str, object]]:
    events, sink = _listen()
    assert quickselect([3, 1, 4, 2], 2, trace_sink=sink) == 3
    frames = []
    for event in events:
        text = f"Pivot {event.values['value']} lands at index {event.values['index']}. The array is {event.values['values']}."
        frames.append(shot("Partition", text, [("index", str(event.values["index"]))], list(event.values["values"]), "chosen"))
    if len(frames) < 3:
        frames.append(shot("Answer", "k is 2, so the value at that index is the answer 3.", [("k", "2")], [3], "done"))
    return frames


def _inversions() -> list[dict[str, object]]:
    events, sink = _listen()
    assert inversion_count([3, 1, 4, 2], trace_sink=sink) == 3
    frames = []
    for event in events:
        text = f"Taking {event.values['taken']} adds {event.values['added']} inversions. The total is {event.values['count']}."
        frames.append(shot("Cross", text, [("count", str(event.values["count"]))], [event.values["count"]], "chosen"))
    return frames


def _probe() -> list[dict[str, object]]:
    table = LinearProbingHashTable(capacity=4)
    table[0] = 1
    frames = [shot("Insert", "Key 0 takes slot 0.", [("slot", "0")], [0], "chosen")]
    table[4] = 2
    frames.append(shot("Probe", "Key 4 shares the start slot and takes slot 1.", [("slot", "1")], [0, 4], "active"))
    del table[0]
    assert table[4] == 2
    frames.append(shot("Tombstone", "Deleting 0 leaves a tombstone. Lookup of 4 still returns 2.", [("found", "2")], [4], "done"))
    return frames


def _lru() -> list[dict[str, object]]:
    cache = LRUCache[str, int](2)
    cache.put("a", 1)
    cache.put("b", 2)
    frames = [
        shot("Put", "Put a, then b. Capacity 2 is full.", [("tail", "a")], ["b", "a"], "active"),
        shot("Get", "Get a moves a off the tail. b is now least recent.", [("recent", "a")], ["a", "b"], "chosen"),
    ]
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None
    frames.append(shot("Evict", "Put c evicts b. A later get of b returns None.", [("evicted", "b")], ["c", "a"], "done"))
    return frames


def _walks() -> list[dict[str, object]]:
    tree = BinarySearchTree()
    for value in (4, 2, 6, 1):
        tree.insert(value)
    assert preorder(tree.root) == [4, 2, 1, 6]
    assert level_order(tree.root) == [4, 2, 6, 1]
    return [
        shot("Preorder", "Preorder visits 4, then 2, then 1, then 6.", [("first", "4")], [4, 2, 1, 6], "chosen"),
        shot("Level", "Level order is 4, then 2, then 6, then 1.", [("queue", "4")], [4, 2, 6, 1], "active"),
        shot("Child", "1 hangs under 2, so it waits behind 6.", [("node", "1")], [2, 6, 1], "done"),
    ]


def _balanced() -> list[dict[str, object]]:
    tree = LeftLeaningRedBlackTree()
    frames = []
    for value in (1, 2, 3):
        tree.insert(value)
        root = tree.root.key if tree.root is not None else None
        text = f"After inserting {value}, the root is {root}. Inorder is {tree.inorder()}."
        frames.append(shot("Insert", text, [("root", str(root))], list(tree.inorder()), "chosen"))
    assert tree.root is not None and tree.root.key == 2
    return frames


def _priority() -> list[dict[str, object]]:
    queue = PriorityQueue[str]()
    frames = []
    for priority, item in ((5, "a"), (3, "b"), (4, "c")):
        queue.push(priority, item)
        text = f"Push priority {priority} for item {item}."
        frames.append(shot("Push", text, [("priority", str(priority))], [priority], "active"))
    assert queue.pop() == (3, "b")
    frames.append(shot("Pop", "The first pop returns priority 3 and item b.", [("item", "b")], [3, "b"], "chosen"))
    return frames


def _graph_store() -> list[dict[str, object]]:
    graph = Graph()
    frames = []
    pairs = 0
    for source, target in (("A", "B"), ("A", "C"), ("B", "D")):
        graph.add_edge(source, target, 1)
        pairs += 1
        text = f"Add {source} to {target}. The list now stores {pairs} neighbor pairs."
        frames.append(shot("Edge", text, [("edges", str(pairs))], [source, target], "active"))
    assert sum(len(graph.neighbors(vertex)) for vertex in graph.vertices()) == 3
    return frames


def _topo() -> list[dict[str, object]]:
    events, sink = _listen()
    graph = Graph()
    for source, target in (("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")):
        graph.add_edge(source, target, 1)
    assert topological_order(graph, trace_sink=sink) == ["A", "B", "C", "D"]
    frames = []
    for event in events:
        text = f"Emit {event.values['vertex']}. The order so far is {event.values['order']}."
        frames.append(shot("Emit", text, [("vertex", str(event.values["vertex"]))], list(event.values["order"]), "done"))
    return frames


def _shortest() -> list[dict[str, object]]:
    events, sink = _listen()
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 4)
    graph.add_edge("B", "C", 2)
    assert dijkstra_distances_heap(graph, "A", trace_sink=sink)["C"] == 3
    frames = []
    for event in events:
        text = f"Settle {event.values['vertex']} at distance {event.values['distance']}."
        frames.append(shot("Settle", text, [("distance", str(event.values["distance"]))], [event.values["vertex"], event.values["distance"]], "chosen"))
    return frames


def _mst() -> list[dict[str, object]]:
    events, sink = _listen()
    graph = UndirectedGraph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 4)
    assert kruskal_minimum_spanning_weight(graph, trace_sink=sink) == 3
    assert prim_minimum_spanning_weight(graph, "A") == 3
    frames = []
    for event in events:
        text = f"{event.kind.capitalize()} weight {event.values['weight']}. The total is {event.values['total']}."
        frames.append(shot(event.kind, text, [("total", str(event.values["total"]))], [event.values["weight"], event.values["total"]], "chosen"))
    return frames


def _two() -> list[dict[str, object]]:
    events, sink = _listen()
    assert two_sum_sorted([1, 2, 4, 7], 6, trace_sink=sink) == (1, 2)
    frames = []
    for event in events:
        text = f"Indexes {event.values['left']} and {event.values['right']} sum to {event.values['total']}."
        frames.append(shot("Move", text, [("sum", str(event.values["total"]))], [event.values["left"], event.values["right"], event.values["total"]]))
    return frames


def _window() -> list[dict[str, object]]:
    events, sink = _listen()
    assert sliding_window_maximum([1, 3, 2, 5], 2, trace_sink=sink) == [3, 3, 5]
    frames = []
    for event in events:
        text = f"The window ending at index {event.values['index']} has maximum {event.values['maximum']}."
        frames.append(shot("Window", text, [("max", str(event.values["maximum"]))], list(event.values["output"]), "chosen"))
    return frames


def _prefix() -> list[dict[str, object]]:
    totals = PrefixSum([1, 2, 3, 4])
    frames = []
    for end, expected in ((1, 1), (2, 3), (4, 10)):
        found = totals.range_sum(0, end)
        assert found == expected
        text = f"range_sum from 0 to {end} returns {found}."
        frames.append(shot("Prefix", text, [("sum", str(found))], [found], "chosen"))
    assert totals.range_sum(1, 3) == 5
    frames.append(shot("Slice", "range_sum from 1 to 3 returns 5, which is 2 + 3.", [("sum", "5")], [5], "done"))
    return frames


def _backtrack() -> list[dict[str, object]]:
    events, sink = _listen()
    assert len(permutations([1, 2, 3], trace_sink=sink)) == 6
    frames = []
    for event in events:
        text = f"Leaf {event.values['count']} is {event.values['path']}."
        frames.append(shot("Leaf", text, [("count", str(event.values["count"]))], list(event.values["path"]), "done"))
    return frames


def _greedy() -> list[dict[str, object]]:
    events, sink = _listen()
    count = interval_scheduling_max_count([(1, 3, "a"), (2, 4, "b"), (3, 5, "c")], trace_sink=sink)
    assert count == 2
    frames = []
    for event in events:
        text = f"{event.kind.capitalize()} interval {event.values['label']}. The count is {event.values['count']}."
        frames.append(shot(event.kind, text, [("count", str(event.values["count"]))], [event.values["label"], event.values["count"]], "chosen"))
    return frames


def _coins() -> list[dict[str, object]]:
    events, sink = _listen()
    assert min_coin_change([1, 3, 4], 6, trace_sink=sink) == 2
    frames = []
    for event in events:
        if int(event.values["value"]) not in (2, 4, 6):
            continue
        text = f"Amount {event.values['value']} takes {event.values['coins']} coins."
        frames.append(shot("Amount", text, [("coins", str(event.values["coins"]))], [event.values["value"], event.values["coins"]], "chosen"))
    return frames


def _kmp() -> list[dict[str, object]]:
    events, sink = _listen()
    assert kmp_search("ababcababa", "ababa", trace_sink=sink) == 5
    frames = []
    for event in events:
        if int(event.values["index"]) not in (0, 4, 5, 9):
            continue
        text = f"At text index {event.values['index']} the pattern state is {event.values['state']}."
        frames.append(shot("Scan", text, [("state", str(event.values["state"]))], [event.values["index"], event.values["state"]]))
    return frames


def _trie() -> list[dict[str, object]]:
    trie = Trie()
    trie.insert("cat")
    frames = [shot("Insert", "Insert cat. contains cat is true.", [("key", "cat")], ["c", "a", "t"], "chosen")]
    trie.insert("car")
    assert trie.contains("car") is True
    frames.append(shot("Insert", "Insert car. contains car is true.", [("key", "car")], ["c", "a", "r"], "active"))
    assert trie.contains("ca") is False
    frames.append(shot("Miss", "contains ca is false. A prefix is not a stored key.", [("key", "ca")], ["c", "a"], "done"))
    return frames


def _fenwick() -> list[dict[str, object]]:
    tree = FenwickTree(4)
    frames = []
    running = 0
    for index, value in ((0, 1), (1, 2), (2, 3)):
        tree.add(index, value)
        running += value
        assert tree.prefix_sum(index) == running
        text = f"Add {value} at index {index}. The prefix through that index is {running}."
        frames.append(shot("Add", text, [("sum", str(running))], [running], "chosen"))
    assert tree.prefix_sum(2) == 6
    return frames


def _bloom() -> list[dict[str, object]]:
    bloom = BloomFilter(bit_count=64, hash_count=3, seed=0)
    bloom.add("cat")
    assert bloom.maybe_contains("cat") is True
    return [
        shot("Add", "add cat sets the three bits that hash names.", [("key", "cat")], ["cat"], "chosen"),
        shot("Hit", "maybe_contains cat is true. Every required bit is set.", [("hit", "true")], ["cat"], "active"),
        shot("Bits", "A clear bit would be a definite miss. This query has none.", [("bits", "3")], [64, 3], "done"),
    ]


def _storage() -> list[dict[str, object]]:
    frames = []
    for values, expected in (([1], 1), ([1, 2], 3), ([1, 2, 3], 6)):
        assert sequential_scan_sum(values) == expected
        text = f"sequential_scan_sum of {values} returns {expected}."
        frames.append(shot("Scan", text, [("sum", str(expected))], list(values), "done"))
    return frames


def _cover() -> list[dict[str, object]]:
    events, sink = _listen()
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("C", "D", 1)
    cover = vertex_cover_two_approximation(graph, trace_sink=sink)
    assert sorted(cover) == ["A", "B", "C", "D"]
    frames = []
    for event in events:
        if event.kind == "start":
            text = "The cover starts empty. No edge has been scanned."
            values: list[object] = []
        else:
            text = f"The edge {event.values['source']} to {event.values['target']} adds both ends."
            values = list(event.values["cover"])
        frames.append(shot(event.kind, text or "Scan.", [("cover", str(values))], values or ["-"], "chosen"))
    return frames


def _answer_search() -> list[dict[str, object]]:
    piles = [3, 6, 7, 11]
    tested: list[int] = []

    def feasible(rate: int) -> bool:
        tested.append(rate)
        return sum((pile + rate - 1) // rate for pile in piles) <= 8

    assert binary_search_on_answer(1, max(piles), feasible) == 4
    assert tested == [6, 3, 4]
    events, sink = _listen()
    tested.clear()

    def feasible_again(rate: int) -> bool:
        return sum((pile + rate - 1) // rate for pile in piles) <= 8

    assert binary_search_on_answer(1, max(piles), feasible_again, trace_sink=sink) == 4
    frames = []
    for event in events:
        text = f"Test rate {event.values['middle']}. Feasible is {event.values['feasible']}."
        frames.append(shot("Test", text, [("rate", str(event.values["middle"]))], [event.values["low"], event.values["middle"], event.values["high"]], "chosen"))
    frames.append(shot("Answer", "The smallest feasible rate is 4.", [("rate", "4")], [4], "done"))
    return frames


_BUILDERS = {
    "input-size-and-operation-counts": _input_size,
    "asymptotic-growth": _growth,
    "cost-models": lambda: _pop_front("cost-models"),
    "loop-invariants": lambda: _insertion("loop-invariants"),
    "arrays-and-python-costs": lambda: _pop_front("arrays"),
    "dynamic-array-growth": _dynamic_array,
    "recursion-and-recurrences": _recursion,
    "singly-linked-list": _linked,
    "stack-basics": _stack,
    "queue-and-deque-operations": _queue,
    "comparison-sorts": lambda: _insertion("comparison-sorts"),
    "merge-sort": _merge,
    "quicksort-and-partition": _quick,
    "hash-chaining": _chain,
    "binary-search-tree-operations": _bst,
    "heap-operations": _heap,
    "graph-traversals": _graph_walk,
    "union-find": _union,
    "dynamic-programming": _fibonacci,
    "fast-slow-pointer-patterns": _fast_slow,
    "linked-list-reversal-and-relinking": _reverse,
    "linked-list-merge-and-sort": _merge_lists,
    "linked-list-special-cases": _nth,
    "doubly-linked-list-operations": _doubly,
    "monotonic-stack-patterns": _greater,
    "stack-parsing-and-expressions": _parsing,
    "noncomparison-sorts": _counting,
    "order-statistic-selection": _select,
    "inversion-counting": _inversions,
    "hash-linear-probing": _probe,
    "lru-cache": _lru,
    "tree-traversals": _walks,
    "balanced-search-trees": _balanced,
    "priority-queues": _priority,
    "graph-representations": _graph_store,
    "topological-order": _topo,
    "shortest-paths": _shortest,
    "minimum-spanning-trees": _mst,
    "two-pointers": _two,
    "sliding-window": _window,
    "prefix-sums": _prefix,
    "backtracking": _backtrack,
    "greedy-methods": _greedy,
    "dp-state-and-transition": _coins,
    "string-search": _kmp,
    "tries-and-text-indexes": _trie,
    "range-query-structures": _fenwick,
    "approximate-membership": _bloom,
    "storage-engines-and-locality": _storage,
    "approximation-guarantees": _cover,
    "binary-search-on-answer": _answer_search,
}
