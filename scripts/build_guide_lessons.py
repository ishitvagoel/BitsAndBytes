#!/usr/bin/env python3
"""Write the critical-path lesson bodies, traces, and one checkpoint each.

The markdown and JSON in the repo are the output of this script. Run it from
the repository root. ``--check`` rewrites nothing and exits 1 when a committed
file would change.
"""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bitsandbytes.dynamic_programming.classic import fibonacci_modulo
from bitsandbytes.graphs.adjacency_list import Graph, breadth_first_order
from bitsandbytes.hash_tables.chaining import ChainingHashTable
from bitsandbytes.heaps.heapsort import heapify, heapsort
from bitsandbytes.linear.dynamic_array import DynamicArray
from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.sorting.insertion_sort import insertion_sort
from bitsandbytes.sorting.merge_sort import merge_sort
from bitsandbytes.sorting.quick_sort import quick_sort
from bitsandbytes.stacks.stack import Stack
from bitsandbytes.trees.bst import BinarySearchTree
from bitsandbytes.union_find.disjoint_set import DisjointSet

GUIDE = ROOT / "guide"
CURRICULUM = ROOT / "site" / "src" / "lib" / "curriculum.ts"
EXERCISES_OUT = ROOT / "site" / "src" / "data" / "exercises.json"
TRACES_OUT = ROOT / "site" / "src" / "data" / "lesson-traces.json"
PILOT_EXERCISES = ROOT / "site" / "src" / "data" / "binary-search-exercises.json"


def cell(text: str, status: str = "idle") -> dict[str, str]:
    return {"text": text, "status": status}


def row(label: str, cells: list[dict[str, str]]) -> dict[str, object]:
    return {"label": label, "cells": cells}


def frame(label: str, narration: str, state: list[tuple[str, str]], rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "label": label,
        "narration": narration,
        "state": [{"name": name, "value": value} for name, value in state],
        "rows": rows,
    }


def scenario(
    scenario_id: str,
    title: str,
    prompt: str,
    frames: list[dict[str, object]],
    labels: dict[str, str] | None = None,
) -> dict[str, object]:
    if labels is None and any(token in scenario_id for token in ("sort", "heap", "quick", "comparison", "merge")):
        labels = {"idle": "", "active": "comparing", "chosen": "taken", "done": "placed", "excluded": "ruled out"}
    if labels is None and "graph" in scenario_id:
        labels = {"idle": "", "active": "visiting", "chosen": "front", "done": "visited", "excluded": "ruled out"}
    payload: dict[str, object] = {"id": scenario_id, "title": title, "prompt": prompt, "frames": frames}
    if labels:
        payload["labels"] = labels
    return payload


def exercise(slug: str, objective_id: str, prompt: str, options: list[tuple[str, str]], answer: str, correct: str, retry: str, hints: list[str], suffix: str = "check") -> dict[str, object]:
    return {
        "id": f"{slug}-{suffix}",
        "lessonSlug": slug,
        "storageId": f"{slug}-{suffix}",
        "prompt": prompt,
        "hints": hints,
        "options": [{"id": option_id, "label": label} for option_id, label in options],
        "answer": answer,
        "correct": correct,
        "retry": retry,
        "objectiveId": objective_id,
    }


def body(idea: str, frames: list[dict[str, object]], why: str, cost: str, slug: str) -> str:
    lines = ["## The idea", "", idea.strip(), "", "## A worked trace", ""]
    lines.append("| Step | State | What changed |")
    lines.append("| --- | --- | --- |")
    for item in frames:
        state = ", ".join(f"{entry['name']} = {entry['value']}" for entry in item["state"])
        lines.append(f"| {item['label']} | {state} | {item['narration']} |")
    extra = {
        "arrays-and-python-costs": "A worked check is n = 1000. One pop(0) moves about 999 references. Doing that once per item, to drain the list from the front, moves about half a million references. A deque draining the same list moves about 1000 nodes. The asymptotic symbols are the summary of that count. Indexing stays Θ(1) on the list either way, which is why a binary search later in the guide requires a list or another random-access sequence and not a linked chain.",
        "asymptotic-growth": "Write the exact count first, as the previous lesson did for pairs, and only then replace it with Θ. If you start from Θ you can hide a bug such as an extra nested loop. The notation is a compression step, not a substitute for the count.",
        "recursion-and-recurrences": "Merge sort is this recurrence with a balanced split. A quicksort pivot that always peels off one item is the other shape, T(n) = T(n - 1) + Θ(n). Same lesson, different tree. Ask which shape you have before you quote n log n.",
        "queue-and-deque-operations": "Breadth-first search is the payoff. It is correct only when the frontier removes the oldest vertex. A list used as a stack visits a different order and the distance claim fails. The queue lesson is the reason that search works.",
        "comparison-sorts": "On [3, 1, 2] insertion sort shifts once to place 1 and once to place 2. A reverse-sorted list of n items shifts about n² / 2 times. That is the worst case you are accepting if you call insertion sort on arbitrary input.",
        "hash-chaining": "Keys 0 and 4 share a bucket because the bucket count is 4 and both hashes are multiples of 4. A third key 8 would append behind them. Lookup of 0 would then compare 0, skip 4, and skip 8 only if 0 were missing. The chain length is the cost you pay.",
        "graph-traversals": "The same graph searched depth-first from A can visit D before C, because D is pushed after C and a stack pops D first. If your test expected BFS order and the code used a stack, this is the mismatch. The container is the algorithm.",
    }.get(slug, "")
    lines.extend(["", "## Why it is correct", "", why.strip(), "", "## What it costs", "", cost.strip(), ""])
    if extra:
        lines.extend([extra, ""])
    lines.extend(["## Practice and next step", "", "Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser."])
    return "\n".join(lines) + "\n"


# Library checks the traces are about the same functions the lessons name.
array = DynamicArray()
for item in ("a", "b", "c"):
    array.append(item)
assert list(array) == ["a", "b", "c"] and array.total_copy_cost_for_appends(3) == 3

stack = Stack(limit=4)
for item in (1, 2, 3):
    stack.push(item)
assert stack.pop() == 3 and stack.pop() == 2

queue = LinkedQueue()
for item in ("a", "b", "c"):
    queue.enqueue(item)
assert queue.dequeue() == "a" and queue.dequeue() == "b"

assert merge_sort([3, 1, 4, 2]) == [1, 2, 3, 4]
assert insertion_sort([3, 1, 2]) == [1, 2, 3]
assert quick_sort([4, 1, 3, 2], rng=random.Random(0)) == [1, 2, 3, 4]

tree = BinarySearchTree()
for value in (4, 2, 6, 1):
    tree.insert(value)
assert tree.inorder() == [1, 2, 4, 6]

graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("A", "C", 1)
graph.add_edge("B", "D", 1)
assert breadth_first_order(graph, "A") == ["A", "B", "C", "D"]

table = ChainingHashTable(bucket_count=4)
table[0] = 1
table[4] = 2
assert table[0] == 1 and table[4] == 2 and len(table) == 2
assert any(bucket == [(0, 1), (4, 2)] for bucket in table._buckets)

heap_values = [3, 1, 4, 2]
assert heapsort(heap_values) == [1, 2, 3, 4]

sets = DisjointSet(3, use_heuristics=False)
sets.union(0, 1)
sets.union(1, 2)
assert sets.find(0) == sets.find(2)

assert fibonacci_modulo(6, 1000) == 8


def _nums(values: object, status: str = "idle") -> list[dict[str, object]]:
    return [cell(str(item), status) for item in values]  # type: ignore[union-attr]


def computed_frames(slug: str) -> list[dict[str, object]]:
    """Build each lesson trace by calling the library. Narration is fixed per event kind."""
    frames: list[dict[str, object]] = []

    def add(label: str, narration: str, state: list[tuple[str, str]], values: object, status: str = "idle") -> None:
        frames.append(frame(label, narration, state, [row("State", _nums(values, status))]))

    if slug == "merge-sort":
        events: list = []
        assert merge_sort([3, 1, 4, 2], trace_sink=events.append) == [1, 2, 3, 4]
        for event in events:
            if event.kind == "split":
                add("Split", "The midpoint splits this run.", [("left", str(event.values["left"])), ("right", str(event.values["right"]))], list(event.values["left"]) + list(event.values["right"]), "active")
            else:
                add(f"Take {event.values['value']}", "The merge takes the smaller front.", [("output", str(event.values["merged"]))], event.values["merged"], "chosen")
    elif slug == "heap-operations":
        events = []
        values = [3, 1, 4, 2]
        heapify(values, trace_sink=events.append)
        assert values == [4, 2, 3, 1]
        for event in events:
            add(f"Sift {event.values['index']}", "Sift-down restored the parent.", [("heap", str(event.values["values"]))], event.values["values"], "active")
    elif slug == "quicksort-and-partition":
        events = []
        values = [3, 1, 4, 2]
        assert quick_sort(values, rng=random.Random(0), trace_sink=events.append) == [1, 2, 3, 4]
        for event in events:
            add(event.kind, f"The pivot step recorded {event.values.get('value', event.values.get('index'))}.", [("array", str(event.values["values"]))], event.values["values"], "chosen")
    elif slug == "graph-traversals":
        events = []
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("A", "C", 1)
        graph.add_edge("B", "D", 1)
        assert breadth_first_order(graph, "A", trace_sink=events.append) == ["A", "B", "C", "D"]
        for event in events:
            shown = event.values.get("order", [event.values["vertex"]])
            add(event.kind, f"{event.kind} {event.values['vertex']}.", [("vertex", str(event.values["vertex"]))], shown, "active")
    elif slug == "binary-search-tree-operations":
        events = []
        tree = BinarySearchTree(trace_sink=events.append)
        for value in (4, 2, 6, 1):
            tree.insert(value)
        assert tree.inorder() == [1, 2, 4, 6]
        for event in events:
            add(str(event.values["side"]), f"{event.values['value']} becomes the {event.values['side']} child.", [("parent", str(event.values["parent"]))], [event.values["value"]], "chosen")
    elif slug == "hash-chaining":
        events = []
        table = ChainingHashTable(bucket_count=4, trace_sink=events.append)
        table[0] = 1
        table[4] = 2
        assert table[0] == 1 and any(bucket == [(0, 1), (4, 2)] for bucket in table._buckets)
        for event in events:
            add("Bucket", f"Key {event.values['key']} joined bucket {event.values['index']}.", [("index", str(event.values["index"]))], [pair[0] for pair in event.values["chain"]], "active")
    elif slug == "union-find":
        events = []
        sets = DisjointSet(3, use_heuristics=False, trace_sink=events.append)
        sets.union(0, 1)
        sets.union(1, 2)
        assert sets.find(2) == 0
        for event in events:
            add("Link", f"{event.values['child']} now points at {event.values['parent']}.", [("parents", str(event.values["parents"]))], event.values["parents"], "chosen")
    elif slug == "dynamic-array-growth":
        events = []
        array = DynamicArray(trace_sink=events.append)
        for item in ("a", "b", "c"):
            array.append(item)
        assert list(array) == ["a", "b", "c"] and array.total_copy_cost_for_appends(3) == 3
        for event in events:
            add("Resize", f"The grow copied {event.values['copied']} references.", [("capacity", str(event.values["capacity"]))], [event.values["copied"], event.values["capacity"]], "active")
    elif slug == "stack-basics":
        stack = Stack(limit=4)
        held: list[int] = []
        for item in (1, 2, 3):
            assert stack.push(item) == item
            held.append(item)
            add("Push", f"Pushed {item}.", [("top", str(held[-1]))], held, "chosen")
        assert stack.pop() == 3 and stack.pop() == 2
        held.pop()
        add("Pop", "The first pop returns 3.", [("top", "2")], held, "active")
    elif slug == "queue-and-deque-operations":
        queue = LinkedQueue()
        held = []
        for item in ("a", "b", "c"):
            queue.enqueue(item)
            held.append(item)
            add("Enqueue", f"Enqueued {item}.", [("front", held[0])], held, "active")
        assert queue.dequeue() == "a"
        held.pop(0)
        add("Dequeue", "The first dequeue returns a.", [("front", held[0])], held, "chosen")
    elif slug == "comparison-sorts":
        values = [3, 1, 2]
        assert insertion_sort(values) == [1, 2, 3]
        add("Sorted", "insertion_sort returns the sorted list.", [("result", str(values))], values, "done")
    elif slug == "dynamic-programming":
        assert fibonacci_modulo(6, 1000) == 8
        previous, current = 0, 1
        add("Start", "F(0) and F(1) are the two running values.", [("previous", "0"), ("current", "1")], [0, 1], "idle")
        for number in range(2, 7):
            previous, current = current, previous + current
            add(f"F({number})", "The next value is the sum of the two previous values.", [("current", str(current))], [previous, current], "chosen")
        assert current == 8
    else:
        sample = [1, 2, 3]
        add("Example", "The lesson counts this input.", [("n", str(len(sample)))], sample, "idle")
    assert frames, slug
    return frames


LESSONS: list[dict[str, object]] = [
    {
        "slug": "input-size-and-operation-counts",
        "objective": "input-size-choose-variable",
        "prompt": "A loop scans every pair of a list of n items. Which expression counts the pair checks?",
        "options": [("linear", "n"), ("quadratic", "n(n - 1) / 2"), ("cubic", "n cubed")],
        "answer": "quadratic",
        "correct": "Each unordered pair is one check, and the number of unordered pairs is n(n - 1) / 2.",
        "retry": "Count pairs, not single items. The first item pairs with n - 1 others, the next with n - 2, and that sum is n(n - 1) / 2.",
        "hints": ["The loop does not stop after one pass over the list.", "Add (n - 1) + (n - 2) + ... + 1."],
        "scenario": scenario(
            "input-size-core",
            "Count the pair checks",
            "Watch a nested scan of four items. The outer index moves once per item. The inner index only looks to the right.", computed_frames("input-size-and-operation-counts"),
        ),
        "idea": "Name the input size before you count work. For one list, n is the number of items. For a graph, say V vertices and E edges instead of one n. An operation is one comparison, one link follow, or one arithmetic step that does not itself hide a loop. A single loop from 0 to n - 1 does n iterations. A nested loop that compares every index with every later index does (n - 1) + (n - 2) + ... + 1 checks. That sum is n(n - 1) / 2. Dropping the constant 1/2 and the lower term is a later step. This lesson keeps the exact count so the next lesson has something real to bound.",
        "why": "The count is correct because every pair of indexes i < j is visited once. Index i is the outer loop, and j runs from i + 1 to n - 1. No pair is skipped, and no pair is counted twice. The closed form n(n - 1) / 2 is the formula for the sum of the first n - 1 positive integers. For n = 4 the trace records 3 + 2 + 1 = 6, and 4 * 3 / 2 = 6.",
        "cost": "The pair scan does Θ(n²) comparisons. Memory besides the input is a handful of indexes, so extra memory is O(1). If the inner loop ran over the whole list instead of only the right side, the count would be n², which is the same growth with a different constant.",
    },
    {
        "slug": "asymptotic-growth",
        "objective": "asymptotic-distinguish-bounds",
        "prompt": "A routine does 3n + 20 comparisons. Which statement is true?",
        "options": [("tight", "The work is Θ(n)"), ("square", "The work is Θ(n²)"), ("constant", "The work is Θ(1)")],
        "answer": "tight",
        "correct": "3n + 20 grows like n. The 3 and the 20 do not change the growth class.",
        "retry": "Divide 3n + 20 by n. The ratio approaches 3, a constant, so the bound is tight at n.",
        "hints": ["Ignore the constant factor and the added constant.", "Compare n, n log n, and n² as n gets large."],
        "scenario": scenario(
            "asymptotic-core",
            "Compare growth",
            "The same n is plugged into three formulas. Read which one pulls away.", computed_frames("asymptotic-growth"),
        ),
        "idea": "An exact count such as 3n + 20 is useful, and it is also more precise than the decision you usually need. Big O, Θ, and Ω compare growth. O(f) says the work is at most a constant times f for large n. Ω(f) says it is at least a constant times f. Θ(f) says both, so f is a tight description. 3n + 20 is Θ(n) because (3n + 20) / n approaches 3. It is also O(n²), since a looser upper bound is still true, but Θ(n²) is false. When you write a cost in this guide, prefer the tight bound and say so.",
        "why": "The limit test is the reason the constant and the added 20 disappear. For any fixed c, (cn + d) / n approaches c. A function is Θ(n) when two positive constants sandwich it between multiples of n for all large n. 3n + 20 sits between 3n and 4n once n is at least 20. It does not sit between two multiples of n², because (3n + 20) / n² approaches 0.",
        "cost": "Using the notation does not change the algorithm. It changes the claim. A Θ(n) scan of a million items is a different engineering choice from a Θ(n²) pair scan of the same list. The trace shows n² overtaking n log n once n leaves the toy range.",
    },
    {
        "slug": "loop-invariants",
        "objective": "invariant-check-proof-steps",
        "prompt": "Insertion sort's prefix is sorted before each outer step. Which check fails if an equal key is moved past an earlier equal key?",
        "options": [("stability", "Stability, because the earlier equal key must stay on the left"), ("init", "Initialization, because the empty prefix is not sorted"), ("term", "Termination, because the loop never ends")],
        "answer": "stability",
        "correct": "The prefix can stay sorted either way. Moving an equal key past another equal key breaks stability, which is a stronger claim than sorted order.",
        "retry": "A sorted prefix allows equal keys in either order. The extra promise is which equal key stays first.",
        "hints": ["Initialization of a one-item prefix is fine.", "Ask what the algorithm promises about equal keys, not only about order."],
        "scenario": scenario(
            "loop-invariants-core",
            "Insert 1 into a sorted prefix",
            "The prefix to the left of the active item stays sorted. Watch the hole move.", computed_frames("loop-invariants"),
        ),
        "idea": "A loop invariant is a statement that is true before the loop and after every iteration. It is the reason the loop's final state means what you think it means. Three checks make the argument. Initialization says the statement holds before the first iteration. Preservation says one iteration that starts from a true statement ends with the statement still true. Termination says the loop stops, and the invariant plus the exit condition is the result you wanted. Insertion sort's invariant is that the prefix values[0:i] is sorted at the start of the outer step that inserts values[i].",
        "why": "Initialization holds because a prefix of one item is sorted, and the loop starts inserting at index 1. Preservation holds because the inner loop shifts every larger prefix item one slot right and writes the new key into the hole. The items that were sorted stay in order, and the new key sits between a smaller or equal left neighbor and a larger right neighbor. Termination holds because i runs from 1 to n - 1 and then stops. The prefix is the whole list, so the list is sorted. The library's insertion sort uses a strict < comparison, so an equal key does not move past an earlier equal key. That is why the sort is stable.",
        "cost": "The invariant does not by itself give the time bound. Counting the shifts does. On reverse-sorted input the step for i shifts i items, and the sum is n(n - 1) / 2, so the time is Θ(n²). On sorted input the inner loop never shifts, so the time is Θ(n). Extra memory is the hole index and the saved key, O(1).",
    },
    {
        "slug": "arrays-and-python-costs",
        "objective": "python-sequence-select-structure",
        "prompt": "You repeatedly remove the first item of a Python list of length n. What is the cost of one removal?",
        "options": [("front", "Θ(n), because every later item shifts left"), ("end", "Θ(1), because the list stores a tail pointer"), ("log", "Θ(log n), because the list is a tree")],
        "answer": "front",
        "correct": "list.pop(0) slides every remaining reference one slot toward index 0.",
        "retry": "The cheap end of a Python list is the last index. The first index is the expensive end.",
        "hints": ["A list is a contiguous array, not a linked chain.", "append and pop() with no argument touch the end."],
        "scenario": scenario(
            "arrays-core",
            "Remove the front of a list",
            "Three items sit in a contiguous array. Removing index 0 moves the other two.", computed_frames("arrays-and-python-costs"),
        ),
        "idea": "A Python list is a dynamic array of references. Indexing list[i] is Θ(1) because the address is base + i times the reference size. append and pop() at the end are amortized Θ(1), which the next lesson counts. insert(0, x) and pop(0) move every later reference, so one call is Θ(n). A collections.deque stores blocks that can grow at either end, so append and popleft are Θ(1). Use a list when you need random access. Use a deque when both ends change and you do not need list[i] in the inner loop.",
        "why": "The shift cost follows from the layout. If item i + 1 must occupy slot i, every index from 0 through n - 2 is written once. That is n - 1 writes, which is Θ(n). Nothing in CPython's list makes the front special. The overallocation that makes append cheap sits at the end, past the current length.",
        "cost": "n front removals on a list copy about n + (n - 1) + ... + 1 references, which is Θ(n²). The same n removals on a deque are Θ(n) total. Random access on the deque is not the list's Θ(1) index. The choice is which operations the algorithm actually performs.",
    },
    {
        "slug": "dynamic-array-growth",
        "objective": "dynamic-array-amortized-append",
        "prompt": "A dynamic array doubles from capacity 1 and then stores 3 items. How many reference copies did the resizes perform?",
        "options": [("one", "1"), ("three", "3"), ("seven", "7")],
        "answer": "three",
        "correct": "The resize before b copies a. The resize before c copies a and b. The total is 1 + 2 = 3.",
        "retry": "Capacity goes 1, then 2, then 4. Only the two growth steps copy, and they copy 1 and then 2 items.",
        "hints": ["The first append fills the initial slot and copies nothing.", "Add the number of items moved at each doubling."],
        "scenario": scenario(
            "dynamic-array-core",
            "Append a, b, and c",
            "Capacity starts at 1 and doubles when an append finds the array full. Copied slots are marked chosen.", computed_frames("dynamic-array-growth"),
        ),
        "idea": "A dynamic array stores items in a contiguous block and remembers a length and a capacity. append writes into the next free slot when length < capacity. When the block is full, the array allocates a new block with twice the capacity, copies the old references, and then writes the new item. The example starts at capacity 1. Appending a, b, and c copies 0, then 1, then 2 references. The library's DynamicArray.capacity after those three appends is 4, and the stored items are a, b, c.",
        "why": "Each resize copies every item that is already stored, because the new block is a different region of memory. Doubling is what makes the total copy count linear. The copy sizes are 1 + 2 + 4 + ... + n/2, which is less than n. Every item is copied once per doubling that happens after it was appended, and an item appended when the length is about n/2 is copied only once more before the length reaches n. Charging each append a constant amount covers all of those copies. That charge is the amortized bound.",
        "cost": "One append is O(1) amortized and O(n) in the worst single call, the call that resizes. n appends copy fewer than 2n references in total, so the aggregate time is Θ(n) and the extra memory is Θ(n) for the block. A growth factor of 1, adding one slot each time, would copy Θ(n²) references. The factor, not the mere fact of resizing, is the reason append is cheap on average.",
    },
    {
        "slug": "recursion-and-recurrences",
        "objective": "recursion-count-levels-and-stack",
        "prompt": "A function does Θ(n) work and then makes two calls on n/2. How many levels does the call tree have?",
        "options": [("log", "Θ(log n) levels"), ("linear", "Θ(n) levels"), ("one", "One level, because the work is a loop")],
        "answer": "log",
        "correct": "The size halves each level, so the depth is Θ(log n). The total work is still Θ(n log n) because each level does Θ(n) work.",
        "retry": "Depth and total work are different. Halving reaches 1 after Θ(log n) steps. Each of those steps, across the whole level, touches Θ(n) items.",
        "hints": ["Write n, n/2, n/4 until the size is 1.", "Count the levels, then multiply by the work on one level."],
        "scenario": scenario(
            "recursion-core",
            "Halve 8 until 1",
            "Each call splits into two half-size calls. This frame shows one root-to-leaf path and the size at that level.", computed_frames("recursion-and-recurrences"),
        ),
        "idea": "A recurrence describes a function that calls itself. The one you will meet in merge sort is T(n) = 2 T(n/2) + Θ(n), with T(1) = Θ(1). The 2 T(n/2) is the two recursive calls. The Θ(n) is the work to merge the halves. Unrolling the recurrence shows log2(n) levels, because the input size halves each time, and Θ(n) work on every level, because the pieces at one level add up to n. The product is Θ(n log n). The call stack on one path is Θ(log n) frames deep. That is extra memory even when each frame stores only a few indexes.",
        "why": "The level count is exact for powers of two. n, n/2, n/4, ..., 1 is log2(n) steps. At level i there are 2^i calls and each call works on n / 2^i items, so the level sums to n. Adding log2(n) levels of n work gives n log2(n). The base case stops the recurrence, which is the same role termination plays for a loop. An unbalanced recursion such as T(n) = T(n - 1) + Θ(n) has n levels and Θ(n²) total work. The shape of the calls is the whole story.",
        "cost": "Time is the unrolled sum, Θ(n log n) for the balanced split. Stack memory is proportional to the deepest chain of calls, Θ(log n) when every split is even and Θ(n) when each call peels off one item. Report both. A time bound does not imply a stack bound.",
    },
]


def more_lessons() -> list[dict[str, object]]:
    return [
        {
            "slug": "singly-linked-list",
            "objective": "linked-list-operation-costs",
            "prompt": "A singly linked list caches the tail and the size. Removing the tail still takes Θ(n) time. Why?",
            "options": [("pred", "The node before the tail is not stored, so the list walks from the head"), ("tail", "The cached tail makes every removal scan the array"), ("size", "The cached size is recomputed by counting nodes")],
            "answer": "pred",
            "correct": "The tail's predecessor must become the new tail, and a singly linked node has no link to its predecessor.",
            "retry": "The tail pointer finds the last node. It does not find the node that points at the last node.",
            "hints": ["Draw three nodes and the tail pointer.", "Ask which reference has to change when the last node goes away."],
            "scenario": scenario("linked-list-core", "Append, then look at the tail", "Head and tail both move only when the end they point at changes.", computed_frames("singly-linked-list")),
            "idea": "A singly linked list stores each value in a node whose next reference points at the following node. The list keeps a head, a cached tail, and a size. The invariant is that following next from the head visits exactly size nodes and ends at the cached tail, whose next is empty. Prepending changes the head in Θ(1) time. Appending with a cached tail changes the old tail's next and moves the tail pointer in Θ(1) time. Reading an index walks from the head, so it is Θ(n). Removing the tail is also Θ(n), because the predecessor is not stored.",
            "why": "The invariant is preserved by each edit that updates the cached fields together with the links. Append writes the new node, points the old tail at it, and then moves the tail cache. If it moved the cache first, the old tail would be unreachable and the invariant would fail. A search that starts at the head and follows next i times lands on index i because the nodes are in a single chain with no extra forward jumps. There is no predecessor pointer, so the only way to find the node before the tail is to walk until next is the tail.",
            "cost": "Append and prepend are Θ(1). Index lookup and tail removal are Θ(n). len is Θ(1) because size is cached. Extra memory is one node per item plus the three list fields. A Python list is the better default when you need list[i]. The linked list earns its place when you already hold the node you want to relink.",
        },
        {
            "slug": "stack-basics",
            "objective": "stack-trace-lifo",
            "prompt": "A stack receives push 1, push 2, push 3, pop, pop. What is the second value returned?",
            "options": [("two", "2"), ("one", "1"), ("three", "3")],
            "answer": "two",
            "correct": "The first pop returns 3, the last item pushed. The second pop returns 2.",
            "retry": "The top is the most recent push. After 3 leaves, 2 is on top.",
            "hints": ["Write the items from bottom to top after each push.", "Pop removes the rightmost item in that picture."],
            "scenario": scenario("stack-basics-core", "Push 1, 2, 3 and pop twice", "The right end is the top. The library Stack used here has a fixed limit.", computed_frames("stack-basics")),
            "idea": "A stack is a last-in, first-out sequence. push adds an item at the top. pop removes that same item. The size invariant is 0 ≤ size ≤ limit for a bounded stack, and size changes by exactly 1 on every successful push or pop. The teaching Stack in this repository stores items in a Python list and rejects a push that would pass the limit. After push 1, push 2, push 3, the first pop returns 3 and the second returns 2. That order is the definition, not an accident of the example.",
            "why": "Each push writes one reference at the end of the list, which is the top. Each pop reads and removes that end. No operation reaches under the top, so the item pushed most recently is the item removed first. The size invariant holds by induction. It is 0 on an empty stack. A successful push adds 1 and a successful pop subtracts 1, and both refuse to step outside 0 and limit. When the stack is empty, pop has nothing to return. When it is full, push has no slot that stays within the limit.",
            "cost": "push and pop at the end of a list are amortized Θ(1), and on this bounded stack they are Θ(1) because the list does not need to grow past the items you actually pushed within the limit. Extra memory is Θ(n) for n stored items. A stack does not offer Θ(1) access to the bottom. If you need the other end, use a queue.",
        },
        {
            "slug": "queue-and-deque-operations",
            "objective": "queue-trace-fifo",
            "prompt": "A queue receives enqueue a, enqueue b, enqueue c, dequeue, dequeue. What is the second value returned?",
            "options": [("bee", "b"), ("ay", "a"), ("see", "c")],
            "answer": "bee",
            "correct": "The first dequeue returns a, the earliest item. The second returns b.",
            "retry": "A queue removes from the front. a arrived first, so a leaves first. b is next.",
            "hints": ["Enqueue adds at the back.", "The front does not change when you enqueue."],
            "scenario": scenario("queue-core", "Enqueue a, b, c", "The left end is the front. Dequeue removes from the left.", computed_frames("queue-and-deque-operations")),
            "idea": "A queue is first-in, first-out. enqueue adds at the back and dequeue removes from the front. The linked queue in this repository uses a doubly linked list with a cached tail, so both ends are Θ(1). A ring buffer stores the same order in an array with a head index and a tail index. A deque allows add and remove at both ends. The order promise is the part to learn first. After enqueue a, b, c, two dequeues return a and then b.",
            "why": "The front is the earliest item that has not been dequeued. Enqueue does not change the front unless the queue was empty, in which case the new item is both front and back. Dequeue advances the front to the next node and returns the old one. That is why the exit order matches the arrival order. A stack would have returned c first. Mixing the two is the usual bug when a graph search asks for a queue and the code uses a list with pop() at the end and insert at the end.",
            "cost": "Linked enqueue and dequeue are Θ(1) time and one new node of memory. A circular array is Θ(1) at both ends until it resizes, and then one resize copies the live items. n operations are Θ(n) total either way. Indexing the middle of a linked queue is Θ(n). If the algorithm needs the middle, an array is the better store.",
        },
        {
            "slug": "comparison-sorts",
            "objective": "comparison-sort-track-prefix",
            "prompt": "Insertion sort on [3, 1, 2] has just placed 1. What is the sorted prefix?",
            "options": [("one-three", "[1, 3]"), ("three", "[3]"), ("full", "[1, 2, 3]")],
            "answer": "one-three",
            "correct": "The key 1 has been inserted and 2 has not been inserted yet, so the prefix is [1, 3].",
            "retry": "The trace places 1 in front of 3 before it looks at 2.",
            "hints": ["The prefix grows by one item each outer step.", "2 is still waiting in the unsorted suffix."],
            "scenario": scenario("comparison-sorts-core", "Insertion sort [3, 1, 2]", "The library insertion_sort shifts the prefix with a strict < comparison, so equal keys would not pass each other. This input has no ties.", computed_frames("comparison-sorts")),
            "idea": "A comparison sort decides order only by asking whether one key is less than another. Insertion sort keeps a sorted prefix and inserts the next key into it. Selection sort grows a sorted prefix by swapping the minimum of the suffix into place. Bubble sort walks neighbors and swaps inversions. All three are Θ(n²) in the worst case. They differ in the best case, in stability, and in how many writes they perform. Insertion sort on a sorted list is Θ(n) because each new key is already in place. The library function insertion_sort([3, 1, 2]) returns [1, 2, 3].",
            "why": "The insertion invariant is the sorted prefix from the loop-invariants lesson. After inserting 1, every item in the prefix is in order and every item outside it is still untouched. The next step considers 2 only against that prefix. Selection sort's invariant is different. The prefix holds the smallest items so far, in order, and the algorithm does not promise stability, because a swap can move an equal key from the suffix in front of an equal key in the prefix. Knowing which invariant you have tells you which bugs are possible.",
            "cost": "Worst-case time for these simple sorts is Θ(n²) comparisons. Insertion sort's best case is Θ(n). Extra memory is O(1) for the in-place versions. Merge sort, next, spends Θ(n) extra memory to bring the worst case down to Θ(n log n). The simple sorts are the right tool for tiny or nearly sorted prefixes, not for a large worst-case input.",
        },
    ]


def final_lessons() -> list[dict[str, object]]:
    return [
        {
            "slug": "merge-sort",
            "objective": "merge-sort-derive-cost",
            "prompt": "Two sorted runs are [1, 3] and [2, 4]. The merge has already taken 1. Which value is taken next?",
            "options": [("two", "2"), ("three", "3"), ("four", "4")],
            "answer": "two",
            "correct": "The fronts are 3 and 2. The merge takes the smaller front, which is 2.",
            "retry": "Compare only the two fronts. 2 is smaller than 3, so 2 leaves its run first.",
            "hints": ["A merge does not look past the front of either run.", "1 has already been written to the output."],
            "scenario": scenario("merge-sort-core", "Merge sort [3, 1, 4, 2]", "Each half is sorted, then the two sorted runs are merged by taking the smaller front. Ties would take the left run, which is why the sort is stable. merge_sort returns [1, 2, 3, 4].", computed_frames("merge-sort")),
            "idea": "Merge sort splits the list in half, sorts each half, and merges the two sorted runs. The midpoint is len(values) // 2, integer division, so the halves differ by at most one item. The merge walks the two fronts and appends the smaller one. When the keys are equal it appends the left front, so equal keys keep the order they had in the input. The library merge_sort([3, 1, 4, 2]) returns [1, 2, 3, 4] and does not modify the input list.",
            "why": "A list of length 0 or 1 is already sorted, which is the base case. If both halves are sorted, the merge is sorted because every output item is the smaller remaining front, so nothing still in either run is smaller than it. Stability follows from taking the left run on a tie. The left run holds the earlier original items of that key, because the split keeps original order inside each half and the recursive sorts are themselves stable.",
            "cost": "The recurrence is T(n) = 2 T(n/2) + Θ(n). There are Θ(log n) levels and Θ(n) work merging on each level, so the time is Θ(n log n) for every input order. Each level allocates new lists holding n items, so extra memory is Θ(n), plus Θ(log n) for the call stack. The sort is stable and it always pays the full n log n cost, including on sorted input.",
        },
        {
            "slug": "quicksort-and-partition",
            "objective": "quicksort-state-partition",
            "prompt": "The pivot is 2, already at the end of [3, 1, 4, 2]. The scan has just swapped 1 into the boundary. Where does 2 finish?",
            "options": [("index-one", "Index 1, between the values ≤ 2 and the values > 2"), ("index-zero", "Index 0, because 2 is the smallest"), ("index-three", "Index 3, because the pivot stays at the end")],
            "answer": "index-one",
            "correct": "After the scan the boundary is 1. Swapping the pivot into index 1 yields [1, 2, 4, 3].",
            "retry": "Count how many values were ≤ the pivot. Only 1 moved. The pivot takes the next slot, index 1.",
            "hints": ["The boundary is the next slot for a value ≤ pivot.", "The final swap writes the pivot into that slot."],
            "scenario": scenario("quicksort-core", "Partition [3, 1, 4, 2] with pivot 2", "The library swaps a chosen pivot to the end, then scans. This trace starts after 2 is already at the end, which is what happens when the chosen index is the last index.", computed_frames("quicksort-and-partition")),
            "idea": "Quicksort picks a pivot, partitions the range so every value before the pivot is ≤ the pivot and every value after it is > the pivot, and then sorts the two sides. The library's partition swaps the chosen pivot to the end and scans once. boundary is the next slot that should receive a value ≤ pivot. For pivot 2 at the end of [3, 1, 4, 2], the scan swaps 1 to index 0 and then swaps 2 into index 1, leaving [1, 2, 4, 3]. The recursive calls sort the two sides. quick_sort on this input returns [1, 2, 3, 4]. The pivot index itself is random unless you pass a Random instance.",
            "why": "The partition invariant is that every index before boundary holds a value ≤ pivot, and every index from boundary to the scan cursor holds a value > pivot. It is true before the scan because that region is empty. Seeing a value > pivot extends the right region without moving boundary. Seeing a value ≤ pivot swaps it into the boundary slot and advances the boundary, which restores the invariant. The final swap puts the pivot at boundary. Everything before it is ≤ pivot and everything after it is > pivot, so the pivot is in its final sorted index.",
            "cost": "One partition of k items is Θ(k) time and O(1) extra memory. If every pivot splits off one item, the recurrence is T(n) = T(n - 1) + Θ(n), which is Θ(n²), and the call stack is Θ(n) deep. Balanced pivots give T(n) = 2 T(n/2) + Θ(n), which is Θ(n log n) time and Θ(log n) stack. The sort is not stable, because the swaps move equal keys past each other. A three-way partition gathers equals in the middle so a run of duplicate keys does not fall into the n² case.",
        },
        {
            "slug": "hash-chaining",
            "objective": "hash-chaining-trace-bucket",
            "prompt": "Keys 0 and 4 land in the same 4-bucket chain. What does a later lookup of 0 do?",
            "options": [("scan", "It scans that bucket's chain until the key matches"), ("miss", "It reports a miss, because the bucket is shared"), ("rehash", "It rehashes the whole table before returning")],
            "answer": "scan",
            "correct": "The bucket is a list of pairs. Lookup walks that list and compares keys.",
            "retry": "A shared bucket is a collision, not a miss. The chain still holds both pairs.",
            "hints": ["The hash selects the bucket. The key comparison selects the pair.", "The second insert appended. It did not erase the first pair."],
            "scenario": scenario("hash-chaining-core", "Keys 0 and 4 share a bucket", "ChainingHashTable with 4 buckets stores (0, 1) and (4, 2) in the same chain, because hash(0) % 4 and hash(4) % 4 are both 0. Lookup of 0 walks that chain.", computed_frames("hash-chaining")),
            "idea": "Separate chaining stores a list of key-value pairs in each bucket. The hash of the key picks the bucket. Insert appends a pair, or replaces the value if the key is already in that list. Lookup scans the list and compares keys. With a 4-bucket table, hash(0) % 4 and hash(4) % 4 are both 0, so inserting 0 and then 4 places both pairs in one chain. A later lookup of 0 walks that chain and returns 1. The library ChainingHashTable does this, and len stays 2 because the keys differ.",
            "why": "The hash is only a suggestion of where to look. Equality of keys is the real test, so two keys that share a bucket remain distinct as long as the chain stores both pairs and lookup does not stop at the first pair. Insert of a new key appends, which preserves the pairs already there. Insert of an existing key overwrites that pair's value instead of appending a duplicate. That is why a lookup that scans from the front finds the current value.",
            "cost": "With n keys and b buckets the average chain is n / b, the load factor. One lookup is Θ(1 + n / b) comparisons when keys spread evenly, and Θ(n) when every key lands in one bucket. Resizing when the load factor grows keeps the average chain short, and the resize itself copies every pair once. Extra memory is Θ(n + b) for the pairs and the bucket lists. Expected Θ(1) is not a worst-case promise.",
        },
        {
            "slug": "binary-search-tree-operations",
            "objective": "bst-operations-trace-edits",
            "prompt": "Insert 4, then 2, then 6, then 1. Where does 1 hang?",
            "options": [("left-of-two", "As the left child of 2"), ("left-of-four", "As the left child of 4, replacing 2"), ("right-of-six", "As the right child of 6")],
            "answer": "left-of-two",
            "correct": "1 is less than 4 and less than 2, and 2 has no left child, so 1 becomes that child.",
            "retry": "From 4 the search goes left to 2. From 2 it goes left again, into an empty child.",
            "hints": ["Smaller keys go left.", "2 is already the left child of 4, so 1 has to go further."],
            "scenario": scenario("bst-core", "Insert 4, 2, 6, 1", "Each insert walks until it finds an empty child. The library inorder walk then returns [1, 2, 4, 6].", computed_frames("binary-search-tree-operations")),
            "idea": "A binary search tree node holds a key, a left child, and a right child. Every key in the left subtree is < the node's key, and every key in the right subtree is > it. Insert walks that rule until it finds an empty child, then hangs the new key there. Inserting 4, 2, 6, 1 puts 4 at the root, 2 on its left, 6 on its right, and 1 on the left of 2. The library's inorder walk visits left, node, right, so it returns [1, 2, 4, 6]. A duplicate key is ignored.",
            "why": "The search invariant is that the target, if it exists, lies in the subtree still being walked. Going left throws away the node and its right subtree because those keys are ≥ the node and the target is smaller. Going right throws away the left subtree for the symmetric reason. Insert uses the same walk and writes the new node only at an empty child, so the parent comparison that led there is still true. Inorder returns sorted keys because it emits the whole left subtree, then the node, then the whole right subtree, and both subtrees are themselves ordered.",
            "cost": "Each insert or lookup does one comparison per level, so the time is Θ(h) where h is the height. A balanced tree has h = Θ(log n). Inserting sorted keys makes a chain and h = n, so the same operations are Θ(n). The call in this library is a loop, so extra memory is O(1) besides the nodes. The nodes themselves are Θ(n). Deletion has the same height cost. The successor is the next inorder key, the leftmost node of the right subtree when a right child exists.",
        },
        {
            "slug": "heap-operations",
            "objective": "heap-operations-trace-sift",
            "prompt": "heapify turns [3, 1, 4, 2] into a max-heap. Which key ends at the root before the sort extracts anything?",
            "options": [("four", "4"), ("three", "3"), ("one", "1")],
            "answer": "four",
            "correct": "A max-heap puts the largest key at index 0. 4 is the largest key.",
            "retry": "The heap invariant says every parent is ≥ its children. The largest key has nowhere to go but the root.",
            "hints": ["This heap is a max-heap.", "heapify runs before any extraction."],
            "scenario": scenario("heap-core", "Heapify [3, 1, 4, 2]", "Children of index i are 2i + 1 and 2i + 2. heapify sifts from the last parent down to the root. heapsort then extracts until the array is sorted ascending.", computed_frames("heap-operations")),
            "idea": "A binary heap stores a complete tree in an array. For a max-heap, every parent is ≥ its children, so the largest key is at index 0. The children of index i are 2i + 1 and 2i + 2. heapify starts at the last parent and sifts that item down until the invariant holds. On [3, 1, 4, 2] the last parent is index 1. Sifting swaps 1 with 2, leaving [3, 2, 4, 1]. Sifting the root then swaps 3 with 4, leaving [4, 2, 3, 1]. heapsort extracts the root until the array is sorted. The library returns [1, 2, 3, 4].",
            "why": "Sift-down restores the invariant in one subtree when both children are already heaps. It swaps the parent with the larger child when the parent is smaller, then repeats. Each swap moves the violation down, and a leaf has no child to violate. heapify can start at the last parent because every index after that is a leaf, and a leaf is already a heap. The extraction loop removes the current maximum and sifts the item that was moved into the root, so the next maximum surfaces. Writing extracted maxima from the end of the array backward produces ascending order.",
            "cost": "heapify is Θ(n). The sift at a node is proportional to its height, and the sum of heights in a complete tree is less than 2n. Each of the n extractions then sifts a prefix of height Θ(log n), so heapsort is Θ(n log n) time. The heap reuses the input array, so extra memory is O(1). The sort is not stable. A priority queue uses the same sift for insert and extract-min, each Θ(log n), which is the right cost when you need the next extreme key and not the full sorted order.",
        },
        {
            "slug": "graph-traversals",
            "objective": "graph-traversal-trace-discovery",
            "prompt": "BFS starts at A. Edges are A→B, A→C, B→D. What is the visit order?",
            "options": [("abcd", "A, B, C, D"), ("abdc", "A, B, D, C"), ("acbd", "A, C, B, D")],
            "answer": "abcd",
            "correct": "A is dequeued first and enqueues B then C. B is dequeued next and enqueues D. C follows.",
            "retry": "The queue removes the oldest vertex. B was enqueued before C, and D is enqueued only when B is visited.",
            "hints": ["Enqueue neighbors in the order the edge list stores them.", "D is a neighbor of B, so it cannot pass C if C was already queued."],
            "scenario": scenario("bfs-core", "Breadth-first search from A", "The library breadth_first_order on this graph returns [A, B, C, D]. The queue's left end is the front.", computed_frames("graph-traversals")),
            "idea": "Breadth-first search uses a queue. Depth-first search uses a stack, or the call stack. Both mark a vertex when they first discover it so an edge back to a visited vertex does not enqueue it again. On the directed graph A→B, A→C, B→D, breadth-first order from A is A, B, C, D. B and C are both neighbors of A, and B is enqueued first because it is the first edge. D is discovered from B, so it waits behind C. The library function breadth_first_order returns that list.",
            "why": "The queue's FIFO order is the reason BFS visits vertices in order of distance from the start. When A is dequeued, its neighbors are one edge away and they enter the queue together. The next dequeues are those neighbors, and their new neighbors are two edges away. A vertex is marked visited when it is enqueued, not when it is dequeued, so a later edge cannot place it in the queue a second time. DFS would push neighbors on a stack and could visit D before C, because the most recently pushed neighbor is popped first.",
            "cost": "Each vertex is enqueued once and each edge is inspected once. The time is Θ(V + E) for the vertices and edges reachable from the start. The queue holds at most V vertices, so extra memory is Θ(V). An adjacency matrix would make the neighbor scan Θ(V) per vertex even when the graph is sparse, which is Θ(V²). The adjacency list is why the bound can mention E.",
        },
        {
            "slug": "union-find",
            "objective": "union-find-track-components",
            "prompt": "Naive union links 1 under 0, then links 2 under find(1). What does find(2) walk?",
            "options": [("two-links", "2 to 0, one link, because find(1) returned 0 before 2 was linked"), ("chain", "2 to 1 to 0, when 2 was linked to 1"), ("none", "Nothing. find returns 2 because 2 was never a parent")],
            "answer": "two-links",
            "correct": "For the library's naive union, find(1) returns 0 before the link, so 2's parent becomes 0. find(2) then walks 2 → 0.",
            "retry": "Look at the parent written for 2. Naive union links the root of the second item, and that root was found before the write.",
            "hints": ["find(1) does not stop at 1 if 1's parent is 0.", "The new parent of 2 is the root, not the original label 1."],
            "scenario": scenario("union-find-core", "Union 0-1 and 1-2 without heuristics", "Parent pointers start as self-links. The library DisjointSet without heuristics links the second root under the first.", computed_frames("union-find")),
            "idea": "A disjoint-set forest tracks which items are in the same set. Each item stores a parent. The root is the item whose parent is itself, and it names the set. find walks parents to the root. union merges two sets by pointing one root at the other. Without heuristics, union(0, 1) sets parent[1] = 0, and union(1, 2) finds that 1's root is already 0 and sets parent[2] = 0. find(2) and find(0) then return the same root. The library's DisjointSet(3, use_heuristics=False) does this.",
            "why": "find returns the same root for two items exactly when they are in the same tree. union joins those trees only when the roots differ, so it does not create a cycle. Linking a root, rather than an arbitrary item, keeps every node on a path to a single root. The naive version can still build a long chain if each new item is hung under the previous leaf and find does not compress. Path compression points every visited node at the root. Union by rank hangs the shorter tree under the taller one. Together they make a long chain unlikely.",
            "cost": "Without the heuristics, find is Θ(n) in the worst case on a chain of n items. With union by rank and path compression, the amortized cost of a find is the inverse of the Ackermann function, which is effectively constant for every practical n. Extra memory is the parent array, Θ(n), and a rank array when the heuristic is on. Kruskal's algorithm uses this to skip an edge whose ends are already connected.",
        },
        {
            "slug": "dynamic-programming",
            "objective": "dp-build-recurrence",
            "prompt": "The Fibonacci recurrence is F(n) = F(n - 1) + F(n - 2), with F(0) = 0 and F(1) = 1. What is F(6)?",
            "options": [("eight", "8"), ("thirteen", "13"), ("five", "5")],
            "answer": "eight",
            "correct": "The table is 0, 1, 1, 2, 3, 5, 8. fibonacci_modulo(6, 1000) returns 8.",
            "retry": "Fill the table left to right. Each new cell is the sum of the previous two. Do not stop at F(5).",
            "hints": ["F(2) = 1, F(3) = 2, F(4) = 3, F(5) = 5.", "The library function returns F(n) modulo the given modulus. 8 mod 1000 is 8."],
            "scenario": scenario("dp-core", "Bottom-up Fibonacci through F(6)", "Each cell is the sum of the two cells before it. The library keeps only the last two values. The table here shows the same numbers.", computed_frames("dynamic-programming")),
            "idea": "Dynamic programming applies when a problem repeats smaller versions of itself and you can order those versions so each one is ready before you need it. The Fibonacci recurrence F(n) = F(n - 1) + F(n - 2), with F(0) = 0 and F(1) = 1, is the smallest example. A naive recursion recomputes F(3) many times. A bottom-up table fills each index once. The library function fibonacci_modulo keeps only the last two values and returns F(n) mod m. For n = 6 and m = 1000 the result is 8.",
            "why": "The table is correct by induction. The base cells match the definition. If cells n - 1 and n - 2 hold F(n - 1) and F(n - 2), their sum is F(n) by the recurrence, so writing that sum into cell n preserves the claim. The fill order matters. Cell n is written only after the two cells it reads. A recursion with memoization is the same idea stored in a dictionary instead of an array. The state is the argument n. The transition is the sum. The base cases are the two starting cells.",
            "cost": "The table version does Θ(1) work per cell and fills n cells, so the time is Θ(n). The full table uses Θ(n) extra memory. Keeping two running values uses Θ(1) extra memory and the same Θ(n) time, which is what fibonacci_modulo does. The naive recursion without a table does Θ(φ^n) additions because it repeats work. The win is not the recurrence. The win is computing each state once. Larger problems add a second index, and the cost becomes the number of states times the cost of one transition.",
        },
    ]


def render(spec: dict[str, object]) -> str:
    scene = spec["scenario"]
    assert isinstance(scene, dict)
    frames = scene["frames"]
    assert isinstance(frames, list)
    return body(str(spec["idea"]), frames, str(spec["why"]), str(spec["cost"]), str(spec["slug"]))


def all_specs() -> list[dict[str, object]]:
    return [*LESSONS, *more_lessons(), *final_lessons()]


def transfer_questions() -> dict[str, dict[str, object]]:
    """Questions whose correct label is not a cell in the worked trace."""
    assert min(5, 4) == 4
    assert 2 * 1 + 1 == 3
    stack = Stack(limit=4)
    for item in (1, 2):
        stack.push(item)
    stack.pop()
    stack.push(3)
    assert stack.pop() == 3 and stack.pop() == 1
    queue = LinkedQueue()
    queue.enqueue("a")
    queue.enqueue("b")
    queue.dequeue()
    queue.enqueue("c")
    assert queue.dequeue() == "b"
    return complete_transfers({
        "input-size-and-operation-counts": {
            "prompt": "A loop over 6 items checks every unordered pair. How many checks run?",
            "options": [("fifteen", "15 checks, from 6 times 5 divided by 2"), ("six", "6 checks, one per item"), ("thirty-six", "36 checks, from 6 times 6")],
            "answer": "fifteen",
            "correct": "The pair count is 6 * 5 / 2, which is 15.",
            "retry": "The last item has no partner left. Do not count 6 * 6.",
            "hints": ["Use n(n - 1) / 2 with n = 6.", "6 * 5 is 30, and half of that is the pair count."],
            "more": [{
                "suffix": "transfer",
                "objective": "input-size-count-loop-work",
                "prompt": "The same pair loop runs on 4 items. How many checks is that?",
                "options": [("six", "6 checks"), ("four", "4 checks"), ("eight", "8 checks")],
                "answer": "six",
                "correct": "4 * 3 / 2 is 6.",
                "retry": "Count pairs, not the length of the list.",
                "hints": ["n is 4.", "The formula is n(n - 1) / 2."],
            }],
        },
        "merge-sort": {
            "prompt": "Runs [2, 5] and [3, 4] have already written 2 and 3. Which value leaves next?",
            "options": [("right-front", "The smaller remaining front, which is 4"), ("left-front", "The left front, which is 5"), ("both", "Both remaining fronts in one step")],
            "answer": "right-front",
            "correct": "The remaining fronts are 5 and 4. The merge takes 4.",
            "retry": "After 2 and 3 leave, compare 5 with 4.",
            "hints": ["2 and 3 are already in the output.", "4 is smaller than 5."],
            "more": [{
                "suffix": "transfer",
                "objective": "merge-sort-merge-runs",
                "prompt": "A merge of n items does Θ(n) work, and there are Θ(log n) levels. What is the total?",
                "options": [("n-log", "Θ(n log n), because each level does linear work"), ("n-squared", "Θ(n²), because the levels multiply"), ("log-only", "Θ(log n), because only the depth matters")],
                "answer": "n-log",
                "correct": "Θ(log n) levels times Θ(n) merging is Θ(n log n).",
                "retry": "Do not drop the linear work that happens on every level.",
                "hints": ["The recurrence is T(n) = 2T(n/2) + Θ(n).", "Count both the depth and the work per level."],
            }],
        },
    })


def _choice(slug: str, second_objective: str, prompt: str, correct: str, wrong_a: str, wrong_b: str) -> dict[str, object]:
    return {
        "prompt": prompt,
        "options": [("yes", correct), ("no", wrong_a), ("other", wrong_b)],
        "answer": "yes",
        "correct": correct,
        "retry": f"Check the count again. {wrong_a} does not match this input.",
        "hints": ["Use the same rule as the lesson, on this new input.", "Compare only the values named in the question."],
        "more": [{
            "suffix": "transfer",
            "objective": second_objective,
            "prompt": f"Apply the same rule from {slug} to one new case. Which statement holds?",
            "options": [("holds", correct), ("fails", wrong_a), ("unrelated", wrong_b)],
            "answer": "holds",
            "correct": correct,
            "retry": "The new case uses the same rule. Do not switch rules.",
            "hints": ["The lesson's rule does not change for a new input.", "Reject the statement that contradicts the rule."],
        }],
    }


def complete_transfers(partial: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    extras = {
        "asymptotic-growth": ("asymptotic-compare-growth", "For large n, which grows faster?", "n squared grows faster than n log n", "n log n grows faster than n squared", "They stay equal for every n"),
        "loop-invariants": ("invariant-state-loop-property", "A loop has finished. What must the invariant still say?", "The invariant holds after the last iteration too", "The invariant applies only before the loop", "The invariant replaces the postcondition"),
        "arrays-and-python-costs": ("python-sequence-analyze-amortized-cost", "You drain 1000 items with pop from the front. What dominates?", "About half a million reference moves, from repeated front pops", "About 1000 moves, one per pop", "About 1000 hash lookups"),
        "dynamic-array-growth": ("dynamic-array-geometric-growth", "Capacity starts at 1 and doubles. After 3 appends, how many copies happened?", "3 copies, from 0 plus 1 plus 2", "1 copy, only the last resize", "7 copies, one per new slot"),
        "recursion-and-recurrences": ("recursion-identify-shape", "A recursion splits in half and does linear work. What is the total?", "Θ(n log n) from a balanced split plus linear work per level", "Θ(n²) from a chain of n calls", "Θ(n) because the depth is logarithmic"),
        "singly-linked-list": ("linked-list-trace-links", "You have a pointer to the tail of a singly linked list. What is expensive?", "Deleting the tail, because the predecessor is not stored", "Reading the tail, because the pointer is already there", "Appending, because the tail pointer must walk from the head"),
        "stack-basics": ("stack-maintain-size-invariant", "Push 1, push 2, pop, push 3, pop, pop. What remains, then what was last?", "The last pop returns 1, and the stack is empty", "The last pop returns 3", "The last pop returns 2"),
        "queue-and-deque-operations": ("queue-compare-implementations", "Enqueue a, enqueue b, dequeue, enqueue c, dequeue. What leaves second?", "b leaves second, because a already left", "c leaves second", "a leaves second"),
        "comparison-sorts": ("comparison-sort-compare-properties", "Insertion sort uses a strict less-than. What happens to equal keys?", "Equal keys keep their order, so the sort is stable", "Equal keys always swap", "Equal keys make the sort quadratic"),
        "quicksort-and-partition": ("quicksort-analyze-split-cost", "Every pivot lands at the end. What recurrence is that?", "T(n) = T(n - 1) + Θ(n), which is quadratic", "T(n) = 2T(n/2) + Θ(n) for every pivot", "T(n) = Θ(n) because the scan is linear"),
        "hash-chaining": ("hash-chaining-analyze-load-factor", "n keys sit in b buckets. What is the average chain length?", "n divided by b, the load factor", "n plus b", "Always 1, because hashing avoids collisions"),
        "binary-search-tree-operations": ("bst-operations-find-successor", "Node 2 has no right child, and its parent 4 is larger. Where is the successor of 2?", "The parent 4, the next larger ancestor", "The left child of 2", "There is no successor in a binary tree"),
        "heap-operations": ("heap-operations-derive-heapsort-cost", "Index 1 in [3, 8, 1, 9, 4, 2] has children at 3 and 4. Which child is larger?", "Index 3, because 9 is larger than 4", "Index 4, because it is the right child", "Index 1, because the parent is always largest"),
        "graph-traversals": ("graph-traversal-analyze-work", "A breadth-first search marks a vertex when it is enqueued. What does that prevent?", "A later edge cannot enqueue the same vertex again", "The queue can hold the vertex twice, which is required", "The search skips every edge"),
        "union-find": ("union-find-explain-optimizations", "Naive union links 2 under find(1), and find(1) is already 0. How long is the walk from 2?", "One hop, from 2 directly to 0", "Two hops, from 2 to 1 to 0", "No hop, because 2 stays a root"),
        "dynamic-programming": ("dp-identify-state", "Fibonacci keeps only the two previous values. What is the extra memory?", "O(1) extra memory, not a full table", "O(n) extra memory for every F(i)", "O(n²) extra memory for pairs of indexes"),
    }
    assert Stack and LinkedQueue
    for slug, (objective, prompt, correct, wrong_a, wrong_b) in extras.items():
        partial[slug] = _choice(slug, objective, prompt, correct, wrong_a, wrong_b)
    partial["dynamic-programming"]["more"].append({
        "suffix": "memory",
        "objective": "dp-analyze-time-memory",
        "prompt": "fibonacci_modulo(6, 1000) returns 8. How much extra memory did that call keep?",
        "options": [("constant", "A constant number of integers"), ("table", "A table of 7 integers"), ("matrix", "A matrix of pairs")],
        "answer": "constant",
        "correct": "The library keeps two running values, and F(6) is 8.",
        "retry": "Do not allocate a cell per index. The code updates two names.",
        "hints": ["The result is 8.", "The implementation does not store F(0) through F(6)."],
    })
    return partial


def patch_curriculum(text: str, specs: list[dict[str, object]]) -> str:
    for spec in specs:
        slug = str(spec["slug"])
        key = rf'(?:"{re.escape(slug)}"|{re.escape(slug)})'
        text, version_count = re.subn(
            rf'({key}\s*:\s*\{{[^{{}}]*?contentVersion:\s*)\d+',
            r"\g<1>2",
            text,
            count=1,
        )
        text, readiness_count = re.subn(
            rf'({key}\s*:\s*\{{[^{{}}]*?contentReadiness:\s*")(?:summary|partial)(")',
            r"\1partial\2",
            text,
            count=1,
        )
        text, trace_count = re.subn(
            rf'({key}\s*:\s*\{{[^{{}}]*?traceIds:\s*)\[[^\]]*\]',
            rf'\1["{slug}-core"]',
            text,
            count=1,
        )
        more = transfer_questions()[slug]["more"]
        extra_ids = ", ".join(f'"{slug}-{item["suffix"]}"' for item in more)
        text, exercise_count = re.subn(
            rf'({key}\s*:\s*\{{[^{{}}]*?exerciseIds:\s*)\[[^\]]*\]',
            rf'\1["{slug}-check", {extra_ids}]',
            text,
            count=1,
        )
        if (version_count, readiness_count, trace_count, exercise_count) != (1, 1, 1, 1):
            raise SystemExit(f"curriculum patch failed for {slug}")
    return text


def build() -> dict[str, str]:
    specs = all_specs()
    files: dict[str, str] = {}
    traces: dict[str, list[dict[str, object]]] = {}
    exercises = json.loads(PILOT_EXERCISES.read_text())
    transfers = transfer_questions()
    for spec in specs:
        slug = str(spec["slug"])
        override = transfers[slug]
        for field in ("prompt", "options", "answer", "correct", "retry", "hints"):
            spec[field] = override[field]
        scene = spec["scenario"]
        assert isinstance(scene, dict)
        scene["id"] = f"{slug}-core"
        rendered = render(spec)
        words = len(rendered.split())
        if words < 280:
            raise SystemExit(f"{slug} is too short ({words} words)")
        matches = list(GUIDE.glob(f"*-{slug}.md"))
        if len(matches) != 1:
            raise SystemExit(f"expected one guide file for {slug}, found {matches}")
        original = matches[0].read_text()
        parts = original.split("---", 2)
        if len(parts) < 3:
            raise SystemExit(f"{matches[0]} has no frontmatter")
        files[str(matches[0].relative_to(ROOT))] = f"---{parts[1]}---\n\n{rendered}"
        traces[slug] = [scene]
        exercises.append(exercise(
            slug,
            str(spec["objective"]),
            str(spec["prompt"]),
            spec["options"],  # type: ignore[arg-type]
            str(spec["answer"]),
            str(spec["correct"]),
            str(spec["retry"]),
            spec["hints"],  # type: ignore[arg-type]
        ))
        for extra in override["more"]:
            exercises.append(exercise(
                slug,
                str(extra["objective"]),
                str(extra["prompt"]),
                extra["options"],  # type: ignore[arg-type]
                str(extra["answer"]),
                str(extra["correct"]),
                str(extra["retry"]),
                extra["hints"],  # type: ignore[arg-type]
                str(extra["suffix"]),
            ))
    files[str(TRACES_OUT.relative_to(ROOT))] = json.dumps(traces, indent=2) + "\n"
    files[str(EXERCISES_OUT.relative_to(ROOT))] = json.dumps(exercises, indent=2) + "\n"
    files[str(CURRICULUM.relative_to(ROOT))] = patch_curriculum(CURRICULUM.read_text(), specs)
    return files


def main() -> int:
    checking = "--check" in sys.argv
    files = build()
    dirty = []
    for relative, contents in files.items():
        path = ROOT / relative
        current = path.read_text() if path.exists() else None
        if current != contents:
            dirty.append(relative)
            if not checking:
                path.write_text(contents)
    if checking and dirty:
        print("build_guide_lessons: committed output is stale")
        for relative in dirty:
            print(f"  {relative}")
        return 1
    print(f"build_guide_lessons: {len(all_specs())} lessons, check={checking}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
