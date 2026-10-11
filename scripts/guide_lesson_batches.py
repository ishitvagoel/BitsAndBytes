"""Specs for the summary lessons that follow the first generated batch.

Every number in a frame is the return value of a library call made in this file.
"""

from __future__ import annotations

from bitsandbytes.approximate.structures import BloomFilter
from bitsandbytes.backtracking.search import permutations
from bitsandbytes.dynamic_programming.classic import knapsack_01, min_coin_change
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import (
    bellman_ford_distances,
    dijkstra_distances_heap,
    floyd_warshall,
    has_directed_cycle,
    is_bipartite,
    kosaraju_strongly_connected_components,
    kruskal_minimum_spanning_weight,
    prim_minimum_spanning_weight,
    topological_order,
    zero_one_bfs_distances,
)
from bitsandbytes.graphs.algorithms import UndirectedGraph
from bitsandbytes.greedy.classic import huffman_codes, interval_scheduling_max_count
from bitsandbytes.hash_tables.linear_probing import LinearProbingHashTable
from bitsandbytes.heaps.priority_queue import PriorityQueue
from bitsandbytes.limits.approximation import vertex_cover_two_approximation
from bitsandbytes.linked_lists.lru_cache import LRUCache
from bitsandbytes.patterns.arrays import PrefixSum, longest_unique_substring_length, sliding_window_maximum, two_sum_sorted
from bitsandbytes.range_queries.structures import FenwickTree, SegmentTree, SparseTable
from bitsandbytes.sorting.selection_and_radix import counting_sort, inversion_count, lsd_radix_sort, quickselect
from bitsandbytes.stacks.infix_postfix import evaluate_infix, infix_to_postfix
from bitsandbytes.stacks.largest_rectangle import largest_rectangle
from bitsandbytes.stacks.min_stack import MinStack
from bitsandbytes.stacks.next_greater import next_greater
from bitsandbytes.stacks.stock_span import stock_spans
from bitsandbytes.stacks.symbol_balance import symbols_are_balanced
from bitsandbytes.storage.engines import BTree, sequential_scan_sum
from bitsandbytes.strings.algorithms import Trie, kmp_search, rabin_karp_search, suffix_array_with_lcp
from bitsandbytes.trees.bst import BinarySearchTree
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree
from bitsandbytes.trees.traversals import level_order, postorder, preorder


def cell(text: str, status: str = "idle") -> dict[str, str]:
    return {"text": text, "status": status}


def frame(label: str, narration: str, state: list[tuple[str, str]], values: list[object], status: str) -> dict[str, object]:
    return {
        "label": label,
        "narration": narration,
        "state": [{"name": name, "value": value} for name, value in state],
        "rows": [{"label": "State", "cells": [cell(str(item), status) for item in values]}],
    }


def scenario(title: str, prompt: str, frames: list[dict[str, object]]) -> dict[str, object]:
    return {"id": "pending", "title": title, "prompt": prompt, "frames": frames}


def ask(
    prompt: str,
    yes: str,
    no: str,
    other: str,
    feedback: str,
    retry: str,
    hints: list[str],
    transfer_objective: str,
    transfer_prompt: str,
    transfer_yes: str,
    transfer_no: str,
    transfer_other: str,
    transfer_feedback: str,
    transfer_retry: str,
) -> dict[str, object]:
    return {
        "prompt": prompt,
        "options": [("yes", yes), ("no", no), ("other", other)],
        "answer": "yes",
        "correct": feedback,
        "retry": retry,
        "hints": hints,
        "more": [{
            "suffix": "transfer",
            "objective": transfer_objective,
            "prompt": transfer_prompt,
            "options": [("yes", transfer_yes), ("no", transfer_no), ("other", transfer_other)],
            "answer": "yes",
            "correct": transfer_feedback,
            "retry": transfer_retry,
            "hints": ["Use the same rule on this new question.", "Reject the choice that changes the rule."],
        }],
    }


def _tree() -> BinarySearchTree[int]:
    tree = BinarySearchTree()
    for value in (4, 2, 6, 1):
        tree.insert(value)
    return tree


def _frames() -> dict[str, list[dict[str, object]]]:
    greater = next_greater([2, 1, 2, 4, 3])
    assert greater == [4, 2, 4, None, None]
    assert stock_spans([100, 80, 60, 70, 60, 75, 85])[5] == 4
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    low = MinStack()
    low.push(3)
    low.push(1)
    low.push(2)
    assert low.minimum() == 1 and low.pop() == 2 and low.minimum() == 1

    assert symbols_are_balanced("([])") is True
    assert symbols_are_balanced("([)]") is False
    assert infix_to_postfix("2+3*4") == ["2", "3", "4", "*", "+"]
    assert evaluate_infix("2+3*4") == 14

    assert counting_sort([3, 1, 2, 1], maximum=3) == [1, 1, 2, 3]
    assert lsd_radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]
    selected = [3, 1, 4, 2]
    assert quickselect(selected, 0) == 1
    assert quickselect([3, 1, 4, 2], 2) == 3
    assert inversion_count([3, 1, 4, 2]) == 3

    probed = LinearProbingHashTable(capacity=4)
    probed[0] = 1
    probed[4] = 2
    assert list(probed._keys[:2]) == [0, 4]
    del probed[0]
    assert probed[4] == 2 and probed._keys[0] is not None and probed._keys[0] != 0

    cache = LRUCache[str, int](2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None and cache.get("a") == 1 and cache.get("c") == 3

    tree = _tree()
    assert preorder(tree.root) == [4, 2, 1, 6]
    assert postorder(tree.root) == [1, 2, 6, 4]
    assert level_order(tree.root) == [4, 2, 6, 1]

    balanced = LeftLeaningRedBlackTree()
    for value in (1, 2, 3):
        balanced.insert(value)
    assert balanced.inorder() == [1, 2, 3]
    assert balanced.root is not None and balanced.root.key == 2
    assert balanced.select(1) == 2 and balanced.rank(2) == 1

    queue = PriorityQueue[str]()
    queue.push(5, "a")
    queue.push(3, "b")
    queue.push(4, "c")
    assert queue.pop() == (3, "b")

    listed = Graph()
    listed.add_edge("A", "B", 1)
    listed.add_edge("A", "C", 1)
    listed.add_edge("B", "D", 1)
    vertex_count = len(list(listed.vertices()))
    edge_count = sum(len(listed.neighbors(vertex)) for vertex in listed.vertices())
    assert (vertex_count, edge_count) == (4, 3)

    ordered = Graph()
    ordered.add_edge("A", "B", 1)
    ordered.add_edge("A", "C", 1)
    ordered.add_edge("B", "D", 1)
    ordered.add_edge("C", "D", 1)
    assert topological_order(ordered) == ["A", "B", "C", "D"]
    assert has_directed_cycle(ordered) is False
    cyclic = Graph()
    cyclic.add_edge("A", "B", 1)
    cyclic.add_edge("B", "A", 1)
    assert has_directed_cycle(cyclic) is True
    try:
        topological_order(cyclic)
    except ValueError:
        pass
    else:
        raise AssertionError("a cycle must not produce a full order")

    weighted = Graph()
    weighted.add_edge("A", "B", 1)
    weighted.add_edge("A", "C", 4)
    weighted.add_edge("B", "C", 2)
    assert dijkstra_distances_heap(weighted, "A")["C"] == 3
    negative = Graph()
    negative.add_edge("A", "B", 1)
    negative.add_edge("B", "C", -2)
    assert bellman_ford_distances(negative, "A")["C"] == -1
    path = Graph()
    path.add_edge("A", "B", 1)
    path.add_edge("B", "C", 1)
    assert zero_one_bfs_distances(path, "A")["C"] == 2
    assert floyd_warshall(path)["A"]["C"] == 2
    triangle = Graph()
    triangle.add_edge("A", "B", 1)
    triangle.add_edge("B", "C", 1)
    triangle.add_edge("C", "A", 1)
    assert is_bipartite(path) is True
    assert is_bipartite(triangle) is False
    assert kosaraju_strongly_connected_components(triangle) == [["A", "C", "B"]]

    undirected = UndirectedGraph()
    undirected.add_edge("A", "B", 1)
    undirected.add_edge("B", "C", 2)
    undirected.add_edge("A", "C", 4)
    assert prim_minimum_spanning_weight(undirected, "A") == 3
    assert kruskal_minimum_spanning_weight(undirected) == 3

    assert two_sum_sorted([1, 2, 4, 7], 6) == (1, 2)
    assert longest_unique_substring_length("abcabcbb") == 3
    assert sliding_window_maximum([1, 3, 2, 5], 2) == [3, 3, 5]
    assert PrefixSum([1, 2, 3, 4]).range_sum(1, 3) == 5
    assert len(permutations([1, 2, 3])) == 6
    assert interval_scheduling_max_count([(1, 3, "a"), (2, 4, "b"), (3, 5, "c")]) == 2
    assert huffman_codes({"a": 3, "b": 1, "c": 1})["a"] == "1"
    assert min_coin_change([1, 3, 4], 6) == 2
    assert knapsack_01([1, 3], [2, 4], 4) == 6
    assert kmp_search("ababcababa", "ababa") == 5
    assert rabin_karp_search("ababcababa", "ababa") == 5
    suffixes, lcp = suffix_array_with_lcp("banana")
    assert suffixes == [5, 3, 1, 0, 4, 2] and lcp[2] == 3
    trie = Trie()
    trie.insert("cat")
    trie.insert("car")
    assert trie.contains("car") is True and trie.contains("ca") is False
    bits = FenwickTree(4)
    bits.add(0, 1)
    bits.add(1, 2)
    bits.add(2, 3)
    assert bits.prefix_sum(2) == 6
    segment = SegmentTree([1, 2, 3, 4])
    segment.range_add(1, 2, 5)
    assert segment.point_query(1) == 7 and segment.point_query(0) == 1
    assert SparseTable([1, 3, 2, 4]).range_min(1, 3) == 2
    bloom = BloomFilter(bit_count=64, hash_count=3, seed=0)
    bloom.add("cat")
    assert bloom.maybe_contains("cat") is True
    btree = BTree()
    btree.insert(2)
    btree.insert(1)
    assert btree.search(1) is True and btree.search(9) is False
    assert sequential_scan_sum([1, 2, 3]) == 6
    cover_graph = Graph()
    cover_graph.add_edge("A", "B", 1)
    cover_graph.add_edge("C", "D", 1)
    assert vertex_cover_two_approximation(cover_graph) == {"A", "B", "C", "D"}

    return {
        "monotonic-stack-patterns": [
            frame("Answers", "next_greater writes the first strictly larger value on the right.", [("first", "4")], greater, "chosen"),
            frame("Area", "The largest rectangle in this histogram has area 10.", [("area", "10")], [2, 1, 5, 6, 2, 3], "active"),
        ],
        "stack-parsing-and-expressions": [
            frame("Brackets", "([]) is balanced. ([)] crosses pairs and is not.", [("balanced", "yes")], ["(", "[", "]", ")"], "done"),
            frame("Postfix", "Multiplication leaves the operator stack before addition.", [("value", "14")], ["2", "3", "4", "*", "+"], "chosen"),
        ],
        "noncomparison-sorts": [
            frame("Counts", "counting_sort places keys by value, not by comparing neighbors.", [("maximum", "3")], [1, 1, 2, 3], "done"),
            frame("Digits", "Least-significant digit passes keep equal-digit order.", [("base", "10")], [2, 24, 45, 66], "active"),
        ],
        "order-statistic-selection": [
            frame("Smallest", "quickselect with k = 0 returns the minimum.", [("k", "0")], [1], "chosen"),
            frame("Third", "k = 2 is the third smallest key, which is 3.", [("k", "2")], [3], "active"),
        ],
        "inversion-counting": [
            frame("Pairs", "Three pairs are out of order in 3, 1, 4, 2.", [("count", "3")], [3, 1, 4, 2], "chosen"),
        ],
        "hash-linear-probing": [
            frame("Probe", "Key 4 finds slot 0 full and takes the next slot.", [("capacity", "4")], [0, 4], "active"),
            frame("Tombstone", "Deleting 0 leaves a marker so the probe can still reach 4.", [("found", "2")], [4], "chosen"),
        ],
        "lru-cache": [
            frame("Evict", "b was the least recent key, so c replaces it.", [("miss", "b")], ["a", "c"], "chosen"),
        ],
        "tree-traversals": [
            frame("Preorder", "Visit the node before either child.", [("root", "4")], [4, 2, 1, 6], "active"),
            frame("Levels", "A queue visits each depth before the next.", [("root", "4")], [4, 2, 6, 1], "done"),
        ],
        "balanced-search-trees": [
            frame("Root", "Sorted inserts still leave 2 at the root.", [("root", "2")], [1, 2, 3], "chosen"),
        ],
        "priority-queues": [
            frame("Pop", "The smallest priority leaves first.", [("item", "b")], [3, 4, 5], "chosen"),
        ],
        "graph-representations": [
            frame("Edges", "Three adjacency-list pairs store this graph.", [("vertices", "4")], ["A", "B", "C", "D"], "idle"),
        ],
        "topological-order": [
            frame("Order", "Kahn's algorithm emits every vertex once.", [("start", "A")], ["A", "B", "C", "D"], "done"),
        ],
        "shortest-paths": [
            frame("Relax", "The path through B beats the direct edge into C.", [("distance", "3")], ["A", "B", "C"], "chosen"),
        ],
        "minimum-spanning-trees": [
            frame("Skip", "The weight-4 edge closes a cycle and is rejected.", [("weight", "3")], [1, 2], "chosen"),
        ],
        "two-pointers": [
            frame("Pair", "Indexes 1 and 2 hold 2 and 4, which sum to 6.", [("target", "6")], [1, 2, 4, 7], "chosen"),
        ],
        "sliding-window": [
            frame("Windows", "Each window of length 2 reports its maximum.", [("window", "2")], [3, 3, 5], "active"),
        ],
        "prefix-sums": [
            frame("Range", "The half-open slice from 1 to 3 sums to 5.", [("sum", "5")], [1, 2, 3, 4], "chosen"),
        ],
        "backtracking": [
            frame("Leaves", "Three distinct items have six permutations.", [("count", "6")], [1, 2, 3], "done"),
        ],
        "greedy-methods": [
            frame("Schedule", "Sorting by finish time keeps two compatible intervals.", [("count", "2")], ["a", "c"], "chosen"),
        ],
        "dp-state-and-transition": [
            frame("Coins", "Amount 6 needs two coins from 1, 3, and 4.", [("coins", "2")], [1, 3, 4], "chosen"),
        ],
        "string-search": [
            frame("Match", "The first full match of ababa starts at index 5.", [("index", "5")], ["a", "b", "a", "b", "a"], "chosen"),
        ],
        "tries-and-text-indexes": [
            frame("Keys", "car is a stored key. ca is only a prefix.", [("hit", "car")], ["c", "a", "r"], "active"),
        ],
        "range-query-structures": [
            frame("Prefix", "The Fenwick prefix through index 2 is 6.", [("sum", "6")], [1, 2, 3], "chosen"),
        ],
        "approximate-membership": [
            frame("Membership", "cat was inserted, so every bit it hashes to is set.", [("cat", "maybe")], ["cat"], "chosen"),
        ],
        "storage-engines-and-locality": [
            frame("Scan", "A sequential sum touches 1, 2, and 3 in order.", [("sum", "6")], [1, 2, 3], "done"),
        ],
        "approximation-guarantees": [
            frame("Cover", "Each uncovered edge contributes both endpoints.", [("edges", "2")], ["A", "B", "C", "D"], "chosen"),
        ],
    }


_BUILT = _frames()


def _spec(slug: str, objective: str, title: str, prompt: str, idea: str, why: str, cost: str) -> dict[str, object]:
    return {
        "slug": slug,
        "objective": objective,
        "scenario": scenario(title, prompt, _BUILT[slug]),
        "idea": idea,
        "why": why,
        "cost": cost,
    }


def batch_specs() -> list[dict[str, object]]:
    return [
        _spec(
            "monotonic-stack-patterns",
            "monotonic-stack-resolve-candidates",
            "Next greater values and a histogram",
            "next_greater on 2, 1, 2, 4, 3 returns 4, 2, 4, None, None. The histogram area is 10.",
            "A monotonic stack stores indexes that are still waiting for an answer. next_greater on 2, 1, 2, 4, 3 returns 4, 2, 4, None, and None. The stack holds indexes. When a larger value arrives, every index it beats is popped and that value is written as the answer. Indexes that remain at the end have no strictly greater value on their right. stock_spans uses the same waiting stack. On prices 100, 80, 60, 70, 60, 75, 85 the span at the 75 is 4, because the walk stops at a strictly higher price. largest_rectangle asks for the nearest shorter bar on each side. The area is height times the gap between those bars. On 2, 1, 5, 6, 2, 3 the largest area is 10. min_stack keeps the current minimum beside the values. After pushing 3, then 1, then 2, the minimum is 1, and it is still 1 after 2 is popped. sort_stack uses a second stack so each moved value lands in order. The shared rule is that a value leaves the stack only when a later value resolves it.",
            "The stack stays ordered by the values at the stored indexes. A new value pops while the top is strictly smaller, so the top is the nearest unresolved candidate. Each pop writes an answer that will not change, because a later value is even farther to the right. The final leftovers are the positions with no greater neighbor, which is why their answers stay empty. The histogram uses two boundaries. A bar's width runs from the previous shorter bar to the next shorter bar, excluding those bars. Multiplying by the bar's height counts the rectangle that bar can support. The total work stays linear because each index is pushed once and popped at most once. The inner loop does not restart from the left.",
            "n indexes produce at most n pushes and n pops, so the time is linear and the stack uses linear extra memory. A fresh scan from each index would be quadratic. largest_rectangle is the same bound. One pass finds the next smaller bar and one pass finds the previous smaller bar. min_stack push, pop, and minimum are constant time because the minimum is stored, not searched. Use this pattern when every item waits for a later item and then never waits again.",
        ),
        _spec(
            "stack-parsing-and-expressions",
            "stack-match-nested-delimiters",
            "Balanced brackets and operator precedence",
            "([]) is balanced and ([)] is not. 2+3*4 becomes 2 3 4 * + and evaluates to 14.",
            "A bracket stack stores unmatched opening marks. symbols_are_balanced pushes each opener and pops when a closer arrives. The closer must match the current top. Other characters are ignored, so a formula and a bare bracket string share one checker. ([]) is balanced. ([)] is not, because the closer for the square bracket arrives while the parenthesis is still on top. An empty string is balanced. A leftover opener is not. Operator precedence uses a second stack. infix_to_postfix turns 2+3*4 into the tokens 2, 3, 4, *, +. Multiplication leaves the operator stack before addition because it binds more tightly. evaluate_infix of that expression returns 14. The value stack applies an operator only when both of its operands are already values. That is why postfix does not need parentheses.",
            "The bracket invariant is that the stack, from bottom to top, is the unmatched openers in the order they appeared. A matching closer restores the invariant by removing the top. A crossing closer breaks it, and the function returns false immediately. Termination with an empty stack means every opener found its closer. The operator invariant is that the operator stack is ordered by precedence, tightest at the top. Seeing a looser operator pops the tighter ones into the output first. The final pops drain the remaining operators. 3 * 4 happens before the addition with 2, so the value is 14.",
            "Each character is pushed or popped at most once, so both scans are linear in the length of the expression. Extra memory is the unmatched openers or the pending operators, which is linear in the worst case and small when the expression stays nested cleanly. A wrong match is a constant-time rejection. Do not scan backward for the opener. The stack already has it.",
        ),
        _spec(
            "noncomparison-sorts",
            "noncomparison-use-key-range",
            "Counting sort and digit passes",
            "counting_sort of 3, 1, 2, 1 with maximum 3 returns 1, 1, 2, 3. A radix pass keeps equal digits in their old order.",
            "Comparison sorts need a logarithmic number of comparisons per item in the worst case when they learn order only by comparing keys. Counting sort skips comparisons when the keys are integers in a known range. counting_sort of 3, 1, 2, 1 with maximum 3 returns 1, 1, 2, 3. It counts how many keys have each value, then writes them into those slots. Equal keys keep their order if the write walks the input from left to right into the next free slot of that count. That stability is what a radix sort needs. lsd_radix_sort of 170, 45, 75, 90, 802, 24, 2, 66 returns 2, 24, 45, 66, 75, 90, 170, 802. Each pass sorts by one digit, starting at the least significant digit, and the next pass must not scramble the order the previous pass built. The digit alphabet is the base, here 10.",
            "The count array is a correct histogram because every key increments exactly one slot. The prefix of those counts says where each value should start in the output. Writing a key into its slot and advancing the slot places each key once. Stability holds when equal keys are written in the order they appear in the input. A radix pass is a counting sort on one digit. After the least significant digit is stable, sorting the next digit groups larger place values without reordering keys that share that digit. The highest digit pass finishes the order.",
            "Counting sort is linear in the number of keys plus the size of the key range. A huge maximum with a tiny list still allocates the count array, so the range belongs in the bound. Radix sort repeats that cost once per digit. With a constant number of digits the total is linear in the number of keys. Extra memory is the count array and the output. These sorts are the right tool for integers or fixed-width strings, not for arbitrary ordered objects.",
        ),
        _spec(
            "order-statistic-selection",
            "selection-trace-quickselect",
            "Quickselect on a small array",
            "quickselect uses the rightmost value as the pivot. k = 0 returns 1 and k = 2 returns 3 on 3, 1, 4, 2.",
            "An order statistic is the k-th smallest key, counting from zero. Sorting would find it, and would also order every other key. quickselect stops when the pivot lands on k. On a copy of 3, 1, 4, 2, quickselect with k = 0 returns 1. The same input with k = 2 returns 3, the third smallest key in 1, 2, 3, 4. The library partition always uses the rightmost value as the pivot. It walks the range once, swaps smaller keys toward the left boundary, and writes the pivot into the boundary. If that index is k, the pivot is the answer. If k is smaller, the search continues on the left side only. If k is larger, it continues on the right side only. The discarded side is not sorted.",
            "The partition invariant matches quicksort. Everything before the boundary is less than or equal to the pivot, and everything after it is greater. The pivot is therefore in its final sorted index even though the two sides are not sorted. The k-th smallest key must lie on the side that still contains index k. Throwing the other side away cannot hide the answer. The loop ends when the pivot index equals k, so the value sitting there is the order statistic.",
            "A balanced pivot throws away a constant fraction of the range, and the expected cost of that recurrence is linear. This implementation does not choose a random pivot. It always uses the right end. An input that always puts an extreme key at the right end shrinks the range by one item and the time becomes quadratic. Extra memory is a handful of indexes. Sort the whole array when you need every order statistic. Select when you need one.",
        ),
        _spec(
            "inversion-counting",
            "inversion-define-pair",
            "Count pairs that are out of order",
            "inversion_count on 3, 1, 4, 2 returns 3. The pairs are (3, 1), (3, 2), and (4, 2).",
            "An inversion is a pair of indexes i < j whose values are out of order, value i greater than value j. inversion_count on 3, 1, 4, 2 returns 3. The pairs are 3 before 1, 3 before 2, and 4 before 2. A sorted array has zero inversions. A reversed array has one inversion per pair. The library counts them while it merges, the same split merge sort uses. Inside one sorted run there are no new inversions. Every inversion that still matters has one endpoint in the left run and one in the right run. When the merge takes from the right run while the left run still has a smaller-index key waiting, that left key and every key still in the left run form inversions with the key just taken.",
            "The merge already knows both runs are sorted. If the right front is smaller, it is smaller than every remaining left key, not only the left front. Adding the number of remaining left keys counts those inversions in one step. Keys taken from the left form no cross inversion with the current right front. Splitting into halves and adding the inversions inside each half counts every pair exactly once. A pair inside a half is counted by the recursive call. A pair that crosses the midpoint is counted by the merge.",
            "The recurrence matches merge sort. A logarithmic number of levels each do linear work, so the time is n log n. Extra memory is the merged runs, which is linear, plus the call stack. Checking every pair directly is quadratic and needs no extra array. Use the merge when you want the count and a sorted copy together. The count is also a measure of how far the input is from sorted.",
        ),
        _spec(
            "hash-linear-probing",
            "hash-probing-trace-tombstones",
            "A collision, then a tombstone",
            "With capacity 4, keys 0 and 4 share a start slot. Deleting 0 leaves a tombstone and lookup of 4 still returns 2.",
            "Linear probing stores one key in each slot of an array. The hash picks a start slot. If that slot is occupied by a different key, the insert tries the next slot, then the next, wrapping at the end of the array. A LinearProbingHashTable with capacity 4 stores key 0 in slot 0. Key 4 has the same start slot, finds it full, and takes slot 1. Lookup of 4 repeats that probe and returns 2. Deleting 0 does not write an empty slot. It writes a tombstone. Lookup of 4 must skip the tombstone and continue, otherwise it would stop and miss a key that sits further along the same probe. An empty slot still means the key is absent. The table rehashes when the number of live keys would reach half the capacity, which keeps clusters shorter.",
            "The probe is a deterministic walk, so insert and lookup that start from the same hash follow the same slots. A tombstone is a slot that used to hold a key. It is not empty, because a later key may have stepped over it. Stopping at a tombstone would hide that later key. Stopping at an empty slot is safe, because an insert would have taken the first empty slot it saw. Rehashing copies every live key into a larger array and drops tombstones. The load factor is the number of live keys divided by the capacity.",
            "One probe is constant time when clusters stay short, and linear in the worst case when keys pile into one run. Primary clustering is that pile. A collision does not stay in one slot. It makes the next inserts more likely to collide too. Extra memory is the slot arrays, one per capacity, plus the tombstones that still occupy slots until a rehash. Keep the load factor bounded if you want the expected constant probe.",
        ),
        _spec(
            "lru-cache",
            "lru-trace-recency-and-eviction",
            "Evict the least recently used key",
            "A cache of capacity 2 stores a, then b, uses a, then stores c. b is the key that disappears.",
            "An LRU cache of capacity k keeps the k most recently used keys. The library uses two structures. A dictionary maps a key to the node that holds it. A doubly linked list orders those nodes by use. The head side is the most recent key and the tail side is the least recent. get moves a hit to the front. put of an existing key updates the value and moves that node to the front. put of a new key evicts the tail when the cache is already full, then inserts the new key at the front. Start with capacity 2. put a, put b, get a, put c. b was used before a, so b is the tail and c evicts it. get b then returns None. get a returns 1 and get c returns 3. A missing get returns None rather than raising.",
            "The recency order is the list order. Moving a node to the front is a constant-time unlink and insert because the node stores both neighbors. The dictionary is why get does not scan the list to find the node. Eviction removes the tail, which the list already knows, and deletes that key from the dictionary. After put c, the live keys are a and c. b is absent, so a later get cannot resurrect it. The capacity check happens before the new insert, so the size never stays above capacity.",
            "get and put are expected constant time. The dictionary lookup is expected constant time and the list edit is constant time. A cache that scanned a singly linked list of k nodes would pay linear time in the capacity on every eviction. Extra memory is one dictionary entry and one node per live key, so it is proportional to the capacity, not to the history of every key you have ever seen. Name both structures when you explain the bound. Either one alone is not enough.",
        ),
        _spec(
            "tree-traversals",
            "tree-traversal-predict-depth-first",
            "Preorder and level order of one tree",
            "Insert 4, 2, 6, 1. Preorder is 4, 2, 1, 6. Level order is 4, 2, 6, 1.",
            "A traversal is a rule for the order in which you visit nodes. The same tree produces different sequences under different rules. Build the binary search tree by inserting 4, then 2, then 6, then 1. preorder visits a node before either child and returns 4, 2, 1, 6. postorder visits both children before the node and returns 1, 2, 6, 4. The inorder walk, left then node then right, returns 1, 2, 4, 6, which is the sorted order only because the tree is a search tree. level_order uses a queue. It returns 4, 2, 6, 1. The root leaves first. Its children are enqueued left then right, so 2 is ahead of 6, and 1 waits behind them. Depth-first walks use a stack, or the call stack. Breadth-first walks use a queue. The container is the difference.",
            "Preorder is correct by induction on the tree. The first value is the root. The next values are the preorder of the left subtree, then the preorder of the right subtree. Postorder appends the root after both recursive sequences. Level order is the queue lesson again. A node is enqueued when its parent is visited, so every node at depth d enters the queue before any node at depth d + 1 is dequeued. Marking is unnecessary on a tree because there is one path from the root and no edge back to an ancestor.",
            "Each walk visits every node once and looks at every child link once, so the time is linear in the number of nodes. The call stack of a skewed preorder is linear. A balanced tree keeps that stack logarithmic. The level-order queue holds one level at a time and can hold about half the nodes of a wide level, so extra memory is linear in the worst case. Use inorder when you want the sorted keys. Use level order when the depth itself is the question.",
        ),
        _spec(
            "balanced-search-trees",
            "balanced-tree-explain-height",
            "Sorted inserts stay balanced",
            "Inserting 1, then 2, then 3 into a left-leaning red-black tree leaves 2 at the root. Inorder is still 1, 2, 3.",
            "A plain binary search tree becomes a chain when keys arrive in sorted order. Every operation then walks n nodes. A balanced tree keeps the height logarithmic by local rotations. The library's left-leaning red-black tree encodes a 2-3 tree. A red link to a left child means two keys share a node. Right-leaning red links are rotated away. Insert 1, then 2, then 3. The inorder walk is 1, 2, 3, so the search-tree order survives. The root key is 2, not 3, so the tree did not become a chain. select(1) returns 2, the second smallest key. rank(2) returns 1, the number of keys strictly smaller than 2. Those order statistics come from subtree sizes stored on the nodes.",
            "A rotation changes which node is the parent and which is the child. It does not change inorder. The keys that were left of a node stay left, and the keys that were right stay right. Only the shape moves. The red-black rules limit how many black links appear on a path from the root to a leaf, and a red link cannot simply stack on another red link. That bound is why the height stays logarithmic after the sorted inserts. select walks by subtree size. If the left subtree holds more than k keys, the answer is in the left subtree. Otherwise it is the node itself or a key in the right subtree.",
            "Insert, delete, rank, and select are logarithmic because the height is logarithmic. A rotation is a constant number of pointer writes. Extra memory is one node per key, plus the color and the size. The plain search tree uses the same memory and loses the height bound. Use the balanced tree when the input order is not under your control and later lookups must stay fast.",
        ),
        _spec(
            "priority-queues",
            "priority-queue-map-operations",
            "Pop the smallest priority",
            "push 5, then 3, then 4. The first pop returns priority 3 and item b.",
            "A priority queue returns the best priority, not the oldest item and not the newest item. The library's PriorityQueue is a binary min-heap. push(5, a), push(3, b), and push(4, c) leave 3 at the root. The first pop returns the pair 3, b. Later pops return 4, c and then 5, a. Each push returns a token. decrease_key uses that token to find the heap index without scanning. The heap stores priority, token, and item. The token breaks ties so two equal priorities stay distinct. This is the structure Dijkstra and Prim need when they repeatedly ask for the next smallest tentative weight. Sorting the whole set once is cheaper when you need every item in order and you will not insert anything in between.",
            "The heap invariant says every parent priority is less than or equal to its children. push appends and sifts up until the invariant holds. pop swaps the root with the last item, removes the old root, and sifts down. The item that leaves is the minimum because the root is the minimum. decrease_key is allowed to move a priority down, toward a better min, and then sifts up. An equal priority is not a decrease. The map from token to index is updated on every swap, so the next decrease still finds the item.",
            "push and pop are logarithmic in the number of stored items. The token map makes the find step constant time, so it does not hide a linear scan inside the logarithmic sift. Extra memory is the heap array plus the map, both linear. n pushes followed by n pops are n log n, the same family as heapsort. Prefer the queue when the set of candidates changes between extractions. Prefer a sort when the set is fixed.",
        ),
        _spec(
            "graph-representations",
            "graph-representation-compare-space",
            "Count the pairs an adjacency list stores",
            "A directed graph with vertices A, B, C, D and three edges stores three neighbor pairs. A matrix would store 16 cells.",
            "A graph can be stored as an adjacency list or as a matrix. The library Graph is a dictionary from each vertex to a list of neighbor and weight pairs. Add A to B, A to C, and B to D. The graph has 4 vertices and 3 outgoing pairs. A matrix for the same vertices has 16 cells, one for every ordered pair, almost all of them empty. The list stores only the edges you added. A sparse graph is one where the edge count is much smaller than the square of the vertex count. Breadth-first search on that shape should use a queue with constant-time ends. Python's collections.deque is the usual choice. The library's own breadth-first search uses its linked queue for the same reason. Scanning a matrix row to find neighbors costs a full vertex scan even when a vertex has one edge.",
            "The list answers 'who are my neighbors' by reading one list. The matrix answers the same question by scanning a row. Both can answer 'is there an edge from u to v', and the matrix does it in constant time while the list scans u's neighbors. Space follows the same split. The list is proportional to vertices plus edges. The matrix is proportional to vertices squared, whether or not the edges exist. Choose the representation for the operation you repeat, not for the picture you draw.",
            "Building the list is proportional to the number of edges. A traversal that walks each list once is proportional to vertices plus edges. The same traversal on a matrix is proportional to vertices squared. Extra memory for the search is still the queue or the stack, proportional to the vertices. Use a matrix only when the graph is dense or you need constant-time edge tests in the inner loop.",
        ),
        _spec(
            "topological-order",
            "topological-order-trace-kahn",
            "Kahn's algorithm on a small dag",
            "Edges A to B, A to C, B to D, and C to D produce the order A, B, C, D. A cycle makes topological_order raise ValueError.",
            "A topological order is a list of the vertices of a directed graph such that every edge points forward in the list. topological_order on edges A to B, A to C, B to D, and C to D returns A, B, C, D. Kahn's algorithm computes an indegree for each vertex. It starts a queue with every vertex whose indegree is zero. A is the only such vertex here. When a vertex leaves the queue, each outgoing edge reduces a neighbor's indegree. A neighbor enters the queue when its indegree hits zero. B and C both become ready after A, and D waits until both of its incoming edges have been counted. has_directed_cycle on this graph is false. On a two-cycle from A to B and back, it is true, and topological_order raises ValueError because the queue runs dry before every vertex has been emitted.",
            "A vertex enters the queue only when every predecessor has already been emitted. Every edge out of an emitted vertex has been relaxed, so a later position cannot be a predecessor of an earlier one. If the graph has a cycle, some vertex on the cycle always has indegree left, because its predecessor on the cycle was never emitted. The queue empties and the output is shorter than the vertex list. That length check is the cycle test inside this function. A depth-first version records a vertex after its descendants and reverses that finish order. Both reject a back edge.",
            "Each vertex is enqueued once and each edge is inspected once, so the time is proportional to vertices plus edges. Extra memory is the indegree map and the queue, proportional to the vertices. Use this order before dynamic programming on a dag, and before scheduling jobs that depend on other jobs. Do not call it on a graph that might contain a cycle unless you catch the error.",
        ),
        _spec(
            "shortest-paths",
            "shortest-path-choose-algorithm",
            "A longer edge loses to a two-edge path",
            "Dijkstra from A reports distance 3 at C, not the direct weight 4. Bellman-Ford allows the negative edge and reports -1.",
            "The shortest-path algorithm you want depends on the weights. Unweighted edges can use breadth-first search, because the fewest edges is the shortest path. Non-negative weights can use Dijkstra. Negative weights need Bellman-Ford, which also reports a negative cycle if you ask it to keep relaxing. On edges A to B weight 1, A to C weight 4, and B to C weight 2, dijkstra_distances_heap from A gives C the distance 3. The direct edge is not the best path. Relaxation is the step that discovers this. When B's distance is final, the edge B to C offers 1 + 2, which beats 4. bellman_ford_distances on A to B weight 1 and B to C weight -2 gives C the distance -1. Dijkstra is not the right call once a weight can be negative. zero_one_bfs_distances on a path of two weight-1 edges gives C the distance 2. floyd_warshall on that path also gives A to C the distance 2, and it fills every pair. is_bipartite is true on the path and false on a directed triangle, which is an odd cycle. kosaraju_strongly_connected_components on that triangle returns one component containing A, C, and B.",
            "Relaxation keeps a tentative distance. An edge u to v of weight w improves v when distance u plus w is smaller than distance v. Breadth-first search is this rule with every weight equal to 1, and the queue order makes the first visit final. Dijkstra makes a visit final when the vertex is dequeued from a non-negative priority queue, because no later path can be cheaper. A negative edge breaks that proof. Bellman-Ford repeats relaxation once per vertex so a simple path has time to propagate. Floyd-Warshall tries every intermediate vertex for every pair. Kosaraju finds mutually reachable sets. It is not a shortest-path algorithm, and it belongs beside these tools because a negative cycle inside a component makes distances undefined.",
            "The array-scan Dijkstra is proportional to vertices squared. The heap version is proportional to vertices plus edges, times a logarithm, when decrease-key is logarithmic. Bellman-Ford is vertices times edges. Floyd-Warshall is vertices cubed. Zero-one breadth-first search is linear in vertices plus edges when weights are only 0 and 1. Extra memory is the distance map. Pick the algorithm whose weight assumption you can actually state.",
        ),
        _spec(
            "minimum-spanning-trees",
            "mst-trace-kruskal",
            "Skip the edge that closes a cycle",
            "Undirected edges of weight 1, 2, and 4. Prim and Kruskal both return total weight 3. The weight-4 edge is the one that closes a cycle.",
            "A minimum spanning tree connects every vertex of an undirected weighted graph and has the smallest total edge weight. Prim and Kruskal both return 3 on the triangle A-B weight 1, B-C weight 2, and A-C weight 4. Kruskal sorts edges by weight and adds an edge when its ends lie in different components. The weight-4 edge finds A and C already connected through B, so the union-find cycle check rejects it. Prim grows one tree from A. It adds the cheapest edge that leaves the visited set. That is A-B, then B-C. The edge back to A is ignored because A is already visited. The two algorithms can pick different edges when weights tie. They do not pick different totals on this graph.",
            "Kruskal's accepted edges never form a cycle because union refuses an edge whose ends already share a root. A set of n - 1 such edges on n vertices is a tree, and it is spanning because every vertex that appears in an edge was merged. The cut property says the cheapest edge leaving a set of visited vertices is safe to add. Prim always adds such an edge. Replacing it with a heavier edge across the same cut would not reduce the total. The rejected weight-4 edge is the unique heaviest edge on the only cycle, which is why both algorithms drop it.",
            "Kruskal sorts the edges, which is E log E, and then runs a union-find almost-constant find per edge. Prim with a binary heap is proportional to vertices plus edges, times a log. Extra memory is the parent array or the heap, both linear in the vertices for a connected graph. Use either algorithm when the graph is undirected and you want a cheapest connection, not a shortest path from one source.",
        ),
        _spec(
            "two-pointers",
            "two-pointers-justify-movement",
            "Two indexes on a sorted array",
            "two_sum_sorted on 1, 2, 4, 7 with target 6 returns indexes 1 and 2.",
            "Two pointers scan a sorted array from the ends, or scan a sequence with a start and an end that only move forward. two_sum_sorted on 1, 2, 4, 7 with target 6 returns indexes 1 and 2, the positions of 2 and 4. The left index starts at 0 and the right index starts at the last item. If the sum is too small, the left index moves right, because every value further left is even smaller. If the sum is too large, the right index moves left. Each move throws away a value that cannot be part of any remaining pair. The loop stops when the indexes meet. A pair of nested loops would also find the pair, and would check every combination.",
            "The invariant is that any solution still available uses a left index at or after the current left, and a right index at or before the current right. It holds at the start because the whole array is inside that range. Moving the left index forward is safe when the sum is too small, because the current left value plus any value to the left of the right index is even smaller. The symmetric argument moves the right index. Sorted order is the assumption. Without it, a larger index is not a larger value, and the move is not safe.",
            "Each index moves at most n times, and only in one direction, so the total time is linear. Extra memory is the two indexes. The nested pair scan is quadratic. State the sorted precondition before you quote the linear bound. If the array is not sorted, sorting it first costs n log n and the two-pointer scan is no longer the whole story.",
        ),
        _spec(
            "sliding-window",
            "sliding-window-maintain-valid-range",
            "Window maximum and a unique substring",
            "sliding_window_maximum on 1, 3, 2, 5 with window 2 returns 3, 3, 5. The longest unique substring of abcabcbb has length 3.",
            "A sliding window is a contiguous slice that moves across the input. You keep a fact about the slice and update it when the slice grows or shrinks, instead of recomputing from scratch. sliding_window_maximum on 1, 3, 2, 5 with window 2 returns 3, 3, 5. A deque stores indexes of candidates. The front is the index of the current maximum. A new value pops the candidates it beats, because they are smaller and older, so they cannot be the maximum of this window or a later one. An index that falls off the left of the window is popped from the front. longest_unique_substring_length on abcabcbb returns 3. The window grows on the right and shrinks on the left whenever a repeated character enters. Both ends move only forward.",
            "The deque stays decreasing in value. The front is therefore the maximum of the indexes that are still inside the window. Popping a smaller tail preserves that order. Dropping an index that is left of the window preserves the window bounds. The unique-substring window's invariant is that every character inside it appears once. When a new character repeats one inside the window, the left end advances past that earlier copy. The length of the window after each step is a candidate for the answer. The maximum of those lengths is 3.",
            "Each index enters and leaves the deque at most once, so the window maximum is linear time and the deque uses linear extra memory in the worst case. The unique-substring scan is also linear because both ends move forward at most n steps. A fresh scan of each window would be quadratic. The monotonicity you need is the decreasing candidate list, or the fact that the left end never needs to move backward. If the predicate is not of that shape, the window method does not apply.",
        ),
        _spec(
            "prefix-sums",
            "prefix-sums-derive-range-query",
            "A half-open range sum",
            "PrefixSum on 1, 2, 3, 4 answers range_sum(1, 3) with 5, the sum of values[1:3].",
            "A prefix sum array stores the total of every item up to each index. The library PrefixSum on 1, 2, 3, 4 builds those totals once. range_sum(start, end) returns the sum of values[start:end], end exclusive. range_sum(1, 3) is 2 + 3, which is 5. The formula is total[end] minus total[start]. The item at start is included and the item at end is not, matching a Python slice. Any later range on the same array is then a subtraction. Counting subarrays that sum to a target uses the same totals. As you walk the array, a map from a previous prefix to how many times it occurred tells you how many earlier starts would make the current prefix hit the target.",
            "total[0] is 0, the sum of an empty prefix. total[i + 1] is total[i] plus values[i]. By induction, total[end] is the sum of the first end items. Subtracting total[start] removes the items before the slice and leaves the slice. The half-open interval is why you do not add or drop an endpoint by hand. A target count is the same identity. If the current prefix minus a previous prefix equals the target, the slice between them sums to the target. The frequency map counts how many such previous prefixes exist.",
            "Building the totals is linear time and linear extra memory. Each range query is constant time. n separate queries are therefore linear after the build, not quadratic. The frequency-map walk is linear expected time with a dictionary. Use prefix sums when the array does not change. A point update would force you to rebuild, which is why a later lesson brings a Fenwick tree.",
        ),
        _spec(
            "backtracking",
            "backtracking-trace-reversible-state",
            "Count the permutations of three items",
            "permutations of 1, 2, 3 returns six lists. Each call chooses, recurses, and undoes.",
            "Backtracking searches a tree of choices. You choose, recurse, and undo so the next choice sees the earlier state. permutations of 1, 2, 3 returns six lists, one for every order. The first position has three choices. The second has two remaining items. The third has one. The product is 6, and the function materializes each list. The undo step puts the chosen item back into the pool before the next sibling is tried. Without the undo, the later branches would see a shrinking pool that is not restored. n_queens_count uses the same shape. A queen is placed, the search goes to the next row, and the placement is removed on the way back. Pruning skips a placement that already shares a column or a diagonal with a queen.",
            "The state invariant is that the pool, or the board, matches the choices on the path from the root to the current call, and nothing else. Choose extends that path. Recurse searches below it. Undo returns to the parent path. A leaf is a complete choice, and it is recorded before the undo. Every permutation appears once because each item is chosen into each position from the items not yet used. The search tree is exhaustive unless a prune deletes a branch. A prune is correct only when every leaf under that branch would fail the same test.",
            "The permutation tree has n! leaves, and building each list copies n items, so the time is proportional to n times n!. Extra memory is the current path, which is n, plus the output. Pruning does not change the worst-case shape. It changes which branches you actually enter. Estimate the tree before you code the search. If the unpruned tree is already enormous, a different state is the real fix.",
        ),
        _spec(
            "greedy-methods",
            "greedy-methods-state-choice",
            "Take the interval that finishes first",
            "Intervals (1, 3), (2, 4), and (3, 5) yield two compatible intervals. The frequent symbol gets the short Huffman code.",
            "A greedy algorithm makes a local choice and does not take it back. The choice needs an argument that some optimal solution agrees with it. interval_scheduling_max_count on (1, 3, a), (2, 4, b), and (3, 5, c) returns 2. The rule sorts by finish time and takes the next interval that starts at or after the previous finish. a finishes first and is taken. b overlaps a and is skipped. c starts when a finishes and is taken. An example with three intervals does not prove the rule. The exchange argument does. Huffman coding is another greedy choice. huffman_codes on frequencies a 3, b 1, and c 1 gives a the code 1, the short code, because a is the frequent symbol. The two rare symbols share the longer branch. The library builds that tree by repeatedly combining the two lightest weights with a min-heap.",
            "Suppose an optimal schedule's first interval is not the one that finishes first. Swap it for the earliest-finishing interval. The swap stays feasible because that interval finishes even sooner, so everything that fit after the old first interval still fits. The count does not drop. Repeating the swap produces the greedy schedule without losing optimality. That is the proof. A single worked example only shows the rule on one input. Huffman' s exchange says the two lightest symbols can be siblings in some optimal tree. Combining them and repeating builds the codes.",
            "Sorting the intervals is n log n, and the scan that follows is linear. Huffman does n heap operations, also n log n, and the output codes are linear in the number of symbols. Extra memory is the sorted copy or the heap. Do not quote the bound until you can say why the local choice is safe. A different sort key, such as shortest interval, needs its own argument or a counterexample.",
        ),
        _spec(
            "dp-state-and-transition",
            "dp-state-define-recurrence",
            "Coin change as a table of amounts",
            "min_coin_change of coins 1, 3, 4 and amount 6 returns 2. The 0-1 knapsack on weights 1, 3 and values 2, 4 with capacity 4 returns 6.",
            "A dynamic-programming state is the smallest subproblem you are willing to store. The transition says how that state is computed from earlier states. For coin change, the state is the minimum number of coins that sum to an amount. min_coin_change on coins 1, 3, 4 and amount 6 returns 2, for example 3 + 3. The transition tries each coin that does not exceed the amount and adds one to the answer for the remaining amount. Amount 0 takes zero coins. A knapsack state needs two indexes. knapsack_01 on weights 1, 3, values 2, 4, and capacity 4 returns 6. Both items fit, and their values sum to 6. The transition either skips the item or takes it when the remaining capacity allows. Taking it is allowed once, which is why the item index moves forward.",
            "The coin table is correct by induction on the amount. The base amount is 0. If every smaller amount is correct, trying each coin reads a correct smaller answer and the minimum plus one is the best for this amount. Order matters. You fill smaller amounts first. The knapsack table is correct by induction on the item index and the capacity. The skip choice copies the previous item's answer. The take choice adds the value to a smaller capacity of the previous item. Both choices are available, so the cell keeps the larger one.",
            "Coin change fills one cell per amount, and each cell tries every coin, so the time is the amount times the number of coins. Extra memory can be the full table or just the previous amounts. The 0-1 knapsack is items times capacity, and a rolling row brings the memory down to the capacity. Count states, then count the work inside one transition, then say whether you store every state. Those are three different numbers.",
        ),
        _spec(
            "string-search",
            "string-search-trace-kmp-fallback",
            "The first match is not at index 0",
            "kmp_search and rabin_karp_search both find ababa inside ababcababa at index 5.",
            "A naive search tries the pattern at every index of the text and compares characters until one differs. Knuth-Morris-Pratt avoids restarting the text index after a partial match. kmp_search of pattern ababa in text ababcababa returns 5. Index 0 matches four characters and then fails, because the text has c where the pattern needs a. The failure links say how long a prefix of the pattern is also a suffix of the part just matched, so the search resumes in the middle of the pattern instead of at its first character. rabin_karp_search on the same strings also returns 5. It compares a rolling hash of the pattern with the hash of each window, and it still checks the characters when the hashes agree. A hash hit is a candidate, not a proof.",
            "The failure link at a position is the longest proper prefix that is also a suffix of the pattern up to that position. Following it on a mismatch preserves the characters that are already known to match. That is why the text index does not move backward. Rabin-Karp's window hash can be updated in constant time by removing the character that leaves and adding the character that enters. Equal hashes can still be different strings, so the character check is part of correctness. Unequal hashes are a sure miss.",
            "The failure table is linear in the pattern length. The search is linear in the text length. Extra memory is the failure table. The naive search is linear in the product of the two lengths. Rabin-Karp is linear in expectation and can degrade if every window collides. Use KMP when you want a worst-case linear bound. Use a rolling hash when you already have a modulus you trust and you verify candidates.",
        ),
        _spec(
            "tries-and-text-indexes",
            "text-index-match-query",
            "A trie stores keys, a suffix array stores positions",
            "After inserting cat and car, contains(car) is true and contains(ca) is false. The suffix array of banana starts 5, 3, 1, 0, 4, 2.",
            "A trie stores strings along a path of characters. Trie.insert walks or creates a child for each character. contains walks the same path and succeeds only when the whole key was inserted. After inserting cat and car, contains car is true, contains cat is true, and contains ca is false. ca is a prefix of both keys, and this trie does not treat a prefix as a stored key. A suffix array is a different index. suffix_array_with_lcp on banana returns the suffix starts 5, 3, 1, 0, 4, 2 and an LCP array whose third entry is 3. The suffixes in that order are a, ana, anana, banana, na, nana. Equal prefixes sit together, which is why a pattern query can binary-search the array. The LCP says how long the shared prefix of neighbors is, so you do not recompare those characters.",
            "Trie lookup is correct because each step consumes one character and the path is unique. Missing a child means the key was never inserted. Stopping in the middle is not a hit unless insert marked that node as a key, and this contains requires the full key. The suffix array is the sorted order of every suffix. Binary search is valid because that order is alphabetical. The LCP of two adjacent suffixes is a lower bound on comparisons you can skip. Construction has to be counted separately from a single query.",
            "Inserting or looking up a key in the trie is proportional to the key length, not to the number of stored keys, unless you are scanning children linearly. The trie memory is proportional to the number of distinct prefixes. Building a suffix array by sorting suffixes naively is more expensive than one query, and the array itself is linear in the text length. Include that build when you compare a trie with a scan of the raw text. A query-only bound hides the index.",
        ),
        _spec(
            "range-query-structures",
            "range-query-compare-operations",
            "Prefix sums that survive a point update",
            "A Fenwick tree that adds 1, 2, and 3 reports prefix 6. A segment tree adds 5 across a span. A sparse table answers a static minimum.",
            "Prefix sums answer a range in constant time until the array changes. A point update then costs a rebuild. A Fenwick tree and a segment tree keep the update logarithmic. FenwickTree of length 4, after add 1 at index 0, add 2 at index 1, and add 3 at index 2, reports prefix_sum(2) equal to 6. The structure stores partial sums on ranges whose length is a power of two. A point add walks those ranges. A prefix query walks a different set and sums them. SegmentTree on 1, 2, 3, 4 can add 5 to the inclusive span from index 1 to index 2. point_query(1) becomes 7 and point_query(0) stays 1. The lazy tag records the addition on a segment node and pushes it to children only when a later query needs them. SparseTable on 1, 3, 2, 4 answers range_min(1, 3) with 2. The range is inclusive. The table does not support updates. It precomputes the minimum of every power-of-two span.",
            "The Fenwick prefix is the sum of disjoint blocks that cover [0, index]. Each add updates every block that contains the index. Those two walks are why a query sees the latest adds. The segment tree's lazy tag is correct because a node tag means every leaf under it should receive the delta. Pushing the tag to the two children and clearing the parent preserves that meaning. The sparse table uses the fact that minimum is idempotent. The minimum of two overlapping blocks is still the minimum of the union, so a query can cover a range with two precomputed blocks.",
            "A Fenwick add or prefix is logarithmic in the length. A segment update or point query is logarithmic. The sparse table builds in n log n and answers a minimum in constant time, with no updates. Extra memory is linear for the Fenwick tree, linear for the segment tree's nodes and tags, and n log n for the sparse table. Choose from the mix of updates and queries you actually have. A static array does not need the heavier tree.",
        ),
        _spec(
            "approximate-membership",
            "bloom-filter-state-guarantees",
            "A definite miss and a possible hit",
            "A Bloom filter with 64 bits and 3 hashes inserts cat. maybe_contains(cat) is true. A miss would mean the item was never added.",
            "A Bloom filter answers membership with a bit array and several hash functions. add sets the bits those hashes name. maybe_contains returns true only when every one of those bits is set. BloomFilter with 64 bits, 3 hashes, and seed 0 inserts cat. maybe_contains cat returns true. A false answer means the item was definitely never added, because add would have set those bits. A true answer means the item might have been added, or other items may have set the same bits. That is a false positive. Which uninserted strings collide depends on the process hash salt, so this lesson does not pin a particular miss. This filter has no delete. Clearing a bit could erase the evidence of a different item. The library states that contract on the class. A definite miss is the useful answer. It lets a storage engine skip a disk read.",
            "There are no false negatives for items that were actually added, as long as nobody clears bits. Each add only sets bits, and maybe_contains only checks those bits. If any bit is clear, at least one add that should have set it did not happen, so the item is absent. If all bits are set, every required bit was set by someone, and that someone might not have been this item. More bits or a different hash count changes how often unrelated items overlap. The seed fixes the hash functions so a test can repeat.",
            "add and maybe_contains hash the item k times, so they are proportional to k, not to the number of items inserted. Extra memory is the bit array, which you choose up front. A dictionary would be exact and would grow with the items. The filter spends a false-positive rate to keep a fixed size. Say the rate you are willing to accept before you treat a hit as a fact.",
        ),
        _spec(
            "storage-engines-and-locality",
            "storage-compare-write-read-tradeoffs",
            "A B-tree lookup and a sequential scan",
            "BTree.search finds 1 after it was inserted and rejects 9. sequential_scan_sum of 1, 2, 3 returns 6.",
            "Storage engines place reads and writes in different structures. A B-tree keeps keys ordered in nodes with many children, so a lookup walks a short path. BTree.insert of 2 and then 1 leaves search(1) true and search(9) false. The branching factor is the knob that trades taller trees for fatter nodes. A log-structured merge tree takes the other side of the trade. Writes append to a memory table and a write-ahead log, then flush sorted runs. Reads may check several runs. Compaction merges those runs. The library's sequential_scan_sum of 1, 2, 3 returns 6. That scan touches neighboring items, which is the access pattern real disks and caches reward. A random jump to each key pays the same arithmetic and a worse memory pattern. Locality is why the sum of a tight array is the baseline you compare against.",
            "B-tree search is correct because each node stores its keys in order and the child between two keys holds only the keys that belong between them. A missing key falls out of a leaf. Insert splits a full node so the branching invariant survives. A write-ahead log is correct when a replay reproduces the same committed writes. A sequential scan is correct because addition is applied once per item and the items are exactly the input. The locality claim is not a change in the arithmetic result. It is a claim about how many cache lines or pages that arithmetic touches.",
            "A B-tree search is logarithmic in the number of keys, with a large base when nodes are wide. Extra memory is the nodes. A sequential scan is linear time and constant extra memory, and it is the practical winner when you need every item anyway. A point lookup in a structure built for scans can be slower than the same lookup in a tree. Say which operation is common before you pick the engine. The toy sum is the locality baseline, not a database.",
        ),
        _spec(
            "approximation-guarantees",
            "approximation-prove-feasibility",
            "A vertex cover at most twice the optimum",
            "Two disjoint edges produce a cover of all four endpoints. The optimum picks one endpoint from each edge. The constructed cover is twice that size.",
            "Some problems have no known exact algorithm that is fast on every input. An approximation algorithm returns a legal answer whose cost is provably close to the best cost. vertex_cover_two_approximation scans edges and, when neither endpoint is already chosen, adds both. On a graph with only the edges A-B and C-D, the cover is the set A, B, C, D. The cover is feasible because every edge has both ends selected, so it certainly has one. An optimum cover can pick one end from each edge, so its size is 2. The algorithm returned 4, which is twice the optimum. The proof is the pairing. Each time the algorithm adds two vertices, it does so for an edge whose ends were both still free. Those edges do not share vertices. Any cover must pick at least one vertex from each such edge. The algorithm picked two. The ratio is therefore at most 2 on every graph, not only on this one.",
            "Feasibility is the first half. Every edge is either selected as a pair or already touched by an earlier pair, so no edge is left uncovered. The ratio is the second half. Let the selected edges be the ones that contributed a pair. They are vertex-disjoint, so the optimum is at least the number of those edges. The algorithm's cover has two vertices per selected edge, plus nothing else from this rule. Twice the optimum is therefore an upper bound on the size of the cover. A single example that happens to be close is not this proof. The proof counts the disjoint edges.",
            "The scan looks at each adjacency-list entry once, so the time is proportional to vertices plus edges. Extra memory is the cover set, which is at most the vertices. The guarantee does not say the cover is the smallest possible. It says you can bound how far it is from the smallest. Use that bound when an exact cover would require a search you cannot afford.",
        ),
    ]


EXTRA_RUNNABLE = {
    "monotonic-stack-patterns": "from bitsandbytes.stacks.next_greater import next_greater\nprint(next_greater([2, 1, 2, 4, 3]))\n# prints: [4, 2, 4, None, None]",
    "stack-parsing-and-expressions": "from bitsandbytes.stacks.infix_postfix import evaluate_infix\nprint(evaluate_infix('2+3*4'))\n# prints: 14",
    "noncomparison-sorts": "from bitsandbytes.sorting.selection_and_radix import counting_sort\nprint(counting_sort([3, 1, 2, 1], maximum=3))\n# prints: [1, 1, 2, 3]",
    "order-statistic-selection": "from bitsandbytes.sorting.selection_and_radix import quickselect\nprint(quickselect([3, 1, 4, 2], 0))\n# prints: 1",
    "inversion-counting": "from bitsandbytes.sorting.selection_and_radix import inversion_count\nprint(inversion_count([3, 1, 4, 2]))\n# prints: 3",
    "hash-linear-probing": "from bitsandbytes.hash_tables.linear_probing import LinearProbingHashTable\ntable = LinearProbingHashTable(capacity=4)\ntable[0] = 1\ntable[4] = 2\ndel table[0]\nprint(table[4])\n# prints: 2",
    "lru-cache": "from bitsandbytes.linked_lists.lru_cache import LRUCache\ncache = LRUCache(2)\ncache.put('a', 1)\ncache.put('b', 2)\ncache.get('a')\ncache.put('c', 3)\nprint(cache.get('b'))\n# prints: None",
    "tree-traversals": "from bitsandbytes.trees.bst import BinarySearchTree\nfrom bitsandbytes.trees.traversals import preorder\ntree = BinarySearchTree()\nfor value in (4, 2, 6, 1):\n    tree.insert(value)\nprint(preorder(tree.root))\n# prints: [4, 2, 1, 6]",
    "balanced-search-trees": "from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree\ntree = LeftLeaningRedBlackTree()\nfor value in (1, 2, 3):\n    tree.insert(value)\nprint(tree.inorder())\n# prints: [1, 2, 3]",
    "priority-queues": "from bitsandbytes.heaps.priority_queue import PriorityQueue\nqueue = PriorityQueue()\nqueue.push(5, 'a')\nqueue.push(3, 'b')\nqueue.push(4, 'c')\nprint(queue.pop())\n# prints: (3, 'b')",
    "graph-representations": "from bitsandbytes.graphs.adjacency_list import Graph\ngraph = Graph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('A', 'C', 1)\ngraph.add_edge('B', 'D', 1)\nprint(sum(len(graph.neighbors(vertex)) for vertex in graph.vertices()))\n# prints: 3",
    "topological-order": "from bitsandbytes.graphs.adjacency_list import Graph\nfrom bitsandbytes.graphs.algorithms import topological_order\ngraph = Graph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('A', 'C', 1)\ngraph.add_edge('B', 'D', 1)\ngraph.add_edge('C', 'D', 1)\nprint(topological_order(graph))\n# prints: ['A', 'B', 'C', 'D']",
    "shortest-paths": "from bitsandbytes.graphs.adjacency_list import Graph\nfrom bitsandbytes.graphs.algorithms import dijkstra_distances_heap\ngraph = Graph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('A', 'C', 4)\ngraph.add_edge('B', 'C', 2)\nprint(dijkstra_distances_heap(graph, 'A')['C'])\n# prints: 3",
    "minimum-spanning-trees": "from bitsandbytes.graphs.algorithms import UndirectedGraph, prim_minimum_spanning_weight\ngraph = UndirectedGraph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('B', 'C', 2)\ngraph.add_edge('A', 'C', 4)\nprint(prim_minimum_spanning_weight(graph, 'A'))\n# prints: 3",
    "two-pointers": "from bitsandbytes.patterns.arrays import two_sum_sorted\nprint(two_sum_sorted([1, 2, 4, 7], 6))\n# prints: (1, 2)",
    "sliding-window": "from bitsandbytes.patterns.arrays import sliding_window_maximum\nprint(sliding_window_maximum([1, 3, 2, 5], 2))\n# prints: [3, 3, 5]",
    "prefix-sums": "from bitsandbytes.patterns.arrays import PrefixSum\nprint(PrefixSum([1, 2, 3, 4]).range_sum(1, 3))\n# prints: 5",
    "backtracking": "from bitsandbytes.backtracking.search import permutations\nprint(len(permutations([1, 2, 3])))\n# prints: 6",
    "greedy-methods": "from bitsandbytes.greedy.classic import interval_scheduling_max_count\nprint(interval_scheduling_max_count([(1, 3, 'a'), (2, 4, 'b'), (3, 5, 'c')]))\n# prints: 2",
    "dp-state-and-transition": "from bitsandbytes.dynamic_programming.classic import min_coin_change\nprint(min_coin_change([1, 3, 4], 6))\n# prints: 2",
    "string-search": "from bitsandbytes.strings.algorithms import kmp_search\nprint(kmp_search('ababcababa', 'ababa'))\n# prints: 5",
    "tries-and-text-indexes": "from bitsandbytes.strings.algorithms import Trie\ntrie = Trie()\ntrie.insert('cat')\ntrie.insert('car')\nprint(trie.contains('car'), trie.contains('ca'))\n# prints: True False",
    "range-query-structures": "from bitsandbytes.range_queries.structures import FenwickTree\ntree = FenwickTree(4)\ntree.add(0, 1)\ntree.add(1, 2)\ntree.add(2, 3)\nprint(tree.prefix_sum(2))\n# prints: 6",
    "approximate-membership": "from bitsandbytes.approximate.structures import BloomFilter\nbloom = BloomFilter(bit_count=64, hash_count=3, seed=0)\nbloom.add('cat')\nprint(bloom.maybe_contains('cat'))\n# prints: True",
    "storage-engines-and-locality": "from bitsandbytes.storage.engines import sequential_scan_sum\nprint(sequential_scan_sum([1, 2, 3]))\n# prints: 6",
    "approximation-guarantees": "from bitsandbytes.limits.approximation import vertex_cover_two_approximation\nfrom bitsandbytes.graphs.adjacency_list import Graph\ngraph = Graph()\ngraph.add_edge('A', 'B', 1)\ngraph.add_edge('C', 'D', 1)\nprint(sorted(vertex_cover_two_approximation(graph)))\n# prints: ['A', 'B', 'C', 'D']",
}


def _questions() -> dict[str, dict[str, object]]:
    rows = [
        ("monotonic-stack-patterns", "A later value resolves waiting indexes. What does next_greater write for the first 2 in 2, 1, 2, 4, 3?", "The first strictly greater value on its right", "The nearest smaller value on its left", "The last value in the list, even when it is smaller", "The stack pops an index when a greater value arrives.", "A smaller neighbor does not answer a next-greater question.", ["The stack stores indexes that are still waiting.", "None means no greater value exists."], "monotonic-stack-count-total-work", "Each index is pushed once and popped at most once. What is the total work?", "Linear in the number of indexes", "Quadratic, because a nested loop always restarts", "Constant, because only the top index matters", "The pops are charged across the whole scan, not to one iteration.", "Do not multiply the inner loop by n a second time."),
        ("stack-parsing-and-expressions", "Which bracket string is balanced?", "([]) because each closer matches the current opener", "([)] because every bracket has a partner somewhere", "(() because a leftover opener is optional", "The closer must match the opener on top of the stack.", "A partner later in the string is not a match if another opener is in between.", ["Ignore characters that are not brackets.", "The stack should be empty at the end."], "stack-trace-operator-precedence", "evaluate_infix of 2+3*4 applies which operator first?", "Multiplication, because it leaves the operator stack before addition", "Addition, because it appears further left", "Neither, because postfix ignores precedence", "The postfix form is 2 3 4 * +, so the product happens first.", "Left-to-right position is not the precedence rule."),
        ("noncomparison-sorts", "counting_sort is told the maximum key. What does that bound pay for?", "A count slot for every key value from zero through the maximum", "A comparison between every pair of keys", "A binary search on the output", "The range of keys becomes an array, not a comparison tree.", "The sort still has to place every input key.", ["Equal keys stay in input order when the write is stable.", "A huge maximum dominates a short list."], "noncomparison-derive-radix-cost", "A radix sort repeats a stable digit pass once per digit. What is the cost when the digit count is constant?", "Linear in the number of keys", "n log n from comparisons", "Quadratic from restarting each pass", "A constant number of linear passes is still linear.", "Do not add a comparison-sort bound on top of the digit passes."),
        ("order-statistic-selection", "quickselect keeps searching after a partition. Which side remains?", "The side that still contains index k", "Both sides, because the answer might be anywhere", "Neither side, because the pivot is always the answer", "The pivot is already in its sorted index.", "The discarded side cannot contain the k-th smallest key.", ["k is zero-based.", "The rightmost value is the pivot in this library."], "selection-compare-cost-risks", "This quickselect always pivots on the rightmost value. What can the worst case cost?", "Quadratic time when every pivot is extreme", "Linear time on every input, because a pivot always halves the range", "n log n time, because it finishes the sort", "An extreme pivot shrinks the range by one item.", "The expected linear bound needs balanced pivots, which this code does not force."),
        ("inversion-counting", "Which pair in 3, 1, 4, 2 is an inversion?", "3 before 1, because the earlier key is larger", "1 before 4, because they are neighbors", "4 before nothing, because 4 is the largest key", "An inversion is an earlier larger key and a later smaller key.", "A sorted pair is not an inversion.", ["i must be less than j.", "The total on this list is three pairs."], "inversion-count-cross-run", "During a merge, the right front is smaller and two keys remain on the left. How many inversions does that one take add?", "Two, one for each key still on the left", "One, only against the left front", "Zero, because both runs are already sorted", "The right front is smaller than every remaining left key.", "Sorted runs still hide cross inversions."),
        ("hash-linear-probing", "Key 0 is deleted after key 4 probed past it. What must the slot hold?", "A tombstone, so lookup of 4 keeps probing", "An empty slot, so lookup of 4 stops and misses", "Key 4, because deletion moves later keys backward", "A tombstone is occupied for the purpose of continuing a probe.", "An empty slot would hide every key that stepped over this one.", ["The start slot of 0 and 4 matches when the capacity is 4.", "Live keys and tombstones are different."], "hash-probing-explain-clustering", "What is the load factor of a probing table?", "Live keys divided by the number of slots", "The length of the longest probe, always", "One, because hashing avoids collisions", "Load factor is size over capacity.", "Clustering gets worse as that ratio grows."),
        ("lru-cache", "Capacity is 2. You put a, put b, get a, then put c. Which key is evicted?", "b, because a was used more recently than b", "a, because the first key always leaves", "c, because the newest key is the first to leave", "The tail is the least recently used key.", "A get counts as a use and moves that key off the tail.", ["The dictionary finds the node.", "The list stores the recency order."], "lru-analyze-combined-operations", "Why is eviction constant time rather than a scan of the capacity?", "The tail node and the dictionary entry are both known", "The cache sorts every key by age on each put", "The singly linked tail pointer walks from the head", "move and unlink use the stored neighbors.", "A search by age would be linear in the capacity."),
        ("tree-traversals", "Insert 4, 2, 6, 1. Which sequence is preorder?", "4, then 2, then 1, then 6", "1, then 2, then 4, then 6", "4, then 2, then 6, then 1", "Preorder visits the node before its children.", "Inorder is the sorted sequence. Level order uses a queue.", ["Left child before right child.", "1 hangs under 2."], "tree-traversal-trace-level-order", "The same tree is visited with a queue. Which sequence is level order?", "4, then 2, then 6, then 1", "4, then 1, then 2, then 6", "1, then 6, then 2, then 4", "Children are enqueued when their parent is dequeued.", "1 is a child of 2, so it waits behind 6."),
        ("balanced-search-trees", "Keys 1, 2, 3 arrive in order. Where does a left-leaning red-black tree put the root?", "At 2, so the tree is not a chain", "At 3, because the last insert becomes the root", "At 1, because the first insert stays the root", "Rotations keep a logarithmic height on this insert order.", "A plain search tree would chain these keys.", ["Inorder is still sorted.", "select and rank use subtree sizes."], "balanced-tree-preserve-order-with-rotations", "A rotation changes the parent of a node. What stays true?", "Inorder still lists the keys from small to large", "Inorder reverses", "The root key is always the first key inserted", "Left keys stay left and right keys stay right.", "Only the shape is edited."),
        ("priority-queues", "Priorities 5, 3, and 4 are pushed. Which item leaves first?", "The item whose priority is 3", "The item pushed first, whose priority is 5", "The item pushed last, whose priority is 4", "A min-heap root is the smallest priority.", "Push order is not the pop order.", ["The token is not the priority.", "Later pops return 4 and then 5."], "priority-queue-choose-extraction-or-sort", "You will insert more items between extractions. Which structure matches that workload?", "A priority queue, because each push and pop is logarithmic", "A full sort before every extraction", "An unordered list scan that you call constant", "The set of candidates changes between pops.", "Sorting a fixed array is the other workload."),
        ("graph-representations", "A graph has 4 vertices and 3 directed edges. What does the adjacency list store?", "Three neighbor pairs, plus the vertex records", "Sixteen filled matrix cells", "One pair per vertex, whether or not an edge exists", "The list stores edges you added, not the empty pairs.", "A matrix is the structure with a cell per ordered pair.", ["Sparse means edges are far fewer than vertices squared.", "A queue walks the lists during breadth-first search."], "graph-representation-choose-operations", "You repeat 'list every neighbor' on a sparse graph. Which store fits?", "An adjacency list, because each neighbor scan reads one list", "A matrix, because every row scan is proportional to the edges", "Either store, because both are proportional to vertices plus edges", "A matrix row scan is proportional to the vertex count.", "The list length is the degree."),
        ("topological-order", "Kahn's algorithm starts with which vertices?", "The vertices whose indegree is zero", "The vertices whose outdegree is zero", "Any vertex on a cycle", "A source has no incoming edge left.", "A cycle has no vertex that can start the order.", ["Emitting a vertex reduces its neighbors' indegrees.", "A short output means a cycle."], "topological-order-detect-cycle", "topological_order is called on a directed cycle. What happens?", "It raises, because some vertex never reaches indegree zero", "It returns the cycle vertices twice", "It returns an empty list for every graph", "The queue empties before every vertex is emitted.", "A dag of the same size would return every vertex."),
        ("shortest-paths", "Edges include A to C with weight 4 and A to B to C with weights 1 and 2. What does Dijkstra report for C?", "Distance 3, after relaxing the edge from B", "Distance 4, because the direct edge is examined first", "Distance 1, because B is the first neighbor", "Relaxation replaces a tentative distance when a better path appears.", "The first edge you see is not frozen unless the algorithm says so.", ["Weights here are non-negative.", "Bellman-Ford is the algorithm that allows a negative edge."], "shortest-path-trace-relaxation", "A negative edge is on the path. Which algorithm still applies?", "Bellman-Ford, which repeats relaxation enough times for a simple path", "Dijkstra, because the heap ignores the sign", "Breadth-first search, because every edge still counts as one hop", "Dijkstra's proof needs non-negative weights.", "A negative cycle makes distances undefined."),
        ("minimum-spanning-trees", "Kruskal considers the weight-4 edge after the weights 1 and 2 are already chosen. What does the cycle check do?", "It rejects the edge, because its ends are already connected", "It adds the edge, because heavier edges are preferred", "It deletes the weight-1 edge to make room", "Union-find reports one component, so the edge would close a cycle.", "The spanning tree wants n - 1 edges, not every edge.", ["Prim grows from one vertex instead of sorting.", "Both algorithms total 3 on this triangle."], "mst-explain-cycle-check", "Why is the rejected edge unsafe to add?", "Its ends are already in the same component, so the edge is not needed", "Its ends are in different components, so the tree stays disconnected", "Spanning trees are required to contain a cycle", "A tree on n vertices has no cycle and has n - 1 edges.", "The cut property is what justifies the edge you do add."),
        ("two-pointers", "The sorted values are 1, 2, 4, 7 and the target is 6. The current sum is too small. Which index moves?", "The left index moves right, toward a larger value", "The right index moves left, toward a smaller value", "Both indexes jump to the middle", "A larger left value is the only way to increase the sum.", "Sorted order is what makes the move safe.", ["The successful indexes are 1 and 2.", "Each index moves in only one direction."], "two-pointers-count-total-moves", "Both indexes move only forward across n items. What is the total number of moves?", "At most n, so the scan is linear", "n squared, because each left index retries every right index", "log n, because the array is binary-searched", "A one-direction walk cannot revisit an item.", "Sorting first would be an extra n log n if the array started unsorted."),
        ("sliding-window", "A window maximum deque sees a new value larger than the candidates at the back. What happens to those candidates?", "They are popped, because they cannot be a later maximum", "They stay, because an older small value might win", "The window restarts from index zero", "A newer larger value dominates older smaller ones inside this window and the next.", "The front of the deque is the current maximum.", ["Indexes that slide out of the window also leave.", "The unique-substring window moves its ends forward too."], "sliding-window-test-monotonicity", "The unique-substring window sees a repeated character. Which end moves?", "The left end advances past the earlier copy", "The right end moves backward", "Neither end, because repeats are kept", "The invariant is one copy of each character inside the window.", "Both ends still move only forward across the whole scan."),
        ("prefix-sums", "Prefix totals exist for 1, 2, 3, 4. range_sum(1, 3) uses which formula?", "The total through the exclusive end, minus the total before the start", "The value at index 1 multiplied by the value at index 3", "A fresh loop from index 1 through index 3 inclusive", "The library slice is half-open, so index 3 is excluded.", "The answer on this input is 2 + 3.", ["total of an empty prefix is zero.", "A point update is why a later structure exists."], "prefix-sums-count-target-subarrays", "You know how many earlier prefixes equal the current prefix minus the target. What does that frequency count?", "The subarrays that end here and sum to the target", "The single longest subarray in the whole array", "Only the empty subarray", "Each matching earlier prefix is one start index.", "The walk stores prefix frequencies as it goes."),
        ("backtracking", "A permutation search places an item and then tries the next sibling. What must happen between those siblings?", "The placement is undone so the pool is restored", "The placement stays, so later siblings see a shorter pool", "The search returns without visiting siblings", "Choose, recurse, and undo is the shape.", "The six permutations of three items all share the same pool.", ["A prune must reject every leaf under that branch.", "The output size belongs in the cost."], "backtracking-analyze-search-tree", "How many leaves does the permutation tree of n distinct items have?", "n factorial", "n squared", "n log n", "The first position has n choices and each next position has one fewer.", "Building each list also copies n items."),
        ("greedy-methods", "Interval scheduling sorts by finish time and takes the next compatible interval. What justifies that first choice?", "Some optimal schedule can be exchanged into the same first interval", "The example with three intervals is already a proof", "The longest interval is always optimal", "Swapping in the earliest finish does not reduce the count.", "An example shows the rule. The exchange shows why it is safe.", ["Huffman gives the frequent symbol the short code.", "A different sort key needs its own argument."], "greedy-methods-justify-optimality", "Two lightest symbols become siblings in a Huffman tree. Why is that safe?", "Some optimal tree has those two symbols as siblings", "The heaviest symbol must be deepest", "Any pairing of symbols has the same cost", "The exchange replaces a worse sibling pair with the two lightest.", "The heap then repeats the choice."),
        ("dp-state-and-transition", "Coin change stores one number per amount. What is the state?", "The fewest coins that sum to that amount", "The list of every combination that sums to that amount", "The largest coin that is at most that amount", "The transition tries each coin and reads a smaller amount.", "Amount zero costs zero coins.", ["Fill smaller amounts first.", "The knapsack adds an item index to the state."], "dp-state-analyze-work-memory", "0-1 knapsack has an item index and a capacity. What dominates the time?", "The number of item-capacity pairs, times the work of one transition", "The capacity alone, because items are free", "The factorial of the item count", "Each cell makes a constant number of choices.", "A rolling row can shrink the memory without changing the time."),
        ("string-search", "KMP has matched a proper prefix and then the next character fails. What does the failure link do?", "It resumes at the longest prefix that is also a suffix of the matched text", "It restarts the text index at zero", "It skips the rest of the text", "The text index does not move backward.", "The link is a fact about the pattern, computed before the search.", ["ababa in ababcababa matches at index 5.", "A hash hit still needs a character check."], "string-search-verify-hash-candidates", "Rabin-Karp reports equal hashes for a window and the pattern. What else is required?", "A character-by-character check of that window", "Nothing, because equal hashes are equal strings", "A second modulus only, with no character check", "Different strings can share a hash.", "Unequal hashes are enough to reject a window."),
        ("tries-and-text-indexes", "cat and car are inserted. What does contains report for ca?", "A miss, because a prefix was not inserted as its own key", "A hit, because both keys start with ca", "A hit only when every key has that prefix", "This trie treats stored keys and proper prefixes differently.", "contains walks the whole key.", ["The suffix array of banana starts at 5, 3, 1, 0, 4, 2.", "Build cost is separate from one query."], "text-index-include-build-cost", "You compare a suffix-array query with a scan of the raw text. What must the comparison include?", "The cost of building the array, not only the later binary search", "Only the binary search", "Only the length of the pattern", "An index is not free to construct.", "The array itself is linear in the text."),
        ("range-query-structures", "A Fenwick tree receives point adds and then a prefix query. What do you gain over a flat prefix array?", "A point update stays logarithmic instead of rebuilding the array", "A range query becomes linear", "Updates become constant and queries become linear", "The flat prefix array is the static special case.", "The sparse table answers minima and does not take updates.", ["The segment tree can tag a whole span.", "Say whether the workload updates."], "range-query-select-for-workload", "The array never changes and you need range minima. Which structure fits?", "A sparse table, with a longer build and a constant query", "A Fenwick tree, because it stores minima the same way", "A fresh scan of the range on every query, called constant", "Minimum of overlapping blocks still covers the union.", "A changing array would push you back to a tree."),
        ("approximate-membership", "A Bloom filter says an item is absent. What may you conclude?", "The item was definitely not added", "The item was probably added", "The item was added and then deleted", "add only sets bits, so a clear bit means this item was not inserted.", "A hit can be a false positive.", ["This filter does not support delete.", "A clear bit is the definite answer."], "bloom-filter-explain-false-positive", "A Bloom filter says an item is present. What may you conclude?", "The item might be present, or other items may have set those bits", "The item is definitely present", "The item is definitely absent", "Every checked bit is set, and more than one item can set a bit.", "A definite answer is the miss, not the hit."),
        ("storage-engines-and-locality", "A B-tree and a sequential scan solve different workloads. Which claim matches the scan?", "Touching neighboring items is the baseline when you need every value", "A scan is the fastest way to test one missing key", "A B-tree lookup is linear in the number of keys on every input", "search walks a short path. The scan adds every item.", "Locality changes the practical cost, not the arithmetic identity.", ["Inserted keys are found. Missing keys are not.", "Writes in an LSM land in a log before they land in a tree."], "storage-engines-explain-locality", "Why can two linear scans with the same arithmetic still differ in practice?", "One touches neighboring memory and the other jumps around", "The jumping scan always does fewer additions", "Locality changes the returned sum", "Cache lines and pages reward the tight walk.", "The toy sum is the baseline, not a different formula."),
        ("approximation-guarantees", "The vertex-cover scan adds both ends of an uncovered edge. Why is the result a cover?", "Every edge is either chosen or already touches a chosen vertex", "The scan adds one vertex from the whole graph", "The scan returns a matching and stops", "Feasibility is separate from the ratio.", "The example cover contains all four endpoints.", ["The selected edges do not share vertices.", "The ratio is at most two on every graph."], "approximation-derive-ratio", "The algorithm adds two vertices per selected edge, and those edges are disjoint. How does that bound the ratio?", "Any cover needs at least one vertex per selected edge, so two is at most twice the optimum", "The cover is always the optimum", "The cover can be arbitrarily larger than the optimum", "The disjoint edges are a lower bound on the optimum.", "A single lucky example is not the proof."),
    ]
    built: dict[str, dict[str, object]] = {}
    for row in rows:
        slug = row[0]
        built[slug] = ask(*row[1:])
    return built


EXTRA_QUESTIONS = _questions()
