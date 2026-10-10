---
title: Recursion and recurrences
slug: recursion-and-recurrences
order: 31
status: present
module: bitsandbytes.complexity
---

## The idea

A recurrence describes a function that calls itself. The one you will meet in merge sort is T(n) = 2 T(n/2) + Θ(n), with T(1) = Θ(1). The 2 T(n/2) is the two recursive calls. The Θ(n) is the work to merge the halves. Unrolling the recurrence shows log2(n) levels, because the input size halves each time, and Θ(n) work on every level, because the pieces at one level add up to n. The product is Θ(n log n). The call stack on one path is Θ(log n) frames deep. That is extra memory even when each frame stores only a few indexes.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Level 0 | size = 8, level = 0 | The root call holds all 8 items. |
| Level 1 | size = 4, level = 1 | One child holds 4 items. The other child is the same size. |
| Level 2 | size = 2, level = 2 | The next call holds 2 items. |
| Level 3 | size = 1, level = 3 | The leaf holds 1 item. log2(8) is 3. |

## Why it is correct

The level count is exact for powers of two. n, n/2, n/4, ..., 1 is log2(n) steps. At level i there are 2^i calls and each call works on n / 2^i items, so the level sums to n. Adding log2(n) levels of n work gives n log2(n). The base case stops the recurrence, which is the same role termination plays for a loop. An unbalanced recursion such as T(n) = T(n - 1) + Θ(n) has n levels and Θ(n²) total work. The shape of the calls is the whole story.

## What it costs

Time is the unrolled sum, Θ(n log n) for the balanced split. Stack memory is proportional to the deepest chain of calls, Θ(log n) when every split is even and Θ(n) when each call peels off one item. Report both. A time bound does not imply a stack bound.

Merge sort is this recurrence with a balanced split. A quicksort pivot that always peels off one item is the other shape, T(n) = T(n - 1) + Θ(n). Same lesson, different tree. Ask which shape you have before you quote n log n.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
