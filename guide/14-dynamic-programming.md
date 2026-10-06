---
title: Dynamic programming
slug: dynamic-programming
order: 14
status: present
module: bitsandbytes.dynamic_programming.classic
---

* `dynamic_programming/classic.py` — bottom-up Fibonacci mod word, coin change, knapsack, LCS, edit distance, LIS, house robber, word break, DAG longest path, unbounded knapsack.

## Industry

A working engineer computes edit distance with a filled table. PostgreSQL's
`fuzzystrmatch` documentation provides `levenshtein(source, target)`, the
Levenshtein distance, and charges 1 for an insertion, a deletion, or a
substitution when those costs are left at their defaults. `edit_distance` in
this module is that recurrence, filled bottom-up so each cell is computed
once.
