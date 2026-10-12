---
title: Loop invariants
slug: loop-invariants
order: 29
status: present
module: bitsandbytes.complexity
---

## The idea

Insertion sort on [3, 1, 2] writes the prefix [1, 3] before it looks at 2.

A loop invariant is a statement that is true before the loop and after every iteration. It is the reason the loop's final state means what you think it means. Three checks make the argument. Initialization says the statement holds before the first iteration. Preservation says one iteration that starts from a true statement ends with the statement still true. Termination says the loop stops, and the invariant plus the exit condition is the result you wanted. Insertion sort's invariant is that the prefix values[0:i] is sorted at the start of the outer step that inserts values[i].

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| start | list = [3, 1, 2] | The input is 3, 1, 2. Nothing is inserted yet. |
| insert | list = [1, 3, 2] | After inserting 1, the prefix through index 1 is sorted. |
| insert | list = [1, 2, 3] | After inserting 2, the prefix through index 2 is sorted. |

## Why it is correct

Initialization holds because a prefix of one item is sorted, and the loop starts inserting at index 1. Preservation holds because the inner loop shifts every larger prefix item one slot right and writes the new key into the hole. The items that were sorted stay in order, and the new key sits between a smaller or equal left neighbor and a larger right neighbor. Termination holds because i runs from 1 to n - 1 and then stops. The prefix is the whole list, so the list is sorted. The library's insertion sort uses a strict < comparison, so an equal key does not move past an earlier equal key. Equal keys keep the order they already had.

## A common mistake

A sorted prefix still allows equal keys in either order. Stability is a stronger claim.

## What it costs

The invariant does not by itself give the time bound. Counting the shifts does. On reverse-sorted input the step for i shifts i items, and the sum is n(n - 1) / 2, so the time is Θ(n²). On sorted input the inner loop never shifts, so the time is Θ(n). Extra memory is the hole index and the saved key, O(1).

## Run it

```python
from bitsandbytes.sorting.insertion_sort import insertion_sort
seen = []
def sink(event):
    seen.append(list(event.values['values']))
insertion_sort([3, 1, 2], trace_sink=sink)
print(seen)
# prints: [[3, 1, 2], [1, 3, 2], [1, 2, 3]]
```

## Practice and next step

Open Arrays and Python sequence costs next. Arrays and Python sequence costs show which container makes an index cheap.
