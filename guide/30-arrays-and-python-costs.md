---
title: Arrays and Python sequence costs
slug: arrays-and-python-costs
order: 30
status: present
module: bitsandbytes.library_costs
---

## Use the operation a sequence is built for

Python's `list` stores an indexed sequence and supports direct access by position. It is a good fit when iteration, indexing, and changes near the end dominate. A queue that repeatedly removes its first element performs a different operation pattern.

**By the end of this overview, you can** choose a sequence based on its operations and distinguish an individual append from an expensive insertion near the front.

## Compare work and memory

Inserting or deleting near index 0 of a list shifts the later references, taking O(n) time. Repeating `pop(0)` n times can therefore perform Θ(n²) total movement. `collections.deque` supports endpoint operations in approximately O(1) time, so it better matches FIFO queue behavior. It is not a replacement for fast arbitrary middle indexing.

Appending to a dynamic array may occasionally resize and copy its storage. Over a long sequence of appends, the total resizing work is spread across operations; this is amortized analysis. A single append can still be more expensive than O(1), so distinguish per-operation worst case from amortized cost.

The implementation helpers in `bitsandbytes.library_costs` compare queue removal, sorted insertion, top-k selection, and sorting. Read their preconditions before transferring one cost claim to a different data structure.

## Practice and next step

Choose between a list and deque for a FIFO queue and for repeated middle indexing. Explain the two different tradeoffs. Continue to [recursion and recurrences](./recursion-and-recurrences.md).
