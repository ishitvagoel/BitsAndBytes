---
title: Special linked-list cases
slug: linked-list-special-cases
order: 25
status: present
module: bitsandbytes.linked_lists.duplicates, bitsandbytes.linked_lists.delete_node, bitsandbytes.linked_lists.add_numbers, bitsandbytes.linked_lists.split_circular, bitsandbytes.linked_lists.reviewers
---

## Make the input contract explicit

Some linked-list exercises depend on assumptions that are easy to miss: values may be sorted, digits may be stored least-significant first, a circular list may have a distinguished head, or the function may be given only a node rather than the list head.

**By the end of this overview, you can** identify the precondition that makes a specialized operation valid and name a boundary test that could reveal a wrong assumption.

## Examples of hidden contracts

Removing adjacent duplicates in a sorted list needs only a forward comparison; the sorted-order precondition is what makes that sufficient. Removing duplicates from an unsorted list needs remembered values or another pass, which changes the time/space tradeoff.

Deleting a node without its list head can copy the successor's value and bypass that successor, but this cannot remove the tail because there is no successor to copy. Adding numbers stored least-significant digit first can process both lists from their heads while carrying at most one extra digit. Splitting a circular list must restore two valid cycles and handle odd and even node counts.

For every specialized operation, list the input shape it assumes, the output shape it promises, and whether it mutates existing nodes. Then test empty input, one node, the last node, duplicates, and the smallest valid cycle or digit list.

## Practice and next step

Explain why a constant-time node-deletion trick cannot work on a tail node when the function receives no list head. Then draw how a five-node circular list should split into two cycles. Compare with [the repository special-case tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list_algorithms.py).

Return to the [linked-list algorithm overview](./list-algorithms.md) for the full implementation inventory.
