---
title: Linked-list merge and sort
slug: linked-list-merge-and-sort
order: 24
status: present
module: bitsandbytes.linked_lists.merge_sorted, bitsandbytes.linked_lists.sort_list, bitsandbytes.linked_lists.intersection
---

## The idea

The chains 1, 4 and 2, 3 merge into 1, 2, 3, 4.

When two chains are sorted, compare only their current heads. Take the smaller head, append it to the result, and advance that input. When one input is empty, attach the other suffix. It is already in order. merge_sorted of 1, 4 and 2, 3 returns 1, 2, 3, 4. Ties use a strict less-than against the second list, so an equal key from the first list stays in front. The nodes are relinked, not copied into a second array of values. Both inputs are left empty because their nodes now belong to the result. Merging a list with itself is rejected, because that would build a cycle. Bottom-up merge sort repeats this combine on adjacent runs of width 1, then 2, then 4. A linked list has no random-access middle, so this width schedule fits it better than a top-down split that indexes the midpoint.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Take | taken = 1 | The merge takes 1. The result so far is [1]. |
| Take | taken = 2 | The merge takes 2. The result so far is [1, 2]. |
| Take | taken = 3 | The merge takes 3. The result so far is [1, 2, 3]. |

## Why it is correct

Each step appends the smaller remaining head, so nothing still in either chain is smaller than the item just written. The attached suffix is sorted by the precondition, and it sits after a head that was smaller than its own head. Taking the first list on a tie keeps the earlier equal key in front. The inputs end empty because the same node objects moved. Intersection is a different question. After both chains are linear, equalize the distance to the ends and advance together. Compare node identity, not equal values. The guard that checks the chains has its own cost.

## A common mistake

Concatenating the two chains skips the head comparison and breaks sorted order.

## What it costs

A merge of lengths n and m does a linear number of comparisons and link updates. The result list object is constant extra memory, because the nodes are reused. Bottom-up sort has a logarithmic number of rounds, and each round visits every node, so the time is n log n. Auxiliary node references beyond the list nodes can stay constant. Repeatedly indexing the middle of a linked list would pay a linear walk per index and would lose the array-style access assumption. Count that walk if you choose it. The merge is Θ(n + m) time and O(1) extra memory besides the nodes.

## Run it

```python
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.merge_sorted import merge_sorted
left, right = LinkedList(), LinkedList()
left.append(1); left.append(4); right.append(2); right.append(3)
print(list(merge_sorted(left, right)))
# prints: [1, 2, 3, 4]
```

## Practice and next step

Open Special linked-list cases next. Special cases are the contracts that make a later list routine valid.
