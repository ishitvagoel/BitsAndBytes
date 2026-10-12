---
title: Two-pointer patterns
slug: two-pointers
order: 58
status: present
module: bitsandbytes.patterns.arrays
---

## The idea

two_sum_sorted on 1, 2, 4, 7 with target 6 returns indexes 1 and 2.

Two pointers scan a sorted array from the ends, or scan a sequence with a start and an end that only move forward. two_sum_sorted on 1, 2, 4, 7 with target 6 returns indexes 1 and 2, the positions of 2 and 4. The left index starts at 0 and the right index starts at the last item. If the sum is too small, the left index moves right, because every value further left is even smaller. If the sum is too large, the right index moves left. Each move throws away a value that cannot be part of any remaining pair. The loop stops when the indexes meet. A pair of nested loops would also find the pair, and would check every combination.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Move | sum = 8 | Indexes 0 and 3 sum to 8. |
| Move | sum = 5 | Indexes 0 and 2 sum to 5. |
| Move | sum = 6 | Indexes 1 and 2 sum to 6. |

## Why it is correct

The invariant is that any solution still available uses a left index at or after the current left. It also uses a right index at or before the current right. It holds at the start because the whole array is inside that range. Moving the left index forward is safe when the sum is too small. The current left value plus any value to the left of the right index is even smaller. The symmetric argument moves the right index. Sorted order is the assumption. Without it, a larger index is not a larger value, and the move is not safe.

## A common mistake

If the array is not sorted, moving the left index does not guarantee a larger sum.

## What it costs

Each index moves at most n times, and only in one direction, so the total time is linear. Extra memory is the two indexes. The nested pair scan is quadratic. State the sorted precondition before you quote the linear bound. If the array is not sorted, sorting it first costs n log n and the two-pointer scan is no longer the whole story. The scan is Θ(n) time and O(1) extra memory.

## Run it

```python
from bitsandbytes.patterns.arrays import two_sum_sorted
print(two_sum_sorted([1, 2, 4, 7], 6))
# prints: (1, 2)
```

## Practice and next step

Open Sliding windows next. A sliding window keeps a fact about a slice whose ends only move forward.
