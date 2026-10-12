---
title: Cost models and assumptions
slug: cost-models
order: 28
status: present
module: bitsandbytes.complexity, bitsandbytes.library_costs
---

## The idea

list_pop_front_cost_demo(3) returns 2 reference moves.

A complexity claim is true only inside a stated model. The word-RAM model charges one step for a comparison, a pointer write, or word-sized arithmetic. That model fits a list of machine words. It is the wrong model when one named step hides a loop. A Python list is a dynamic array of references. Reading an index is one address calculation. list.pop(0) moves every later reference one slot toward index 0. list_pop_front_cost_demo(3) returns 2. Those two writes are the items that remain after the front item leaves. A linked list has no constant-time middle. Binary search stays logarithmic only when each index is constant time. Count the container operation the code actually performs. State a key-size assumption before you call hashing constant time. Count the recursion stack apart from the loop variables. The point of this lesson is to separate algorithm steps from Python container costs.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Start | moved = 0 | A list of length 3 has moved 0 references so far. |
| Slide | moved = 1 | A list of length 3 has moved 1 references so far. |
| Slide | moved = 2 | A list of length 3 has moved 2 references so far. |

## Why it is correct

The demo returns length minus 1 for a positive length. A list of three items has two items behind the front. Each of those items slides one slot. The spare capacity of a list sits at the end, not at index 0. Binary search on a list is logarithmic because each middle index is constant time. The same comparisons on a linked list walk from the head. The elapsed work is then linear in the index, not logarithmic. bisect.insort is linear overall because the insertion dominates the logarithmic search. A deque documents approximately constant-time endpoint appends and pops. The bound and the container belong in the same sentence.

## A common mistake

The comparison count is not the elapsed work when each comparison hides a walk.

## What it costs

One pop(0) on n items moves n - 1 references. That is linear in n. Draining n items from the front moves about n squared over 2 references. n calls to deque.popleft are linear in total. The demo computes length minus 1 and does not build the list. Reporting a logarithmic bound without saying random-access hides the linked-list case. The assumption is part of the claim. A later lesson can turn this exact count into a tight growth bound. One pop(0) is Θ(n) time, and the demo uses O(1) extra memory.

## Run it

```python
from bitsandbytes.library_costs import list_pop_front_cost_demo
print(list_pop_front_cost_demo(3))
# prints: 2
```

## Practice and next step

Open Loop invariants next. Loop invariants are the statements that make a later count mean the result you wanted.
