---
title: Monotonic stack patterns
slug: monotonic-stack-patterns
order: 33
status: present
module: bitsandbytes.stacks.next_greater, bitsandbytes.stacks.stock_span, bitsandbytes.stacks.largest_rectangle
---

## Keep unresolved candidates in order

A monotonic stack stores candidates in increasing or decreasing order. When a new value makes earlier candidates impossible, pop those candidates and resolve their answers. Each item is pushed once and popped at most once.

**By the end of this overview, you can** explain why a next-greater scan is linear even though an iteration may pop several items.

## Work an example

For values `[2, 1, 3]`, the `3` is the next greater value for both `2` and `1`. Before processing `3`, both indexes may be unresolved on a decreasing stack. Processing `3` pops them and records the answer. No popped index is examined again.

Across `n` inputs, there are at most `n` pushes and `n` pops, so total stack work is O(n), not O(n²). The stack may hold O(n) indexes. The same pattern supports stock span and histogram rectangle problems, but the comparison condition and sentinel handling must match each problem's definition.

## Practice and next step

Trace `[2, 1, 3]`, listing the stack after every input and the index resolved at each pop. Then change the final value to `0` and explain which indexes remain unresolved. Compare with [the repository monotonic-stack tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_stack_algorithms.py).
