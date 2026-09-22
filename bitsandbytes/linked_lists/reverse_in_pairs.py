"""Swap every two nodes of a linear linked list.

``1 --> 2 --> 3 --> 4 --> 5`` becomes ``2 --> 1 --> 4 --> 3 --> 5``.
A trailing node with no partner stays where it is.

This is the same rearrangement as reversing blocks of 2, written out as a
single pass so the pointer dance is visible without the general k-group loop.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def reverse_in_pairs(lst: LinkedList[T]) -> None:
    """Swap each adjacent pair in ``lst`` in place."""

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return

    # The anchor is not part of the list. It gives the first pair a node to
    # hang from, which removes a special case for the head.
    anchor: Node[T] = Node(lst.head.data, lst.head)
    previous = anchor
    current = lst.head
    while current is not None and current.next is not None:
        partner = current.next
        # Before: previous -> current -> partner -> after
        # After:  previous -> partner -> current -> after
        current.next = partner.next
        partner.next = current
        previous.next = partner
        previous = current
        current = current.next

    lst.head = anchor.next
    lst.refresh()
