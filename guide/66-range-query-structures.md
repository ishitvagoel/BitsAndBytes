---
title: Range-query structures
slug: range-query-structures
order: 66
status: present
module: bitsandbytes.range_queries.structures
---

## Match updates and queries

A Fenwick tree supports prefix sums and point updates in O(log n) time using a compact array. A segment tree supports more general associative range queries and point updates in O(log n); lazy propagation can defer range updates across covered nodes.

## Use static preprocessing when updates are absent

A sparse table answers idempotent range-minimum queries in O(1) after O(n log n) preprocessing, but it does not support arbitrary point updates efficiently. Choose from the operation set, not from a structure's name.

## Practice

Compare Fenwick, segment tree and sparse table for point updates plus range sum, static range minimum, and range assignment plus range sum.

Source: [`structures.py`](../bitsandbytes/range_queries/structures.py).
