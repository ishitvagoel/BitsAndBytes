---
title: Special linked-list cases
slug: linked-list-special-cases
order: 25
status: present
module: bitsandbytes.linked_lists.duplicates, bitsandbytes.linked_lists.delete_node, bitsandbytes.linked_lists.add_numbers, bitsandbytes.linked_lists.split_circular, bitsandbytes.linked_lists.reviewers
---

## The idea

Some linked-list routines are valid only under a contract that is easy to miss. Values may be sorted. Digits may be stored least-significant digit first. A circular list may have a distinguished head. The function may receive one node and not the list head. nth_from_end makes its contract explicit. n is 1-based, and 1 means the tail. On 1, 2, 3, 4, nth_from_end with n equal to 2 returns the node holding 3. The leader walks n steps first. Then the leader and the trailer walk together. When the leader falls off, the trailer is the requested node. Removing adjacent duplicates in a sorted list needs only a neighbor comparison. The sorted precondition is what makes that enough. An unsorted list needs a set of seen values, which changes the memory. Deleting a node without the list head can copy the successor and bypass it. That trick cannot remove the tail, because there is no successor to copy. Adding numbers stored least-significant digit first can walk both heads and carry one digit. Splitting a circular list must restore two cycles and handle an odd count and an even count.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| From end | node = 3 | Two steps from the end lands on 3. |

## Why it is correct

The gap stays n because both pointers move one step after the leader's head start. The trailer therefore sits n nodes behind the leader for the rest of the walk. No length subtraction is required. The sorted-duplicate claim fails as soon as an inversion exists, because a later duplicate is not beside its earlier copy. The headless delete fails on the tail for a structural reason, not an off-by-one. There is no next node whose value can be copied back. A circular split is wrong if either result is linear or if the two cycles share a node. Name the input shape, the output shape, and whether existing nodes are mutated.

## What it costs

The leader takes n steps and then both pointers take the remaining steps. The total is linear in the length. Extra memory for the gap is two references. Counting the length and then walking length minus n is the same linear bound. The gap removes the subtraction, not the scan. A set of seen values for unsorted duplicates is linear extra memory. Copying a successor is constant time only when the successor exists. Test the empty list, one node, the last node, a duplicate run, and the smallest valid cycle or digit list.

## Run it

```python
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.nth_from_end import nth_from_end
chain = LinkedList()
for item in (1, 2, 3, 4):
    chain.append(item)
print(nth_from_end(chain, 2).data)
# prints: 3
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
