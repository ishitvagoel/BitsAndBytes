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
| Append a | length = 1, capacity = 1, copies = 0 | Length 1, capacity 1. No copy. |
| Append b | length = 2, capacity = 2, copies = 1 | The array is full, so it doubles to 2 and copies a, then writes b. |
| Append c | length = 3, capacity = 4, copies = 3 | The array is full again. It doubles to 4 and copies a and b, then writes c. |

## Why it is correct

Each resize copies every item that is already stored, because the new block is a different region of memory. Doubling is what makes the total copy count linear. The copy sizes are 1 + 2 + 4 + ... + n/2, which is less than n. Every item is copied once per doubling that happens after it was appended, and an item appended when the length is about n/2 is copied only once more before the length reaches n. Charging each append a constant amount covers all of those copies. That charge is the amortized bound.

## What it costs

One append is O(1) amortized and O(n) in the worst single call, the call that resizes. n appends copy fewer than 2n references in total, so the aggregate time is Θ(n) and the extra memory is Θ(n) for the block. A growth factor of 1, adding one slot each time, would copy Θ(n²) references. The factor, not the mere fact of resizing, is the reason append is cheap on average.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
