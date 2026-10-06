---
title: Recursion and recurrences
slug: recursion-and-recurrences
order: 31
status: present
module: bitsandbytes.complexity
---

## Relate recursive calls to total work

Recursion solves a problem by calling a function on smaller inputs. A recurrence describes the cost of those calls plus work done outside them. Identify the base case, subproblem sizes, number of calls, and work per level before choosing a bound.

**By the end of this overview, you can** recognize the recurrences for halving, merge-and-divide, and a linear worst-case chain.

## Three common shapes

Binary search has one half-size call and constant comparison work: `T(n) = T(n/2) + O(1)`, which is Θ(log n). Merge sort has two half-size calls and linear merge work: `T(n) = 2T(n/2) + O(n)`, which is Θ(n log n). A badly unbalanced quicksort split may do one size-`n-1` call and scan `n` items: `T(n) = T(n-1) + O(n)`, which is Θ(n²).

The recursion tree exposes the same totals: count levels and work at each level. Also count call-stack memory. This repository's [`recursion_limit`](https://docs.python.org/3/library/sys.html#sys.getrecursionlimit) helper reports CPython's active limit; Python does not eliminate tail calls.

## Practice and next step

For `T(n) = T(n/2) + O(1)`, count the number of levels for `n = 16`. Then describe the work at each level of merge sort. Continue to [linked-list structures](./singly-linked-list.md) with the cost model in mind.
