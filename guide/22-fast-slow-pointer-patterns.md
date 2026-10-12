---
title: Fast and slow pointers
slug: fast-slow-pointer-patterns
order: 22
status: present
module: bitsandbytes.linked_lists.middle, bitsandbytes.linked_lists.cycle, bitsandbytes.linked_lists.remove_cycle, bitsandbytes.linked_lists.nth_from_end, bitsandbytes.linked_lists.palindrome, bitsandbytes.linked_lists.modular_nodes
---

## The idea

On the list 1, 2, 3, 4, 5 the slow pointer stops on 3.

A linked list has no index, so two pointers replace a length calculation. The fast pointer moves two links for every one link the slow pointer moves. When fast falls off a linear list, slow is at a middle node. middle_node on 1, 2, 3, 4, 5 returns the node holding 3. On an even list the same function returns the second of the two middles. middle_node on 1, 2, 3, 4 returns 3. end_of_first_half stops one step sooner and returns 2, the left middle. Palindrome and reorder split there. If the links form a cycle, fast gains one node per iteration and meets slow inside the cycle. Reset one pointer to the head and walk both one step at a time. They meet at the entrance. On 1 through 5 with the tail linked to 3, find_cycle_start returns index 3. A fixed gap finds a node from the end. Move a lead pointer k links ahead, then move both pointers together. The gap stays k.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Middle | middle = 3 | The slow pointer on 1 through 5 stops on 3. |
| Even | middle = 3 | The even list 1 through 4 keeps the later middle 3. |
| Entrance | index = 3 | The cycle entrance is the node holding 3. |

## Why it is correct

The speed ratio is the whole argument. Fast takes two steps while slow takes one, so slow has seen half the nodes when fast finishes a linear list. The even-length choice is a contract. Stopping when fast cannot take two more steps keeps the later middle. Stopping when fast.next.next is missing keeps the earlier middle. Both land on the single middle when the length is odd. Inside a cycle the same ratio makes a meeting inevitable, because fast closes the gap by one node each iteration. The entrance walk works because the meeting point is a known number of steps from the entrance, matching the distance from the head. The gap method needs no subtraction. When the lead falls off, the trailer is k nodes from the end.

## A common mistake

On an even length the function returns the later middle, not the earlier one.

## What it costs

Each walk examines each link a constant number of times, so the time is linear in the number of nodes. The pointer walk stores a constant number of references. require_linear may hold a set of node ids while it checks for a cycle, and that set is a separate cost from the two-pointer loop. Say which one you are counting. Before you call one of these functions, state the even-length rule, what k means, and whether a cycle is allowed. Test an empty list, one node, an even length, and a cycle against that contract. The walk is Θ(n) time and O(1) extra memory for the pointers.

## Run it

```python
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.middle import middle_node
chain = LinkedList()
for item in (1, 2, 3, 4, 5):
    chain.append(item)
print(middle_node(chain).data)
# prints: 3
```

## Practice and next step

Open Linked-list reversal and relinking next. Reversal and relinking show the pointer you must save before you overwrite next.
