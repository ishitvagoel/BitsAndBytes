---
title: Linked-list reversal and relinking
slug: linked-list-reversal-and-relinking
order: 23
status: present
module: bitsandbytes.linked_lists.reverse, bitsandbytes.linked_lists.reverse_in_pairs, bitsandbytes.linked_lists.reverse_in_blocks, bitsandbytes.linked_lists.rotate, bitsandbytes.linked_lists.partition, bitsandbytes.linked_lists.odd_even, bitsandbytes.linked_lists.reorder
---

## Change links without losing the rest of the chain

These problems rearrange existing nodes by changing their `next` references. Before replacing a link, save the node that follows it; otherwise the unvisited suffix can become unreachable.

**By the end of this overview, you can** explain the three-pointer reversal invariant and identify the extra boundary work needed for pair, block, rotation, partition, odd/even, and reorder operations.

## The reversal invariant

Keep `previous` as the reversed prefix, `current` as the next node to process, and `following` as the untouched suffix. Save `current.next`, point `current.next` to `previous`, then advance both moving pointers. At each iteration, no node is lost: the prefix is reversed and the suffix remains connected. When `current` is empty, `previous` is the new head.

For a list with `n` nodes, this loop visits each node once: O(n) time and O(1) extra pointer space. A recursive version can use O(n) call-stack space even though it rewrites the same links.

Pair and block reversal reuse the invariant but must reconnect the previous block to the new head of the current block and connect its tail to the untouched suffix. Rotation first identifies a new tail and makes the chain temporarily circular, then cuts it at the chosen position. Partition and odd/even grouping preserve separate tails before joining the chains.

## Check the boundaries

Trace an empty list, a one-node list, a two-node list, and a block size larger than the list. For each pointer write, state which node owns the remaining suffix. Check that a linear input remains linear and that every original node appears exactly once after the operation.

## Practice and next step

Draw the list `A → B → C → D` and reverse it by hand, writing `previous`, `current`, and `following` before each update. Then explain why saving `following` after overwriting `current.next` cannot work. Compare with [the repository implementations and tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list_algorithms.py).

Continue to [linked-list merge and sort](./linked-list-merge-and-sort.md) for operations that combine two ordered chains.
