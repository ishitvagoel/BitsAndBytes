"""Reverse a linear linked list, iteratively and recursively."""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def reverse_iterative(lst: LinkedList[T]) -> None:
    """Reverse ``lst`` with three pointers and no call stack.

    ``previous`` is the reversed prefix, ``current`` is the node being
    flipped, and ``upcoming`` is saved before ``current.next`` is overwritten.
    """

    lst.require_linear()
    previous: Node[T] | None = None
    current = lst.head
    while current is not None:
        upcoming = current.next
        current.next = previous
        previous = current
        current = upcoming
    lst.head = previous
    lst.refresh()


def reverse_recursive(lst: LinkedList[T]) -> None:
    """Reverse ``lst`` by stitching links on the way back from the tail.

    The deepest call sees the tail and makes it the head. Each caller then
    points that returned node at itself and drops its old forward link.
    """

    lst.require_linear()

    def _reverse(node: Node[T]) -> Node[T]:
        if node.next is None:
            lst.head = node
            return node
        reversed_from_here = _reverse(node.next)
        reversed_from_here.next = node
        node.next = None
        return node

    if lst.head is not None:
        _reverse(lst.head)
    lst.refresh()
