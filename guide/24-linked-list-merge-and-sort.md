---
title: Linked-list merge and sort
slug: linked-list-merge-and-sort
order: 24
status: present
module: bitsandbytes.linked_lists.merge_sorted, bitsandbytes.linked_lists.sort_list, bitsandbytes.linked_lists.intersection
---

## Reuse order already present in linked lists

When two chains are sorted, compare only their current heads. Append the smaller head to the result and advance that input. Once one input is empty, attach the other suffix; it is already in order.

**By the end of this overview, you can** explain why merging visits each node a constant number of times and why bottom-up merge sort suits linked lists without random access.

## Merge and sort

For input lengths `n` and `m`, merge takes O(n + m) comparisons and link updates. A dummy head can make the first append use the same code path as later appends. If the implementation relinks existing nodes, the result does not require a second array of values.

Bottom-up merge sort repeatedly combines adjacent runs of width 1, 2, 4, and so on. There are O(log n) rounds, and each round visits O(n) nodes, giving O(n log n) time. It can use O(1) auxiliary node references beyond the list nodes. Stable merge chooses the left item when keys compare equal, preserving their original order.

Intersection is a different question: after confirming both chains are linear, equalize the distance to the ends and advance together. The key is to compare node identity, not equal values. The guard that checks whether the chains are valid has its own cost and should be counted separately from the final walk.

## Practice and next step

Merge `[1, 4, 8]` and `[2, 3]` by writing the pair of head values at each comparison. Count how many times each input node is selected or attached. Then explain why sorting a linked list by repeatedly indexing its middle would lose the array-style access cost assumption.

Compare with [the repository merge/sort implementation tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list_algorithms.py) and continue to [special linked-list cases](./linked-list-special-cases.md).
