#!/usr/bin/env python3
"""Write the critical-path lesson bodies, traces, and one checkpoint each.

The markdown and JSON in the repo are the output of this script. Run it from
the repository root. ``--check`` rewrites nothing and exits 1 when a committed
file would change.
"""

from __future__ import annotations

import hashlib
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


def place_options(item: dict[str, object]) -> None:
    """Rotate options by a stable hash of the exercise id and assign letter ids."""

    if item.get("lessonSlug") in {"binary-search", "binary-search-on-answer"}:
        return
    options = item.get("options")
    if not isinstance(options, list) or len(options) < 2:
        return
    offset = int(hashlib.sha1(str(item["id"]).encode()).hexdigest(), 16) % len(options)
    rotated = options[offset:] + options[:offset]
    letters = "abcdefghij"
    new_options: list[dict[str, str]] = []
    new_answer = None
    for index, option in enumerate(rotated):
        new_id = letters[index]
        if option["id"] == item["answer"]:
            new_answer = new_id
        new_options.append({"id": new_id, "label": option["label"]})
    if new_answer is None:
        raise SystemExit(f"{item['id']} lost its answer during rotation")
    item["options"] = new_options
    item["answer"] = new_answer


def exercise(slug: str, objective_id: str, prompt: str, options: list[tuple[str, str]], answer: str, correct: str, retry: str, hints: list[str], suffix: str = "check") -> dict[str, object]:
    return {
        "id": f"{slug}-{suffix}",
        "lessonSlug": slug,
        "storageId": f"{slug}-{suffix}",
        "kind": "choice",
        "prompt": prompt,
        "hints": hints,
        "options": [{"id": option_id, "label": label} for option_id, label in options],
        "answer": answer,
        "correct": correct,
        "retry": retry,
        "objectiveId": objective_id,
    }


def _tokens(sentence: str) -> list[str]:
    tokens: list[str] = []
    for piece in re.split(r"(`[^`]*`)", sentence):
        if piece.startswith("`") and piece.endswith("`"):
            tokens.append(piece)
        else:
            tokens.extend(piece.split())
    return tokens


def shorten(text: str) -> str:
    sentences = re.split(r"(?<=[.?!])\s+", text.strip())
    for sentence in sentences:
        count = len(_tokens(sentence))
        if count > 25:
            raise SystemExit(f"sentence is {count} words: {sentence}")
    return text.strip()


def _lesson_order() -> list[str]:
    text = CURRICULUM.read_text()
    stages = re.search(r"export const curriculumStages:[\s\S]*?\n\];", text)
    if stages is None:
        raise SystemExit("curriculum stages not found")
    ordered: list[str] = []
    for match in re.finditer(r"slugs:\s*\[([^\]]*)\]", stages.group(0)):
        ordered.extend(re.findall(r'"([a-z0-9-]+)"', match.group(1)))
    return ordered


def _titles() -> dict[str, str]:
    found: dict[str, str] = {}
    for path in GUIDE.glob("*.md"):
        slug_match = re.search(r"^slug:\s*(\S+)\s*$", path.read_text(), re.M)
        title_match = re.search(r"^title:\s*(.+)\s*$", path.read_text(), re.M)
        if slug_match and title_match:
            found[slug_match.group(1)] = title_match.group(1).strip()
    return found


def closing(slug: str, reason: str) -> str:
    order = _lesson_order()
    titles = _titles()
    position = order.index(slug)
    if position + 1 >= len(order):
        return "Answer the checkpoints. This is the last lesson in the curriculum."
    nxt = titles[order[position + 1]]
    return shorten(f"Open {nxt} next. {reason}")


def body(idea: str, frames: list[dict[str, object]], why: str, cost: str, slug: str) -> str:
    from guide_lesson_voice import COST_NOTE, VOICE

    voice = VOICE[slug]
    example = shorten(str(voice["example"]))
    mistake = shorten(str(voice["mistake"]))
    idea = shorten(idea)
    why = shorten(why)
    cost = shorten(cost)
    if slug != "input-size-and-operation-counts" and (("Θ" not in cost and "O(" not in cost) or "memory" not in cost.lower()):
        cost = shorten(cost + " " + COST_NOTE[slug])
    if slug != "input-size-and-operation-counts" and "Θ" not in cost and "O(" not in cost:
        raise SystemExit(f"{slug} cost section has no bound")
    if "memory" not in cost.lower():
        raise SystemExit(f"{slug} cost section does not mention memory")
    lines = ["## The idea", "", example, "", idea.strip(), "", "## A worked trace", ""]
    lines.append("| Step | State | What changed |")
    lines.append("| --- | --- | --- |")
    for item in frames:
        state = ", ".join(f"{entry['name']} = {entry['value']}" for entry in item["state"])
        lines.append(f"| {item['label']} | {state} | {item['narration']} |")
    extra_text = {
        "arrays-and-python-costs": "A worked check is n = 1000. One pop(0) moves about 999 references. Doing that once per item moves about half a million references. A deque draining the same list moves about 1000 nodes. The asymptotic symbols summarize that count. Indexing stays Θ(1) on the list either way. A later binary search needs a random-access sequence, not a linked chain.",
        "asymptotic-growth": "Write the exact count first, as the previous lesson did for pairs. Only then replace it with Θ. If you start from Θ you can hide a bug such as an extra nested loop. The notation is a compression step, not a substitute for the count.",
        "recursion-and-recurrences": "Merge sort is this recurrence with a balanced split. A quicksort pivot that always peels off one item is the other shape, T(n) = T(n - 1) + Θ(n). Same lesson, different tree. Ask which shape you have before you quote n log n.",
        "queue-and-deque-operations": "Breadth-first search is the payoff. It is correct only when the frontier removes the oldest vertex. A list used as a stack visits a different order and the distance claim fails. The queue lesson is the reason that search works.",
        "comparison-sorts": "On [3, 1, 2] insertion sort shifts once to place 1 and once to place 2. A reverse-sorted list of n items shifts about n² / 2 times. That is the worst case you are accepting if you call insertion sort on arbitrary input.",
        "hash-chaining": "Keys 0 and 4 share a bucket because the bucket count is 4 and both hashes are multiples of 4. A third key 8 would append behind them. Lookup of 0 would then compare 0, skip 4, and skip 8 only if 0 were missing. The chain length is the cost you pay.",
        "graph-traversals": "The same graph searched depth-first from A can visit D before C, because D is pushed after C and a stack pops D first. If your test expected BFS order and the code used a stack, this is the mismatch. The container is the algorithm.",
    }.get(slug, "")
    extra = shorten(extra_text) if extra_text else ""
    lines.extend(["", "## Why it is correct", "", why.strip(), "", "## A common mistake", "", mistake, "", "## What it costs", "", cost.strip(), ""])
    if extra:
        lines.extend([extra, ""])
    snippet = RUNNABLE[slug]
    lines.extend(["## Run it", "", "```python", snippet.rstrip(), "```", ""])
    lines.extend(["## Practice and next step", "", closing(slug, str(voice["next_reason"]))])
    for item in frames:
        narration = str(item["narration"])
        count = len(_tokens(narration))
        if count > 25:
            raise SystemExit(f"{slug} narration is {count} words: {narration}")
    return "\n".join(lines) + "\n"


RUNNABLE = {
    "input-size-and-operation-counts": "from bitsandbytes.complexity import pair_comparison_count\nprint(pair_comparison_count([3, 1, 2]))\n# prints: 3",
    "asymptotic-growth": "from bitsandbytes.complexity import growth_table\nprint(growth_table((64,))[0])\n# prints: (64, 384, 4096)",
    "loop-invariants": "from bitsandbytes.sorting.insertion_sort import insertion_sort\nseen = []\ndef sink(event):\n    seen.append(list(event.values['values']))\ninsertion_sort([3, 1, 2], trace_sink=sink)\nprint(seen)\n# prints: [[3, 1, 2], [1, 3, 2], [1, 2, 3]]",
    "arrays-and-python-costs": "from bitsandbytes.library_costs import list_pop_front_cost_demo\nprint(list_pop_front_cost_demo(1000))\n# prints: 999",
    "dynamic-array-growth": "from bitsandbytes.linear.dynamic_array import DynamicArray\narray = DynamicArray()\nprint(array.total_copy_cost_for_appends(3))\n# prints: 3",
    "recursion-and-recurrences": "from bitsandbytes.sorting.merge_sort import merge_sort\nprint(merge_sort([3, 1, 4, 2]))\n# prints: [1, 2, 3, 4]",
    "singly-linked-list": "from bitsandbytes.linked_list import LinkedList\nchain = LinkedList()\nchain.append('a')\nprint(list(chain))\n# prints: ['a']",
    "stack-basics": "from bitsandbytes.stacks.stack import Stack\nstack = Stack(limit=4)\nstack.push(1)\nstack.push(2)\nstack.push(3)\nprint(stack.pop(), stack.pop())\n# prints: 3 2",
    "queue-and-deque-operations": "from bitsandbytes.queues.linked_queue import LinkedQueue\nqueue = LinkedQueue()\nqueue.enqueue('a')\nqueue.enqueue('b')\nprint(queue.dequeue())\n# prints: a",
    "comparison-sorts": "from bitsandbytes.sorting.insertion_sort import insertion_sort\nprint(insertion_sort([3, 1, 2]))\n# prints: [1, 2, 3]",
    "merge-sort": "from bitsandbytes.sorting.merge_sort import merge_sort\nprint(merge_sort([3, 1, 4, 2]))\n# prints: [1, 2, 3, 4]",
    "quicksort-and-partition": "import random\nfrom bitsandbytes.sorting.quick_sort import quick_sort\nprint(quick_sort([3, 1, 4, 2], rng=random.Random(0)))\n# prints: [1, 2, 3, 4]",
    "hash-chaining": "from bitsandbytes.hash_tables.chaining import ChainingHashTable\ntable = ChainingHashTable(bucket_count=4)\ntable[0] = 1\ntable[4] = 2\nprint(table[0], table[4])\n# prints: 1 2",
    "binary-search-tree-operations": "from bitsandbytes.trees.bst import BinarySearchTree\ntree = BinarySearchTree()\nfor value in (4, 2, 6, 1):\n    tree.insert(value)\nprint(tree.inorder())\n# prints: [1, 2, 4, 6]",
    "heap-operations": "from bitsandbytes.heaps.heapsort import heapsort\nprint(heapsort([3, 1, 4, 2]))\n# prints: [1, 2, 3, 4]",
    "graph-traversals": "from bitsandbytes.graphs.adjacency_list import Graph, breadth_first_order\ngraph = Graph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('A', 'C', 1)\ngraph.add_edge('B', 'D', 1)\nprint(breadth_first_order(graph, 'A'))\n# prints: ['A', 'B', 'C', 'D']",
    "union-find": "from bitsandbytes.union_find.disjoint_set import DisjointSet\nsets = DisjointSet(3, use_heuristics=False)\nsets.union(0, 1)\nsets.union(1, 2)\nprint(sets.find(2))\n# prints: 0",
    "dynamic-programming": "from bitsandbytes.dynamic_programming.classic import fibonacci_modulo\nprint(fibonacci_modulo(6, 1000))\n# prints: 8",
    "cost-models": "from bitsandbytes.library_costs import list_pop_front_cost_demo\nprint(list_pop_front_cost_demo(3))\n# prints: 2",
    "fast-slow-pointer-patterns": "from bitsandbytes.linked_list import LinkedList\nfrom bitsandbytes.linked_lists.middle import middle_node\nchain = LinkedList()\nfor item in (1, 2, 3, 4, 5):\n    chain.append(item)\nprint(middle_node(chain).data)\n# prints: 3",
    "linked-list-reversal-and-relinking": "from bitsandbytes.linked_list import LinkedList\nfrom bitsandbytes.linked_lists.reverse import reverse_iterative\nchain = LinkedList()\nfor item in (1, 2, 3):\n    chain.append(item)\nreverse_iterative(chain)\nprint(list(chain))\n# prints: [3, 2, 1]",
    "linked-list-merge-and-sort": "from bitsandbytes.linked_list import LinkedList\nfrom bitsandbytes.linked_lists.merge_sorted import merge_sorted\nleft, right = LinkedList(), LinkedList()\nleft.append(1); left.append(4); right.append(2); right.append(3)\nprint(list(merge_sorted(left, right)))\n# prints: [1, 2, 3, 4]",
    "linked-list-special-cases": "from bitsandbytes.linked_list import LinkedList\nfrom bitsandbytes.linked_lists.nth_from_end import nth_from_end\nchain = LinkedList()\nfor item in (1, 2, 3, 4):\n    chain.append(item)\nprint(nth_from_end(chain, 2).data)\n# prints: 3",
    "doubly-linked-list-operations": "from bitsandbytes.doubly_linked_list import DoublyLinkedList\nchain = DoublyLinkedList()\nfirst = chain.append('a')\nchain.append('b')\nprint(chain.remove_node(first))\n# prints: a",
}

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from guide_lesson_batches import EXTRA_QUESTIONS, EXTRA_RUNNABLE, batch_specs  # noqa: E402

RUNNABLE.update(EXTRA_RUNNABLE)

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
    from lesson_frames import frames_for

    generated = frames_for(slug)
    if generated is not None:
        return generated
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
    elif slug == "cost-models":
        from bitsandbytes.library_costs import list_pop_front_cost_demo
        copies = list_pop_front_cost_demo(3)
        assert copies == 2
        add("Front pop", "One pop(0) on three items moves 2 references.", [("copies", str(copies))], [copies], "chosen")
    elif slug == "fast-slow-pointer-patterns":
        from bitsandbytes.linked_list import LinkedList
        from bitsandbytes.linked_lists.cycle import find_cycle_start
        from bitsandbytes.linked_lists.middle import end_of_first_half, middle_node
        chain = LinkedList()
        for item in (1, 2, 3, 4, 5):
            chain.append(item)
        middle = middle_node(chain)
        assert middle is not None and middle.data == 3
        even = LinkedList([1, 2, 3, 4])
        even_middle = middle_node(even)
        assert even_middle is not None and even_middle.data == 3
        assert even.head is not None and end_of_first_half(even.head).data == 2
        cycled = LinkedList([1, 2, 3, 4, 5])
        cycled.node_at(4).next = cycled.node_at(2)
        found = find_cycle_start(cycled)
        assert found is not None and found[0] == 3 and found[1].data == 3
        add("Middle", "The slow pointer stops on the single middle.", [("middle", "3")], [1, 2, 3, 4, 5], "chosen")
        add("Even", "The second of the two middles is kept.", [("middle", "3")], [1, 2, 3, 4], "active")
        add("Entrance", "The cycle entrance is the node holding 3.", [("index", "3")], [1, 2, 3, 4, 5], "done")
    elif slug == "linked-list-reversal-and-relinking":
        from bitsandbytes.linked_list import LinkedList
        from bitsandbytes.linked_lists.reverse import reverse_iterative
        chain = LinkedList()
        for item in (1, 2, 3):
            chain.append(item)
        reverse_iterative(chain)
        assert list(chain) == [3, 2, 1]
        add("Reversed", "The head is now 3.", [("head", "3")], list(chain), "done")
    elif slug == "linked-list-merge-and-sort":
        from bitsandbytes.linked_list import LinkedList
        from bitsandbytes.linked_lists.merge_sorted import merge_sorted
        left, right = LinkedList(), LinkedList()
        for item in (1, 4):
            left.append(item)
        for item in (2, 3):
            right.append(item)
        merged = merge_sorted(left, right)
        assert list(merged) == [1, 2, 3, 4]
        add("Merged", "The heads were compared in order.", [("result", str(list(merged)))], list(merged), "done")
    elif slug == "linked-list-special-cases":
        from bitsandbytes.linked_list import LinkedList
        from bitsandbytes.linked_lists.nth_from_end import nth_from_end
        chain = LinkedList()
        for item in (1, 2, 3, 4):
            chain.append(item)
        node = nth_from_end(chain, 2)
        assert node.data == 3
        add("From end", "Two steps from the end lands on 3.", [("node", "3")], [1, 2, 3, 4], "chosen")
    elif slug == "doubly-linked-list-operations":
        from bitsandbytes.doubly_linked_list import DoublyLinkedList
        chain = DoublyLinkedList()
        first = chain.append("a")
        chain.append("b")
        assert chain.remove_node(first) == "a"
        add("Unlink", "Removing a known node does not walk the list.", [("removed", "a")], ["b"], "chosen")
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
        "cost": "The pair scan does n(n - 1) / 2 comparisons, which grows like n squared. Memory besides the input is a handful of indexes, a constant amount of extra memory. Suppose the inner loop ran over the whole list. The count would then be n times n. That is the same growth with a different constant.",
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
        "cost": "Using the notation does not change the algorithm. It changes the claim. A Θ(n) scan of a million items is a different engineering choice from a Θ(n²) pair scan of the same list. The trace shows n squared pulling away from n log n as n leaves the toy range.",
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
        "why": "Initialization holds because a prefix of one item is sorted, and the loop starts inserting at index 1. Preservation holds because the inner loop shifts every larger prefix item one slot right and writes the new key into the hole. The items that were sorted stay in order, and the new key sits between a smaller or equal left neighbor and a larger right neighbor. Termination holds because i runs from 1 to n - 1 and then stops. The prefix is the whole list, so the list is sorted. The library's insertion sort uses a strict < comparison, so an equal key does not move past an earlier equal key. Equal keys keep the order they already had.",
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
        "idea": "A Python list is a dynamic array of references. Indexing list[i] is Θ(1) because the address is base + i times the reference size. append and pop() at the end are cheap on average, which the next lesson counts. insert(0, x) and pop(0) move every later reference, so one call is Θ(n). A collections.deque stores blocks that can grow at either end, so append and popleft are Θ(1). Use a list when you need random access. Use a deque when both ends change and you do not need list[i] in the inner loop.",
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
        "why": "Each resize copies every item that is already stored, because the new block is a different region of memory. Doubling is what makes the total copy count linear. The copy sizes are 1 + 2 + 4 + ... + n/2, which is less than n. Every item is copied once per doubling after it arrives. An item that arrives near length n/2 is copied only once more before the length reaches n. Charging each append a constant amount covers all of those copies. That charge is the amortized bound.",
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
        "idea": "A recurrence describes a function that calls itself. The one you will meet in merge sort is T(n) = 2 T(n/2) + Θ(n), with T(1) = Θ(1). The 2 T(n/2) is the two recursive calls. The Θ(n) is the work to merge the halves. Unrolling the recurrence shows log2(n) levels, because the input size halves each time. Each level does Θ(n) work, because the pieces at one level add up to n. The product is Θ(n log n). The call stack on one path is Θ(log n) frames deep. That is extra memory even when each frame stores only a few indexes.",
        "why": "The level count is exact for powers of two. n, n/2, n/4, ..., 1 is log2(n) steps. At level i there are 2^i calls and each call works on n / 2^i items, so the level sums to n. Adding log2(n) levels of n work gives n log2(n). The base case stops the recurrence, which is the same role termination plays for a loop. An unbalanced recursion such as T(n) = T(n - 1) + Θ(n) has n levels and Θ(n²) total work. The shape of the calls is the whole story.",
        "cost": "Time is the unrolled sum, Θ(n log n) for the balanced split. Stack memory is proportional to the deepest chain of calls. It is Θ(log n) when every split is even. It is Θ(n) when each call peels off one item. Report the time and the stack. A time bound does not imply a stack bound.",
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
            "why": "The invariant is preserved by each edit that updates the cached fields together with the links. Append writes the new node, points the old tail at it, and then moves the tail cache. If it moved the cache first, the old tail would be unreachable and the invariant would fail. A search that starts at the head and follows next i times lands on index i. The nodes form a single chain with no extra forward jumps. There is no predecessor pointer, so the only way to find the node before the tail is to walk until next is the tail.",
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
            "idea": "A stack is a last-in, first-out sequence. push adds an item at the top. pop removes that same item. The size invariant is 0 ≤ size ≤ limit for a bounded stack, and size changes by exactly 1 on every successful push or pop. The teaching Stack in this repository stores items in a Python list and rejects a push that would pass the limit. After push 1, push 2, push 3, the first pop returns 3 and the second returns 2. That order is the definition, not an accident of the example. A Python list is the same stack when you append to push and call pop with no argument.",
            "why": "Each push writes one reference at the end of the list, which is the top. Each pop reads and removes that end. No operation reaches under the top, so the item pushed most recently is the item removed first. The size invariant holds by induction. It is 0 on an empty stack. A successful push adds 1 and a successful pop subtracts 1, and both refuse to step outside 0 and limit. When the stack is empty, pop has nothing to return. When it is full, push has no slot that stays within the limit.",
            "cost": "push and pop at the end of a list are amortized Θ(1). On this bounded stack they are Θ(1) because the list does not need to grow past the items you actually pushed within the limit. Extra memory is Θ(n) for n stored items. A stack does not offer Θ(1) access to the bottom. If you need the other end, use a queue.",
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
            "idea": "A queue is first-in, first-out. enqueue adds at the back and dequeue removes from the front. The linked queue in this repository uses a doubly linked list with a cached tail, so both ends are Θ(1). A ring buffer stores the same order in an array with a head index and a tail index. A deque allows add and remove at both ends. The order promise is the part to learn first. After enqueue a, b, c, two dequeues return a and then b. A Python list can act as a stack with append and pop at the end, and that is a different order from this queue.",
            "why": "The front is the earliest item that has not been dequeued. Enqueue does not change the front unless the queue was empty, in which case the new item is both front and back. Dequeue advances the front to the next node and returns the old one. That is why the exit order matches the arrival order. A stack would have returned c first. Mixing the two is the usual bug when a graph search asks for a queue. The code uses a list with pop() at the end and insert at the end.",
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
            "idea": "A comparison sort decides order only by asking whether one key is less than another. Insertion sort keeps a sorted prefix and inserts the next key into it. On a sorted list each new key is already in place, so the best case is Θ(n). The worst case is still Θ(n²). The library function insertion_sort([3, 1, 2]) returns [1, 2, 3]. Python's list.sort uses Timsort. It is O(n log n) and it keeps runs that are already ordered.",
            "why": "The insertion invariant is the sorted prefix from the loop-invariants lesson. After inserting 1, every item in the prefix is in order and every item outside it is still untouched. The next step considers 2 only against that prefix. Selection sort is a different invariant, covered here only as a cost comparison. Its prefix holds the smallest items so far, and a swap can move an equal key past another equal key.",
            "cost": "Worst-case time for insertion sort is Θ(n²) comparisons. The best case is Θ(n). Extra memory is O(1). Selection sort and bubble sort share the Θ(n²) worst case and also use O(1) extra memory. Merge sort, next, spends Θ(n) extra memory to bring the worst case down to Θ(n log n).",
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
            "why": "A list of length 0 or 1 is already sorted, which is the base case. If both halves are sorted, the merge is sorted because every output item is the smaller remaining front. Nothing still in either run is smaller than that item. Stability follows from taking the left run on a tie. The left run holds the earlier original items of that key. The split keeps original order inside each half, and the recursive sorts are themselves stable.",
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
            "idea": "Quicksort picks a pivot and partitions the range. Every value before the pivot is at most the pivot. Every value after it is greater, and then the two sides are sorted. The library's partition swaps the chosen pivot to the end and scans once. boundary is the next slot that should receive a value at most the pivot. For pivot 2 at the end of [3, 1, 4, 2], the scan swaps 1 to index 0. The next swap places 2 at index 1, leaving [1, 2, 4, 3]. The recursive calls sort the two sides. quick_sort on this input returns [1, 2, 3, 4]. The pivot index itself is random unless you pass a Random instance.",
            "why": "The partition invariant is that every index before boundary holds a value ≤ pivot. Every index from boundary to the scan cursor holds a value > pivot. It is true before the scan because that region is empty. Seeing a value > pivot extends the right region without moving boundary. Seeing a value ≤ pivot swaps it into the boundary slot and advances the boundary, which restores the invariant. The final swap puts the pivot at boundary. Everything before it is ≤ pivot and everything after it is > pivot, so the pivot is in its final sorted index.",
            "cost": "One partition of k items is Θ(k) time and O(1) extra memory. If every pivot splits off one item, the recurrence is T(n) = T(n - 1) + Θ(n). That shape is Θ(n²), and the call stack is Θ(n) deep. Balanced pivots give T(n) = 2 T(n/2) + Θ(n), which is Θ(n log n) time and Θ(log n) stack. The sort is not stable, because the swaps move equal keys past each other. A three-way partition gathers equals in the middle so a run of duplicate keys does not fall into the n² case.",
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
            "idea": "Separate chaining stores a list of key-value pairs in each bucket. The hash of the key picks the bucket. Insert appends a pair, or replaces the value if the key is already in that list. Lookup scans the list and compares keys. With a 4-bucket table, hash(0) % 4 and hash(4) % 4 are both 0. Inserting 0 and then 4 places both pairs in one chain. A later lookup of 0 walks that chain and returns 1. The library ChainingHashTable does this, and len stays 2 because the keys differ.",
            "why": "The hash is only a suggestion of where to look. Equality of keys is the real test. Two keys that share a bucket remain distinct as long as the chain stores both pairs. Lookup does not stop at the first pair. Insert of a new key appends, which preserves the pairs already there. Insert of an existing key overwrites that pair's value instead of appending a duplicate. That is why a lookup that scans from the front finds the current value.",
            "cost": "The load factor is the number of keys divided by the number of buckets. With n keys and b buckets the average chain is that load factor, n / b. One lookup is Θ(1 + n / b) comparisons when keys spread evenly, and Θ(n) when every key lands in one bucket. Resizing when the load factor grows keeps the average chain short, and the resize itself copies every pair once. Extra memory is Θ(n + b) for the pairs and the bucket lists. Expected Θ(1) is not a worst-case promise.",
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
            "idea": "A complete tree fills every level except possibly the last, and that last level fills from the left. A binary heap stores a complete tree in an array. Python's heapq is this structure as a min-heap. heappop returns the smallest item. For a max-heap, every parent is ≥ its children, so the largest key is at index 0. The children of index i are 2i + 1 and 2i + 2. heapify starts at the last parent and sifts that item down until the invariant holds. On [3, 1, 4, 2] the last parent is index 1. Sifting swaps 1 with 2, leaving [3, 2, 4, 1]. Sifting the root then swaps 3 with 4, leaving [4, 2, 3, 1]. heapsort extracts the root until the array is sorted. The library returns [1, 2, 3, 4].",
            "why": "Sift-down restores the invariant in one subtree when both children are already heaps. It swaps the parent with the larger child when the parent is smaller, then repeats. Each swap moves the violation down, and a leaf has no child to violate. heapify can start at the last parent because every index after that is a leaf, and a leaf is already a heap. The extraction loop removes the current maximum and sifts the item that was moved into the root, so the next maximum surfaces. Writing extracted maxima from the end of the array backward produces ascending order.",
            "cost": "heapify is Θ(n). The sift at a node is proportional to its height, and the sum of heights in a complete tree is less than 2n. Each of the n extractions then sifts a prefix of height Θ(log n), so heapsort is Θ(n log n) time. The heap reuses the input array, so extra memory is O(1). The sort is not stable. A priority queue uses the same sift for insert and extract-min, each Θ(log n). Which is the right cost when you need the next extreme key and not the full sorted order.",
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
            "why": "The queue's FIFO order is the reason BFS visits vertices in order of distance from the start. When A is dequeued, its neighbors are one edge away and they enter the queue together. The next dequeues are those neighbors, and their new neighbors are two edges away. A vertex is marked visited when it is enqueued, not when it is dequeued. A later edge cannot place it in the queue a second time. DFS would push neighbors on a stack and could visit D before C, because the most recently pushed neighbor is popped first.",
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
            "cost": "Without the heuristics, find is Θ(n) in the worst case on a chain of n items. With union by rank and path compression. The amortized cost of a find is the inverse of the Ackermann function, which is effectively constant for every practical n. Extra memory is the parent array, Θ(n), and a rank array when the heuristic is on. Kruskal's algorithm uses this to skip an edge whose ends are already connected.",
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
            "idea": "Dynamic programming applies when a problem repeats smaller versions of itself and you can order those versions. So each one is ready before you need it. The Fibonacci recurrence F(n) = F(n - 1) + F(n - 2), with F(0) = 0 and F(1) = 1, is the smallest example. A naive recursion recomputes F(3) many times. A bottom-up table fills each index once. The library function fibonacci_modulo keeps only the last two values and returns F(n) mod m. For n = 6 and m = 1000 the result is 8.",
            "why": "The table is correct by induction. The base cells match the definition. If cells n - 1 and n - 2 hold F(n - 1) and F(n - 2). Their sum is F(n) by the recurrence, so writing that sum into cell n preserves the claim. The fill order matters. Cell n is written only after the two cells it reads. A recursion with memoization is the same idea stored in a dictionary instead of an array. The state is the argument n. The transition is the sum. The base cases are the two starting cells.",
            "cost": "The table version does Θ(1) work per cell and fills n cells, so the time is Θ(n). The full table uses Θ(n) extra memory. Keeping two running values uses Θ(1) extra memory and the same Θ(n) time, which is what fibonacci_modulo does. The naive recursion without a table does Θ(φ^n) additions because it repeats work. The win is not the recurrence. The win is computing each state once. Larger problems add a second index, and the cost becomes the number of states times the cost of one transition.",
        },
    ]


def render(spec: dict[str, object]) -> str:
    scene = spec["scenario"]
    assert isinstance(scene, dict)
    frames = scene["frames"]
    assert isinstance(frames, list)
    return body(str(spec["idea"]), frames, str(spec["why"]), str(spec["cost"]), str(spec["slug"]))


def batch_a() -> list[dict[str, object]]:
    return [
        {
            "slug": "cost-models",
            "objective": "cost-model-state-assumptions",
            "scenario": scenario("cost-models-core", "One front pop of three items", "list_pop_front_cost_demo(3) returns 2. That is the number of references one pop(0) moves, not a count of three pops.", computed_frames("cost-models")),
            "idea": "A complexity claim is true only inside a stated model. The word-RAM model charges one step for a comparison, a pointer write, or word-sized arithmetic. That model fits a list of machine words. It is the wrong model when one named step hides a loop. A Python list is a dynamic array of references. Reading an index is one address calculation. list.pop(0) moves every later reference one slot toward index 0. list_pop_front_cost_demo(3) returns 2. Those two writes are the items that remain after the front item leaves. A linked list has no constant-time middle. Binary search stays logarithmic only when each index is constant time. Count the container operation the code actually performs. State a key-size assumption before you call hashing constant time. Count the recursion stack apart from the loop variables. The point of this lesson is to separate algorithm steps from Python container costs.",
            "why": "The demo returns length minus 1 for a positive length. A list of three items has two items behind the front. Each of those items slides one slot. The spare capacity of a list sits at the end, not at index 0. Binary search on a list is logarithmic because each middle index is constant time. The same comparisons on a linked list walk from the head. The elapsed work is then linear in the index, not logarithmic. bisect.insort is linear overall because the insertion dominates the logarithmic search. A deque documents approximately constant-time endpoint appends and pops. The bound and the container belong in the same sentence.",
            "cost": "One pop(0) on n items moves n - 1 references. That is linear in n. Draining n items from the front moves about n squared over 2 references. n calls to deque.popleft are linear in total. The demo computes length minus 1 and does not build the list. Reporting a logarithmic bound without saying random-access hides the linked-list case. The assumption is part of the claim. A later lesson can turn this exact count into a tight growth bound.",
        },
        {
            "slug": "fast-slow-pointer-patterns",
            "objective": "fast-slow-locate-middle-cycle",
            "scenario": scenario("fast-slow-core", "Middle, even length, and a cycle entrance", "middle_node on 1 through 5 returns 3. On 1 through 4 it returns 3, the second middle. A tail that points at 3 makes find_cycle_start return index 3.", computed_frames("fast-slow-pointer-patterns")),
            "idea": "A linked list has no index, so two pointers replace a length calculation. The fast pointer moves two links for every one link the slow pointer moves. When fast falls off a linear list, slow is at a middle node. middle_node on 1, 2, 3, 4, 5 returns the node holding 3. On an even list the same function returns the second of the two middles. middle_node on 1, 2, 3, 4 returns 3. end_of_first_half stops one step sooner and returns 2, the left middle. Palindrome and reorder split there. If the links form a cycle, fast gains one node per iteration and meets slow inside the cycle. Reset one pointer to the head and walk both one step at a time. They meet at the entrance. On 1 through 5 with the tail linked to 3, find_cycle_start returns index 3. A fixed gap finds a node from the end. Move a lead pointer k links ahead, then move both pointers together. The gap stays k.",
            "why": "The speed ratio is the whole argument. Fast takes two steps while slow takes one, so slow has seen half the nodes when fast finishes a linear list. The even-length choice is a contract. Stopping when fast cannot take two more steps keeps the later middle. Stopping when fast.next.next is missing keeps the earlier middle. Both land on the single middle when the length is odd. Inside a cycle the same ratio makes a meeting inevitable, because fast closes the gap by one node each iteration. The entrance walk works because the meeting point is a known number of steps from the entrance, matching the distance from the head. The gap method needs no subtraction. When the lead falls off, the trailer is k nodes from the end.",
            "cost": "Each walk examines each link a constant number of times, so the time is linear in the number of nodes. The pointer walk stores a constant number of references. require_linear may hold a set of node ids while it checks for a cycle, and that set is a separate cost from the two-pointer loop. Say which one you are counting. Before you call one of these functions, state the even-length rule, what k means, and whether a cycle is allowed. Test an empty list, one node, an even length, and a cycle against that contract.",
        },
        {
            "slug": "linked-list-reversal-and-relinking",
            "objective": "list-reversal-preserve-suffix",
            "scenario": scenario("reversal-core", "Reverse 1, 2, 3", "reverse_iterative rewrites next links. The list that started as 1, 2, 3 ends as 3, 2, 1.", computed_frames("linked-list-reversal-and-relinking")),
            "idea": "Reversal rearranges a chain by changing next references, not by copying values. Before you overwrite a link, save the node that follows it. Otherwise the unvisited suffix becomes unreachable. reverse_iterative keeps three names. previous is the reversed prefix. current is the node being flipped. upcoming is the saved suffix. The library starts previous empty and current at the head. Each step saves current.next, points current.next at previous, then advances both moving names. When current is empty, previous is the new head. On 1, 2, 3 the result is 3, 2, 1. Pair and block reversal reuse the same invariant. They must also reconnect the previous block to the new head of the current block, and connect that block's tail to the untouched suffix. Rotation finds a new tail, makes the chain temporarily circular, then cuts it. Partition and odd-even grouping keep separate tails, then join the chains.",
            "why": "The invariant is that previous is a reversed chain of the nodes already visited, and current still heads the original suffix. It holds at the start because the prefix is empty and current is the whole list. One step moves current onto the prefix and leaves upcoming as the rest, so the invariant holds again. No node is dropped because upcoming was saved before the write. The loop stops when current is empty, so every node is on the reversed prefix. A recursive reversal rewrites the same links and can use a linear call stack. The iterative version stores three references. For every pointer write, name which node still owns the remaining suffix.",
            "cost": "The loop body runs once per node. Each iteration reads and writes a constant number of pointers, so the time is linear and the reversal itself uses constant extra memory. require_linear can hold a set of ids while it runs, and that peak is separate from the three pointers. A recursive version adds a linear stack. Trace an empty list, a one-node list, a two-node list, and a block size larger than the list. A linear input must stay linear, and every original node must appear once.",
        },
        {
            "slug": "linked-list-merge-and-sort",
            "objective": "list-merge-head-order",
            "scenario": scenario("list-merge-core", "Merge 1, 4 with 2, 3", "merge_sorted relinks the existing nodes. The result is 1, 2, 3, 4, and both inputs are left empty.", computed_frames("linked-list-merge-and-sort")),
            "idea": "When two chains are sorted, compare only their current heads. Take the smaller head, append it to the result, and advance that input. When one input is empty, attach the other suffix. It is already in order. merge_sorted of 1, 4 and 2, 3 returns 1, 2, 3, 4. Ties use a strict less-than against the second list, so an equal key from the first list stays in front. The nodes are relinked, not copied into a second array of values. Both inputs are left empty because their nodes now belong to the result. Merging a list with itself is rejected, because that would build a cycle. Bottom-up merge sort repeats this combine on adjacent runs of width 1, then 2, then 4. A linked list has no random-access middle, so this width schedule fits it better than a top-down split that indexes the midpoint.",
            "why": "Each step appends the smaller remaining head, so nothing still in either chain is smaller than the item just written. The attached suffix is sorted by the precondition, and it sits after a head that was smaller than its own head. Taking the first list on a tie keeps the earlier equal key in front. The inputs end empty because the same node objects moved. Intersection is a different question. After both chains are linear, equalize the distance to the ends and advance together. Compare node identity, not equal values. The guard that checks the chains has its own cost.",
            "cost": "A merge of lengths n and m does a linear number of comparisons and link updates. The result list object is constant extra memory, because the nodes are reused. Bottom-up sort has a logarithmic number of rounds, and each round visits every node, so the time is n log n. Auxiliary node references beyond the list nodes can stay constant. Repeatedly indexing the middle of a linked list would pay a linear walk per index and would lose the array-style access assumption. Count that walk if you choose it.",
        },
        {
            "slug": "linked-list-special-cases",
            "objective": "list-state-preconditions",
            "scenario": scenario("special-cases-core", "Two places from the end of 1, 2, 3, 4", "nth_from_end counts the tail as 1. A gap of 2 on this list lands on 3.", computed_frames("linked-list-special-cases")),
            "idea": "Some linked-list routines are valid only under a contract that is easy to miss. Values may be sorted. Digits may be stored least-significant digit first. A circular list may have a distinguished head. The function may receive one node and not the list head. nth_from_end makes its contract explicit. n is 1-based, and 1 means the tail. On 1, 2, 3, 4, nth_from_end with n equal to 2 returns the node holding 3. The leader walks n steps first, and then both pointers walk together. When the leader falls off, the trailer is the requested node. Removing adjacent duplicates in a sorted list needs only a neighbor comparison. The sorted precondition is what makes that enough. An unsorted list needs a set of seen values, which changes the memory. Deleting a node without the list head can copy the successor and bypass it. That trick cannot remove the tail, because there is no successor to copy. Adding numbers stored least-significant digit first can walk both heads and carry one digit.",
            "why": "The gap stays n because both pointers move one step after the leader's head start. The trailer therefore sits n nodes behind the leader for the rest of the walk. No length subtraction is required. The sorted-duplicate claim fails as soon as an inversion exists, because a later duplicate is not beside its earlier copy. The headless delete fails on the tail for a structural reason, not an off-by-one. There is no next node whose value can be copied back. A circular split is wrong if either result is linear or if the two cycles share a node. Name the input shape, the output shape, and whether existing nodes are mutated.",
            "cost": "The leader takes n steps and then both pointers take the remaining steps. The total is linear in the length. Extra memory for the gap is two references. Counting the length and then walking length minus n is the same linear bound. The gap removes the subtraction, not the scan. A set of seen values for unsorted duplicates is linear extra memory. Copying a successor is constant time only when the successor exists. Test the empty list, one node, the last node, a duplicate run, and the smallest valid cycle or digit list.",
        },
        {
            "slug": "doubly-linked-list-operations",
            "objective": "doubly-linked-update-neighbors",
            "scenario": scenario("doubly-core", "Unlink a known node", "append a, then b. remove_node on the node for a returns a, and the list that remains is b.", computed_frames("doubly-linked-list-operations")),
            "idea": "A doubly linked node stores prev and next. If you already hold the node, you do not walk from the head to find its neighbors. remove_node on the node for a, in a list that also holds b, returns a and leaves b. The unlink follows prev and next and rewires those neighbors to each other. insert_after splices a new node between a known node and that node's next. Both directions must be written. A missing reverse link makes a forward walk and a backward walk disagree. Finding a node by value is still linear, unless another structure stores the node. Sentinels are one way to make every real node have neighbors, including the empty list. This list keeps a head and a tail instead, and the endpoint cases update those caches.",
            "why": "The known-node claim is that the predecessor and the successor are fields, not search results. Rewiring them restores a single chain. The forward neighbor's prev and the backward neighbor's next must both change, or one direction still points at the removed node. insert_after writes the new node's two links and the two neighboring links that should point at it. That is four pointers when both neighbors exist. An endpoint has a missing neighbor, so the list updates head or tail instead of a second node. The size cache changes by one. After the edit, a walk from the head and a walk from the tail must list the same nodes in opposite orders.",
            "cost": "Unlinking or inserting beside a known node is a constant number of pointer writes. It is constant time. A singly linked delete of an arbitrary node is linear, because the predecessor must be found from the head. A search by value on this list is still linear. n such searches are quadratic if you repeat them. Extra memory is one node per item plus the list caches. Draw both directions after a removal. Test an empty list and a one-node list, and check that head and tail still agree.",
        },
    ]


def all_specs() -> list[dict[str, object]]:
    return [*LESSONS, *more_lessons(), *batch_a(), *batch_specs(), *final_lessons()]


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
        **EXTRA_QUESTIONS,
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
        "cost-models": {
            "prompt": "Binary search does a logarithmic number of comparisons. Where is the elapsed work also logarithmic?",
            "options": [("list", "On a Python list, because each index is constant time"), ("chain", "On a singly linked list, because the middle is one hop"), ("either", "On either structure, because only the comparison count matters")],
            "answer": "list",
            "correct": "Each middle index on a list is one address calculation.",
            "retry": "A linked list walks from the head to reach the middle.",
            "hints": ["Ask what an index costs on each structure.", "The comparison count is not the elapsed work."],
            "more": [{
                "suffix": "transfer",
                "objective": "cost-model-python-operations",
                "prompt": "list_pop_front_cost_demo(3) counts one pop(0). What does it return?",
                "options": [("two", "2 reference moves, one per item still in the list"), ("three", "3 reference moves, one per original item"), ("one", "1 reference move, only the removed item")],
                "answer": "two",
                "correct": "A list of length 3 moves the 2 items that remain.",
                "retry": "The removed item does not slide. The items behind it do.",
                "hints": ["The function returns length minus 1.", "Length 3 leaves 2 items to slide."],
            }],
        },
        "fast-slow-pointer-patterns": {
            "prompt": "middle_node walks 1, 2, 3, 4, 5. Where does the slow pointer stop?",
            "options": [("middle", "On the single middle node of that five-node list"), ("tail", "On the last node, because the fast pointer finishes there"), ("head", "On the first node, because the slow pointer starts there")],
            "answer": "middle",
            "correct": "Fast moves two steps and slow moves one, so slow stops in the middle.",
            "retry": "Slow does not stay on the head, and it does not chase fast all the way to the end.",
            "hints": ["Count steps, not node values.", "An odd length has one middle."],
            "more": [{
                "suffix": "transfer",
                "objective": "fast-slow-preserve-gap",
                "prompt": "A lead pointer starts two steps ahead of a trailer. When the lead falls off, where is the trailer?",
                "options": [("gap", "Two nodes behind the end, because the gap never changes"), ("head", "On the head, because only the lead pointer moves"), ("tail", "On the tail, because the lead pointer is the position you want")],
                "answer": "gap",
                "correct": "Both pointers move together after the lead's head start, so the gap stays two.",
                "retry": "The trailer moves. It just stays a fixed number of nodes behind the lead.",
                "hints": ["The gap is set before the joint walk.", "nth_from_end uses this gap."],
            }],
        },
        "linked-list-reversal-and-relinking": {
            "prompt": "You are about to overwrite a node's next link. What must you save first?",
            "options": [("suffix", "The untouched suffix, or that suffix becomes unreachable"), ("prefix", "Only the reversed prefix, because the suffix stays indexed"), ("nothing", "Nothing, because a tail pointer remembers every later node")],
            "answer": "suffix",
            "correct": "The upcoming node is the only reference to the rest of the chain.",
            "retry": "A singly linked node does not remember its old next after you write a new one.",
            "hints": ["Draw three nodes and erase the first next arrow.", "Ask which name still points at the node you have not reversed."],
            "more": [{
                "suffix": "transfer",
                "objective": "list-relink-boundary-reconnection",
                "prompt": "A block reversal finishes a block. Which link is the extra boundary write?",
                "options": [("join", "The previous block must point at the new head of the block just reversed"), ("skip", "No extra write, because the whole list is one block"), ("tail", "The head of the list must point at the old tail of this block")],
                "answer": "join",
                "correct": "The reversed block has a new head, and the node before the block must follow it.",
                "retry": "Reversing inside the block does not update the node that pointed at the old head.",
                "hints": ["The three-pointer loop fixes links inside the block.", "The node before the block is outside that loop."],
            }],
        },
        "linked-list-merge-and-sort": {
            "prompt": "The current heads are 1 and 2. Which node is taken first?",
            "options": [("smaller", "The smaller head, the node holding the lesser key"), ("larger", "The larger head, so the result is descending"), ("both", "Both heads in one step, then the loop stops")],
            "answer": "smaller",
            "correct": "A sorted merge appends the smaller remaining head.",
            "retry": "Do not concatenate the chains, and do not prefer the larger key.",
            "hints": ["Only the two fronts are compared.", "The leftover chain is attached at the end."],
            "more": [{
                "suffix": "transfer",
                "objective": "list-merge-sort-cost",
                "prompt": "Bottom-up merge sort runs a logarithmic number of rounds, and each round visits every node. What is the total?",
                "options": [("nlog", "n log n, because every round is linear"), ("linear", "Linear, because a linked list has no indexes"), ("square", "Quadratic, because each comparison scans a chain")],
                "answer": "nlog",
                "correct": "A logarithmic number of linear rounds is n log n.",
                "retry": "The missing indexes do not remove the work of walking each run.",
                "hints": ["Widths go 1, 2, 4, and so on.", "Each width still touches every node."],
            }],
        },
        "linked-list-special-cases": {
            "prompt": "A function may delete a node when it is given only that node. Which node can it not delete this way?",
            "options": [("tail", "The tail, because there is no successor value to copy"), ("head", "The head, because the head value is always copied forward"), ("middle", "Any middle node, because the predecessor is required")],
            "answer": "tail",
            "correct": "The trick copies the successor and bypasses it. The tail has no successor.",
            "retry": "A middle node has a successor. The tail does not.",
            "hints": ["The function was not given the list head.", "Copying a value requires a next node."],
            "more": [{
                "suffix": "transfer",
                "objective": "list-special-boundary-tests",
                "prompt": "nth_from_end uses a gap of 2 on the list 1, 2, 3, 4. Which position does the trailer hold when the leader falls off?",
                "options": [("back", "Two places before the end"), ("end", "The tail, because the count starts at zero"), ("front", "The head, because the trailer never moves")],
                "answer": "back",
                "correct": "The leader takes two steps first, and the gap stays two.",
                "retry": "n is 1-based. A gap of 2 is not the tail and not the head on this list.",
                "hints": ["1 means the tail.", "Both pointers move after the gap is opened."],
            }],
        },
        "doubly-linked-list-operations": {
            "prompt": "You insert a node between two existing neighbors. How many pointers must change?",
            "options": [("four", "Four pointers, both directions on both sides of the splice"), ("one", "One pointer, only the forward link of the left neighbor"), ("two", "Two pointers, only the new node's own links")],
            "answer": "four",
            "correct": "The new node points both ways, and each neighbor must point back at it.",
            "retry": "Writing only the new node's links leaves the neighbors pointing at each other.",
            "hints": ["Each side of a doubly linked node has a back link.", "An endpoint is the case with a missing neighbor."],
            "more": [{
                "suffix": "transfer",
                "objective": "doubly-linked-known-node-unlink",
                "prompt": "You already hold the node. What does remove_node cost?",
                "options": [("constant", "Constant time, because prev and next are stored on the node"), ("linear", "Linear time, because the list walks from the head"), ("square", "Quadratic time, because both directions are scanned")],
                "answer": "constant",
                "correct": "The neighbors are fields. Nothing searches for them.",
                "retry": "A walk from the head is the cost of finding the node, which this call does not do.",
                "hints": ["The argument is the node, not the value.", "A singly linked predecessor is not stored."],
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
        if slug in partial:
            continue
        partial[slug] = _choice(slug, objective, prompt, correct, wrong_a, wrong_b)
    from guide_checkpoint_copy import CHECKS

    for slug, fields in CHECKS.items():
        item = partial[slug]
        item["correct"] = fields["why"]
        item["retry"] = fields["retry"]
        item["hints"] = fields["hints"]
        item["more"] = [fields["more"]]
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
        matches = [
            path
            for path in GUIDE.glob("*.md")
            if path.stem.partition("-")[0].isdigit() and path.stem.partition("-")[2] == slug
        ]
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
    for item in exercises:
        if "kind" not in item:
            item["kind"] = "choice"
    predict = {
        "input-size-and-operation-counts-transfer": ("print(4 * 3 // 2)", "6", "4", "12"),
        "stack-basics-transfer": ("print([1, 2].pop())", "2", "1", "3"),
        "queue-and-deque-operations-transfer": ("from collections import deque\nitems = deque(['a', 'b'])\nitems.popleft()\nitems.append('c')\nprint(items.popleft())", "b", "a", "c"),
        "dynamic-programming-memory": ("print(8)", "8", "13", "5"),
    }
    for item in exercises:
        coded = predict.get(str(item["id"]))
        if not coded:
            continue
        code, right, wrong_a, wrong_b = coded
        item["kind"] = "predict-output"
        item["code"] = code
        item["options"] = [
            {"id": "yes", "label": right},
            {"id": "no", "label": wrong_a},
            {"id": "other", "label": wrong_b},
        ]
        item["answer"] = "yes"
        if item["id"] not in {"dynamic-programming-memory", "input-size-and-operation-counts-transfer"}:
            item["prompt"] = "What does this code print?"
            item["correct"] = f"The code prints {right}."
            item["retry"] = f"The printed value is {right}."
            item["hints"] = [f"The code prints one value, {right}.", "Ignore the values that are not printed."]
    heap = next(item for item in exercises if item["id"] == "heap-operations-transfer")
    heap_frame = traces["heap-operations"][0]["frames"][0]
    heap["kind"] = "fill-cell"
    heap["frameLabel"] = heap_frame["label"]
    heap["rowLabel"] = heap_frame["rows"][0]["label"]
    heap["cellIndex"] = 0
    cell_text = str(heap_frame["rows"][0]["cells"][0]["text"])
    heap["options"] = [
        {"id": "shown", "label": cell_text},
        {"id": "other", "label": "99"},
        {"id": "missing", "label": "missing"},
    ]
    heap["answer"] = "shown"
    heap["prompt"] = "Which value belongs in the named cell?"
    heap["correct"] = f"The cell shows {cell_text}."
    heap["retry"] = f"The named cell is {cell_text}."
    from lesson_frames import frames_for

    answer_frames = frames_for("binary-search-on-answer")
    if answer_frames is None:
        raise SystemExit("binary-search-on-answer trace missing")
    traces["binary-search-on-answer"] = [{
        "id": "binary-search-on-answer-core",
        "title": "Rates for piles 3, 6, 7, 11",
        "prompt": "The library tests rates 6, 3, and 4, then returns 4.",
        "frames": answer_frames,
    }]
    for slug, scenes in traces.items():
        count = sum(len(scene["frames"]) for scene in scenes)
        if count < 3 or count > 12:
            raise SystemExit(f"{slug} has {count} frames")
        previous = None
        for scene in scenes:
            for frame_item in scene["frames"]:
                narration = str(frame_item["narration"])
                if "recorded" in narration:
                    raise SystemExit(f"{slug} narration says recorded")
                signature = (frame_item["state"], narration)
                if signature == previous:
                    raise SystemExit(f"{slug} repeats a frame")
                previous = signature
    for item in exercises:
        place_options(item)
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
