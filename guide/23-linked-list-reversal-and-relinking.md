---
title: Linked-list reversal and relinking
slug: linked-list-reversal-and-relinking
order: 23
status: present
module: bitsandbytes.linked_lists.reverse, bitsandbytes.linked_lists.reverse_in_pairs, bitsandbytes.linked_lists.reverse_in_blocks, bitsandbytes.linked_lists.rotate, bitsandbytes.linked_lists.partition, bitsandbytes.linked_lists.odd_even, bitsandbytes.linked_lists.reorder
---

## The idea

Reversal rearranges a chain by changing next references, not by copying values. Before you overwrite a link, save the node that follows it. Otherwise the unvisited suffix becomes unreachable. reverse_iterative keeps three names. previous is the reversed prefix. current is the node being flipped. upcoming is the saved suffix. The library starts previous empty and current at the head. Each step saves current.next, points current.next at previous, then advances both moving names. When current is empty, previous is the new head. On 1, 2, 3 the result is 3, 2, 1. Pair and block reversal reuse the same invariant. They must also reconnect the previous block to the new head of the current block, and connect that block's tail to the untouched suffix. Rotation finds a new tail, makes the chain temporarily circular, then cuts it. Partition and odd-even grouping keep separate tails, then join the chains.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Reversed | head = 3 | The head is now 3. |

## Why it is correct

The invariant is that previous is a reversed chain of the nodes already visited, and current still heads the original suffix. It holds at the start because the prefix is empty and current is the whole list. One step moves current onto the prefix and leaves upcoming as the rest, so the invariant holds again. No node is dropped because upcoming was saved before the write. The loop stops when current is empty, so every node is on the reversed prefix. A recursive reversal rewrites the same links and can use a linear call stack. The iterative version stores three references. For every pointer write, name which node still owns the remaining suffix.

## What it costs

The loop body runs once per node. Each iteration reads and writes a constant number of pointers, so the time is linear and the reversal itself uses constant extra memory. require_linear can hold a set of ids while it runs, and that peak is separate from the three pointers. A recursive version adds a linear stack. Trace an empty list, a one-node list, a two-node list, and a block size larger than the list. A linear input must stay linear, and every original node must appear once.

## Run it

```python
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.reverse import reverse_iterative
chain = LinkedList()
for item in (1, 2, 3):
    chain.append(item)
reverse_iterative(chain)
print(list(chain))
# prints: [3, 2, 1]
```

## Practice and next step

Answer the checkpoints, then open Linked-list merge and sort. The checkpoint stays in this browser.
