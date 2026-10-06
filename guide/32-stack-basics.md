---
title: Stack basics
slug: stack-basics
order: 32
status: present
module: bitsandbytes.stacks.stack, bitsandbytes.stacks.algorithm_stack
---

## Keep the newest item at the top

A stack follows last-in, first-out order: the most recently pushed item is the next one popped. Its small interface is `push`, `pop`, and often `peek`. Keeping all three operations focused on the top avoids searching through the structure.

**By the end of this overview, you can** trace push/pop order and state the size and capacity invariant of a bounded stack.

## Trace the state

Represent the stack as a list with its top at the right. Starting empty, push `A`, push `B`, then pop: `B` leaves first and `A` remains. After each step, the stack size equals the number of pushes minus pops. For a bounded stack, also require `0 ≤ size ≤ capacity`.

Python lists support end `append` and `pop`, so they are a natural stack implementation. These operations are amortized O(1); a bounded wrapper adds a capacity check. Popping an empty stack and pushing onto a full bounded stack need explicit behavior in the API contract.

## Practice and next step

Trace `push(4), push(9), pop(), push(2), pop()` and name each returned value. Then test empty and capacity-one boundaries. Continue to [monotonic stack patterns](./monotonic-stack-patterns.md) to see how a stack can remember unresolved candidates.
