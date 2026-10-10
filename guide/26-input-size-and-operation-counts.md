---
title: Input size and operation counts
slug: input-size-and-operation-counts
order: 26
status: present
module: bitsandbytes.complexity
---

## The idea

Name the input size before you count work. For one list, n is the number of items. For a graph, say V vertices and E edges instead of one n. An operation is one comparison, one link follow, or one arithmetic step that does not itself hide a loop. A single loop from 0 to n - 1 does n iterations. A nested loop that compares every index with every later index does (n - 1) + (n - 2) + ... + 1 checks. That sum is n(n - 1) / 2. Dropping the constant 1/2 and the lower term is a later step. This lesson keeps the exact count so the next lesson has something real to bound.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Start | checks = 0, n = 4 | Nothing has been compared. n is 4. |
| Outer 0 | checks = 3, outer = 0 | Index 0 pairs with the three items to its right. |
| Outer 1 | checks = 5, outer = 1 | Index 1 pairs with two items to its right. The total is 5. |
| Outer 2 | checks = 6, outer = 2 | Index 2 pairs with one item. The total is 6, which is 4 * 3 / 2. |

## Why it is correct

The count is correct because every pair of indexes i < j is visited once. Index i is the outer loop, and j runs from i + 1 to n - 1. No pair is skipped, and no pair is counted twice. The closed form n(n - 1) / 2 is the formula for the sum of the first n - 1 positive integers. For n = 4 the trace records 3 + 2 + 1 = 6, and 4 * 3 / 2 = 6.

## What it costs

The pair scan does Θ(n²) comparisons. Memory besides the input is a handful of indexes, so extra memory is O(1). If the inner loop ran over the whole list instead of only the right side, the count would be n², which is the same growth with a different constant.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
