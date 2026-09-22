"""Merge two ascending linked lists by relinking the existing nodes.

No third chain of values is allocated. Each step takes the smaller head and
appends it to the merged tail, which is the standard linear merge. It replaces
the older span-splicing version: same O(n + m) bound, with one obvious loop
instead of nested "run of nodes still smaller than the other side" bookkeeping.

Ties prefer the first list, matching a stable merge.

Both inputs are emptied, because their nodes now belong to the result. Merging
a list with itself is rejected; that would build a cycle.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def merge_sorted(first: LinkedList[T], second: LinkedList[T]) -> LinkedList[T]:
    """Return a new list that owns the nodes of ``first`` and ``second``.

    ``first`` and ``second`` are left empty.
    """

    merged: LinkedList[T] = LinkedList()
    merged.head = _detach_merged(first, second)
    merged.refresh()
    return merged


def merge_sorted_into(destination: LinkedList[T], source: LinkedList[T]) -> None:
    """Splice ``source`` into ``destination``. ``source`` is left empty."""

    if destination is source:
        raise ValueError("Cannot merge a list with itself.")
    destination.require_linear()
    source.require_linear()
    destination.head = _merge_nodes(destination.head, source.head)
    # Clear the source before refreshing it. Otherwise refresh would walk the
    # merged chain and the source would still look like it owns those nodes.
    source.head = None
    source.refresh()
    destination.refresh()


def _detach_merged(first: LinkedList[T], second: LinkedList[T]) -> Node[T] | None:
    """Merge ``first`` and ``second`` and detach both lists from the result."""

    if first is second:
        raise ValueError("Cannot merge a list with itself.")
    first.require_linear()
    second.require_linear()
    merged_head = _merge_nodes(first.head, second.head)
    first.head = None
    second.head = None
    first.refresh()
    second.refresh()
    return merged_head


def _merge_nodes(first: Node[T] | None, second: Node[T] | None) -> Node[T] | None:
    """Relink two ascending chains into one and return its head."""

    head: Node[T] | None = None
    tail: Node[T] | None = None
    while first is not None and second is not None:
        # Strict ``<`` keeps an equal value from the first list in front.
        if second.data < first.data:
            chosen = second
            second = second.next
        else:
            chosen = first
            first = first.next
        if tail is None:
            head = chosen
        else:
            tail.next = chosen
        tail = chosen

    # The leftover chain is already sorted, so one assignment attaches all of it.
    remainder = first if first is not None else second
    if tail is None:
        return remainder
    tail.next = remainder
    return head
