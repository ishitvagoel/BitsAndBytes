---
title: Recursion and recurrences
slug: recursion-and-recurrences
order: 31
status: present
module: bitsandbytes.complexity
---

## The idea

A merge-divide tree on n = 8 has 4 levels, and each level does 8 units of work.

A recurrence describes a function that calls itself. The one you will meet in merge sort is T(n) = 2 T(n/2) + Θ(n), with T(1) = Θ(1). The 2 T(n/2) is the two recursive calls. The Θ(n) is the work to merge the halves. Unrolling the recurrence shows log2(n) levels, because the input size halves each time. Each level does Θ(n) work, because the pieces at one level add up to n. The product is Θ(n log n). The call stack on one path is Θ(log n) frames deep. That is extra memory even when each frame stores only a few indexes.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Level 0 | work = 8 | Level 0 has 1 calls of size 8. The level still does 8 work. |
| Level 1 | work = 8 | Level 1 has 2 calls of size 4. The level still does 8 work. |
| Level 2 | work = 8 | Level 2 has 4 calls of size 2. The level still does 8 work. |
| Level 3 | work = 8 | Level 3 has 8 calls of size 1. The level still does 8 work. |

## Why it is correct

The level count is exact for powers of two. n, n/2, n/4, ..., 1 is log2(n) steps. At level i there are 2^i calls and each call works on n / 2^i items, so the level sums to n. Adding log2(n) levels of n work gives n log2(n). The base case stops the recurrence, which is the same role termination plays for a loop. An unbalanced recursion such as T(n) = T(n - 1) + Θ(n) has n levels and Θ(n²) total work. The shape of the calls is the whole story.

## A common mistake

Depth and total work are different. A short depth can still do linear work on every level.

## What it costs

Time is the unrolled sum, Θ(n log n) for the balanced split. Stack memory is proportional to the deepest chain of calls. It is Θ(log n) when every split is even. It is Θ(n) when each call peels off one item. Report the time and the stack. A time bound does not imply a stack bound.

Merge sort is this recurrence with a balanced split. A quicksort pivot that always peels off one item is the other shape, T(n) = T(n - 1) + Θ(n). Same lesson, different tree. Ask which shape you have before you quote n log n.

## Run it

```python
from bitsandbytes.sorting.merge_sort import merge_sort
print(merge_sort([3, 1, 4, 2]))
# prints: [1, 2, 3, 4]
```

## Practice and next step

Open Singly linked list next. A singly linked list is the first structure whose cost depends on which pointer you hold.
