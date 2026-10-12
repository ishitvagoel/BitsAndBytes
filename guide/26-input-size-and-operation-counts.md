---
title: Input size and operation counts
slug: input-size-and-operation-counts
order: 26
status: present
module: bitsandbytes.complexity
---

## The idea

For n = 4 the nested pair scan checks 6 pairs. The exact count is 4 * 3 / 2.

Name the input size before you count work. For one list, n is the number of items. For a graph, say V vertices and E edges instead of one n. An operation is one comparison, one link follow, or one arithmetic step that does not itself hide a loop. A single loop from 0 to n - 1 does n iterations. A nested loop that compares every index with every later index does (n - 1) + (n - 2) + ... + 1 checks. That sum is n(n - 1) / 2. Dropping the constant 1/2 and the lower term is a later step. This lesson keeps the exact count so the next lesson has something real to bound.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Pair | count = 1 | Compare 3 with 1. The pair count is 1. |
| Pair | count = 2 | Compare 3 with 2. The pair count is 2. |
| Pair | count = 3 | Compare 1 with 2. The pair count is 3. |

## Why it is correct

The count is correct because every pair of indexes i < j is visited once. Index i is the outer loop, and j runs from i + 1 to n - 1. No pair is skipped, and no pair is counted twice. The closed form n(n - 1) / 2 is the formula for the sum of the first n - 1 positive integers. For n = 4 the trace records 3 + 2 + 1 = 6, and 4 * 3 / 2 = 6.

## A common mistake

Counting n times n double-counts every pair. The inner loop only looks to the right of i.

## What it costs

The pair scan does n(n - 1) / 2 comparisons, which grows like n squared. Memory besides the input is a handful of indexes, a constant amount of extra memory. Suppose the inner loop ran over the whole list. The count would then be n times n. That is the same growth with a different constant.

## Run it

```python
from bitsandbytes.complexity import pair_comparison_count
print(pair_comparison_count([3, 1, 2]))
# prints: 3
```

## Practice and next step

Open Asymptotic growth next. Asymptotic growth replaces this exact count with a tight bound.
