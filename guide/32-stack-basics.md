---
title: Stack basics
slug: stack-basics
order: 32
status: present
module: bitsandbytes.stacks.stack, bitsandbytes.stacks.algorithm_stack
---

## The idea

A stack is a last-in, first-out sequence. push adds an item at the top. pop removes that same item. The size invariant is 0 ≤ size ≤ limit for a bounded stack, and size changes by exactly 1 on every successful push or pop. The teaching Stack in this repository stores items in a Python list and rejects a push that would pass the limit. After push 1, push 2, push 3, the first pop returns 3 and the second returns 2. That order is the definition, not an accident of the example.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Push 1 | size = 1, top = 1 | The stack holds one item. Size is 1. |
| Push 2 | size = 2, top = 2 | 2 is the new top. 1 stays underneath. |
| Push 3 | size = 3, top = 3 | 3 is the top. The push order was 1, 2, 3. |
| Pop, pop | size = 1, returned = 2 | The first pop returns 3. The second pop returns 2. 1 remains. |

## Why it is correct

Each push writes one reference at the end of the list, which is the top. Each pop reads and removes that end. No operation reaches under the top, so the item pushed most recently is the item removed first. The size invariant holds by induction. It is 0 on an empty stack. A successful push adds 1 and a successful pop subtracts 1, and both refuse to step outside 0 and limit. When the stack is empty, pop has nothing to return. When it is full, push has no slot that stays within the limit.

## What it costs

push and pop at the end of a list are amortized Θ(1), and on this bounded stack they are Θ(1) because the list does not need to grow past the items you actually pushed within the limit. Extra memory is Θ(n) for n stored items. A stack does not offer Θ(1) access to the bottom. If you need the other end, use a queue.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
