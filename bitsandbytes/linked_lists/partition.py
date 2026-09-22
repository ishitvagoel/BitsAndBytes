"""Stable partition around a pivot value.

Every node strictly less than ``pivot`` moves in front of every node that is
greater than or equal to it. Relative order inside each group is preserved,
so ``[1, 4, 3, 2, 5, 2]`` around ``3`` becomes ``[1, 2, 2, 4, 3, 5]``.

Build the two groups as separate chains, then hang the greater-or-equal chain
off the tail of the smaller chain. Unlinking each node before appending it
stops the old ``next`` pointer from dragging the rest of the list into the
wrong group.

Comparing with ``<`` only means a type that is ordered the same way as
``sorted`` works here. Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def partition(lst: LinkedList[T], pivot: T) -> None:
    """Rearrange ``lst`` so values ``< pivot`` precede the rest."""

    lst.require_linear()
    smaller_head: Node[T] | None = None
    smaller_tail: Node[T] | None = None
    other_head: Node[T] | None = None
    other_tail: Node[T] | None = None

    current = lst.head
    while current is not None:
        upcoming = current.next
        current.next = None
        if current.data < pivot:
            smaller_head, smaller_tail = _append(smaller_head, smaller_tail, current)
        else:
            other_head, other_tail = _append(other_head, other_tail, current)
        current = upcoming

    if smaller_tail is None:
        lst.head = other_head
    else:
        smaller_tail.next = other_head
        lst.head = smaller_head
    lst.refresh()


def _append(
    head: Node[T] | None,
    tail: Node[T] | None,
    node: Node[T],
) -> tuple[Node[T], Node[T]]:
    if tail is None:
        return node, node
    tail.next = node
    return head if head is not None else node, node
