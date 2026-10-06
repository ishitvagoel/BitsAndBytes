---
title: Greedy algorithms
slug: greedy-algorithms
order: 15
status: present
module: bitsandbytes.greedy.classic
---

* `greedy/classic.py` — interval scheduling, fractional knapsack, Huffman codes.

## Industry

A working engineer uses a min-heap when the greedy choice is the lightest
remaining weight. Huffman coding in this module repeatedly takes the two
lightest weights with `heapq.heappop`. Python documents a min-heap whose
smallest item is `heap[0]`, and `heappop` returns that item.
