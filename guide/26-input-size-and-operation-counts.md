---
title: Input size and operation counts
slug: input-size-and-operation-counts
order: 26
status: present
module: bitsandbytes.complexity
---

## Choose the quantity that grows

Algorithm analysis starts by naming the input size. For a list, it is usually the number of elements `n`; for a graph, it may be both the number of vertices `V` and edges `E`; for a string, it is its length. State the quantity before counting work so the result can be compared across inputs.

**By the end of this overview, you can** choose a useful input-size variable and count the operations in a simple loop or nested loop.

## Count work, then simplify

A loop that visits each of `n` items performs a fixed amount of work per item, so its total is proportional to `n`. Two consecutive full passes perform about `2n` steps; the constant factor does not change the growth class. A nested loop that compares every pair performs `n × n` comparisons, or `n²`.

When a loop stops early, distinguish best, typical, and worst input behavior if the algorithm's contract permits all three. Do not treat one observed run as a worst-case proof. Also separate preprocessing from the operation being analyzed: searching a list that must first be sorted includes both costs if the input is not already sorted.

## Practice and next step

For a loop over `n` values followed by a second loop over the same values, write a rough count and state what happens when `n` doubles. Then count the comparisons in a triangular nested loop. Continue to [asymptotic growth](./asymptotic-growth.md) to express these counts compactly.
