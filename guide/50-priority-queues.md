---
title: Priority queues
slug: priority-queues
order: 50
status: present
module: bitsandbytes.heaps.priority_queue
---

## The idea

A priority queue returns the best priority, not the oldest item and not the newest item. The library's PriorityQueue is a binary min-heap. push(5, a), push(3, b), and push(4, c) leave 3 at the root. The first pop returns the pair 3, b. Later pops return 4, c and then 5, a. Each push returns a token. decrease_key uses that token to find the heap index without scanning. The heap stores priority, token, and item. The token breaks ties so two equal priorities stay distinct. This is the structure Dijkstra and Prim need when they repeatedly ask for the next smallest tentative weight. Sorting the whole set once is cheaper when you need every item in order and you will not insert anything in between.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Pop | item = b | The smallest priority leaves first. |

## Why it is correct

The heap invariant says every parent priority is less than or equal to its children. push appends and sifts up until the invariant holds. pop swaps the root with the last item, removes the old root, and sifts down. The item that leaves is the minimum because the root is the minimum. decrease_key is allowed to move a priority down, toward a better min, and then sifts up. An equal priority is not a decrease. The map from token to index is updated on every swap, so the next decrease still finds the item.

## What it costs

push and pop are logarithmic in the number of stored items. The token map makes the find step constant time, so it does not hide a linear scan inside the logarithmic sift. Extra memory is the heap array plus the map, both linear. n pushes followed by n pops are n log n, the same family as heapsort. Prefer the queue when the set of candidates changes between extractions. Prefer a sort when the set is fixed.

## Run it

```python
from bitsandbytes.heaps.priority_queue import PriorityQueue
queue = PriorityQueue()
queue.push(5, 'a')
queue.push(3, 'b')
queue.push(4, 'c')
print(queue.pop())
# prints: (3, 'b')
```

## Practice and next step

Answer the checkpoints, then open Graph representations. The checkpoint stays in this browser.
