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
| Example | n = 3 | The lesson counts this input. |

## Why it is correct

The count is correct because every pair of indexes i < j is visited once. Index i is the outer loop, and j runs from i + 1 to n - 1. No pair is skipped, and no pair is counted twice. The closed form n(n - 1) / 2 is the formula for the sum of the first n - 1 positive integers. For n = 4 the trace records 3 + 2 + 1 = 6, and 4 * 3 / 2 = 6.

## What it costs

The pair scan does n(n - 1) / 2 comparisons, which grows like n squared. Memory besides the input is a handful of indexes, a constant amount of extra memory. If the inner loop ran over the whole list instead of only the right side. The count would be n times n, which is the same growth with a different constant.

## Run it

```python
n = 6
print(n * (n - 1) // 2)
# prints: 15
```

## Practice and next step

Answer the checkpoints, then open Asymptotic growth. The checkpoint stays in this browser.
