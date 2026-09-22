"""Sort a linked list with bottom-up merge sort.

Merge sort fits a linked list better than the array sorts. There is no random
access, so quick sort's partition and heap sort's indexing are awkward.
Merging two sorted chains only rewrites ``next`` pointers.

Bottom-up avoids the recursion and the repeated search for a midpoint. Merge
adjacent runs of length 1, then 2, then 4, and so on, until a run covers the
whole list. An anchor node in front of the head gives every pass a stable
place to hang the newly merged run, including a run that becomes the new head.
The anchor's value is never read.

Ties keep the left run's node first, so the sort is stable.

Time O(n log n). Extra memory O(1) besides the input nodes.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def sort_list(lst: LinkedList[T]) -> None:
    """Sort ``lst`` in ascending order in place."""

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return

    length = len(lst)
    anchor: Node[T] = Node(lst.head.data, lst.head)
    run = 1
    while run < length:
        previous = anchor
        while previous.next is not None:
            left, rest = _cut(previous.next, run)
            right, rest = _cut(rest, run)
            merged_head, merged_tail = _merge_runs(left, right)
            previous.next = merged_head
            merged_tail.next = rest
            previous = merged_tail
        run *= 2

    lst.head = anchor.next
    lst.refresh()


def _cut(start: Node[T] | None, count: int) -> tuple[Node[T] | None, Node[T] | None]:
    """Detach a run of at most ``count`` nodes.

    Returns ``(run, rest)``. The run's tail no longer points at ``rest``.
    """

    if start is None:
        return None, None
    tail = start
    taken = 1
    while taken < count and tail.next is not None:
        tail = tail.next
        taken += 1
    rest = tail.next
    tail.next = None
    return start, rest


def _merge_runs(
    left: Node[T] | None,
    right: Node[T] | None,
) -> tuple[Node[T], Node[T]]:
    """Merge two sorted runs and return the head and tail of the result."""

    if left is None:
        assert right is not None
        return _span(right)
    if right is None:
        return _span(left)

    head: Node[T] | None = None
    tail: Node[T] | None = None
    while left is not None and right is not None:
        # Take from the right only when it is strictly smaller, so equal keys
        # stay in their original relative order.
        if right.data < left.data:
            chosen = right
            right = right.next
        else:
            chosen = left
            left = left.next
        if tail is None:
            head = chosen
        else:
            tail.next = chosen
        tail = chosen

    assert tail is not None and head is not None
    tail.next = left if left is not None else right
    while tail.next is not None:
        tail = tail.next
    return head, tail


def _span(node: Node[T]) -> tuple[Node[T], Node[T]]:
    tail = node
    while tail.next is not None:
        tail = tail.next
    return node, tail
