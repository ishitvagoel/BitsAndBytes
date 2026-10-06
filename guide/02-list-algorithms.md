---
title: List algorithms
slug: list-algorithms
order: 2
status: present
module: bitsandbytes.linked_lists.reverse, bitsandbytes.linked_lists.reverse_in_pairs, bitsandbytes.linked_lists.reverse_in_blocks, bitsandbytes.linked_lists.middle, bitsandbytes.linked_lists.cycle, bitsandbytes.linked_lists.remove_cycle, bitsandbytes.linked_lists.nth_from_end, bitsandbytes.linked_lists.duplicates, bitsandbytes.linked_lists.rotate, bitsandbytes.linked_lists.partition, bitsandbytes.linked_lists.odd_even, bitsandbytes.linked_lists.reorder, bitsandbytes.linked_lists.palindrome, bitsandbytes.linked_lists.delete_node, bitsandbytes.linked_lists.add_numbers, bitsandbytes.linked_lists.merge_sorted, bitsandbytes.linked_lists.intersection, bitsandbytes.linked_lists.sort_list, bitsandbytes.linked_lists.split_circular, bitsandbytes.linked_lists.modular_nodes, bitsandbytes.linked_lists.reviewers
---

This is the legacy overview and complexity index for the repository's list exercises. Use the focused overviews for a first pass through [fast/slow pointers](./fast-slow-pointer-patterns.md), [reversal and relinking](./linked-list-reversal-and-relinking.md), [merge and sort](./linked-list-merge-and-sort.md), and [special input cases](./linked-list-special-cases.md).

These modules only rewrite `next` on that shared list. Any call that starts with `require_linear` inherits that O(n) peak before the main loop.

* `linked_lists/reverse.py` — iterative reversal is O(n) time and O(1) extra memory for the three pointers. The recursive form adds O(n) call-stack memory.
* `linked_lists/reverse_in_pairs.py` — swap neighbours. O(n) time, O(1) extra memory for the loop.
* `linked_lists/reverse_in_blocks.py` — reverse every block of `k`. Each node is touched a constant number of times, so time is O(n), not O(n·k).
* `linked_lists/middle.py` — fast and slow pointers; two different “middles” on even length. O(n) time. See the worked trace in the module docstring.
* `linked_lists/cycle.py` — Floyd’s algorithm finds a cycle entrance. O(n) time, O(1) extra memory for the walk itself.
* `linked_lists/remove_cycle.py` — clear the link that points back at the entrance. O(n) time, O(1) extra memory.
* `linked_lists/nth_from_end.py` — a fixed gap of `n` nodes, then one walk together. O(length) time, O(1) extra memory for the two pointers.
* `linked_lists/duplicates.py` — sorted duplicates are O(n) time and O(1) extra memory. Unsorted duplicates use a set: expected O(n) time and O(n) extra memory.
* `linked_lists/rotate.py`, `partition.py`, `odd_even.py`, `reorder.py` — relinking only. O(n) time, O(1) extra memory for each loop.
* `linked_lists/palindrome.py` — split at the left middle, reverse the second half, compare, restore. O(n) time, O(1) extra memory for the loop.
* `linked_lists/delete_node.py` — copy the successor forward. O(1). Cannot delete the tail.
* `linked_lists/add_numbers.py` — least-significant digit at the head. O(n + m) time, O(1) scratch besides the result nodes.
* `linked_lists/merge_sorted.py` — merge two sorted chains by relinking. O(n + m) time, O(1) extra memory.
* `linked_lists/intersection.py` — `require_linear` on both lists, then equalize with cached lengths and walk in step. O(n + m) time; O(1) extra memory for the walk besides the guard peak.
* `linked_lists/sort_list.py` — bottom-up merge sort. O(n log n) time, O(1) extra memory besides nodes. Stable.
* `linked_lists/split_circular.py`, `modular_nodes.py`, `reviewers.py` — see each module’s `Cost` section. `modular_node_from_end` uses `nth_from_end`, so it is O(n) time and O(1) extra memory for the gap walk.

## Industry

A working engineer rewrites links when the records are already a chain.
Merging two sorted chains has a library twin: Python's `heapq.merge` merges
already-sorted inputs into one sorted output and does not pull every stream
into memory at once. On these lists the same merge relinks the existing
nodes.
