"""Find the first shared node of two acyclic lists.

The lists may differ in length. Walk the extra nodes of the longer list
first, then move both pointers together. The first identical node is the
join. If both pointers fall off, the lists never meet.

Length is counted by following ``next``, not from the cached size. Splicing
``list2`` onto a node of ``list1`` (the usual way to build this example)
does not update that cache.

The old code returned ``.data`` even when both pointers became ``None``,
which raised ``AttributeError`` for lists that do not intersect.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def find_intersection(first: LinkedList[T], second: LinkedList[T]) -> Node[T] | None:
    """Return the first node shared by ``first`` and ``second``, or ``None``."""

    first_length = _length(first.head)
    second_length = _length(second.head)
    first_node = first.head
    second_node = second.head
    if first_length > second_length:
        first_node = _advance(first_node, first_length - second_length)
    elif second_length > first_length:
        second_node = _advance(second_node, second_length - first_length)

    while first_node is not second_node:
        # Both sides are the same remaining length, so they reach None together
        # when there is no shared node.
        if first_node is None or second_node is None:
            return None
        first_node = first_node.next
        second_node = second_node.next
    return first_node


def _length(head: Node[T] | None) -> int:
    count = 0
    seen: set[int] = set()
    node = head
    while node is not None:
        if id(node) in seen:
            raise ValueError("Intersection search expects acyclic lists.")
        seen.add(id(node))
        count += 1
        node = node.next
    return count


def _advance(node: Node[T] | None, steps: int) -> Node[T] | None:
    for _ in range(steps):
        if node is None:
            return None
        node = node.next
    return node
