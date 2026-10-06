---
title: Dynamic-array growth
slug: dynamic-array-growth
order: 36
status: present
module: bitsandbytes.linear.dynamic_array
---

## Grow capacity without copying on every append

A dynamic array keeps a logical size and a backing capacity. When there is room, append writes into the next slot. When full, it allocates a larger buffer and copies existing elements before adding the new value.

**By the end of this overview, you can** distinguish one resize from the total work of a long append sequence and explain amortized O(1) append.

## Count the copies

With geometric growth, capacities might double: 1, 2, 4, 8, and so on. A resize copies the old contents, but the total copies through `n` appends are bounded by a geometric sum smaller than a constant multiple of `n`. The sequence therefore takes O(n) total append work, or amortized O(1) per append. A particular append that triggers a resize still takes O(n).

The space cost is O(capacity), which may be larger than the number of stored elements. This tradeoff buys fast indexed access and inexpensive growth on average. A fixed-capacity circular queue has a different contract: it does not grow and must decide what happens when full.

## Practice and next step

For capacities 1, 2, 4 and 8, write the number of elements copied at each resize while appending 9 items. Sum those copies and compare with 9. See the [repository dynamic-array implementation and tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_queues.py).
