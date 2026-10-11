---
title: Dynamic-array growth
slug: dynamic-array-growth
order: 36
status: present
module: bitsandbytes.linear.dynamic_array
---

## The idea

A dynamic array stores items in a contiguous block and remembers a length and a capacity. append writes into the next free slot when length < capacity. When the block is full, the array allocates a new block with twice the capacity, copies the old references, and then writes the new item. The example starts at capacity 1. Appending a, b, and c copies 0, then 1, then 2 references. The library's DynamicArray.capacity after those three appends is 4, and the stored items are a, b, c.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Resize | capacity = 2 | The grow copied 1 references. |
| Resize | capacity = 4 | The grow copied 2 references. |

## Why it is correct

Each resize copies every item that is already stored, because the new block is a different region of memory. Doubling is what makes the total copy count linear. The copy sizes are 1 + 2 + 4 + ... + n/2, which is less than n. Every item is copied once per doubling that happens after it was appended, and an item appended. When the length is about n/2 is copied only once more before the length reaches n. Charging each append a constant amount covers all of those copies. That charge is the amortized bound.

## What it costs

One append is O(1) amortized and O(n) in the worst single call, the call that resizes. n appends copy fewer than 2n references in total, so the aggregate time is Θ(n) and the extra memory is Θ(n) for the block. A growth factor of 1, adding one slot each time, would copy Θ(n²) references. The factor, not the mere fact of resizing, is the reason append is cheap on average.

## Run it

```python
from bitsandbytes.linear.dynamic_array import DynamicArray
array = DynamicArray()
print(array.total_copy_cost_for_appends(3))
# prints: 3
```

## Practice and next step

Answer the checkpoints, then open Recursion and recurrences. The checkpoint stays in this browser.
