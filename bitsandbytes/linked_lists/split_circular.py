"""Split a circular linked list into two linear lists.

The first list receives ``ceil(n / 2)`` nodes, so an odd length leaves the
extra node in front. Both results are linear: the cycle is broken. That
matches the original samples, which print two ordinary chains.

``1 --> 2 --> ... --> 11 --> (back to 1)`` becomes ``1..6`` and ``7..11``.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList

T = TypeVar("T")


def split_circular(source: LinkedList[T]) -> tuple[LinkedList[T], LinkedList[T]]:
    """Break ``source`` into two linear lists and return ``(first, second)``.

    ``source`` itself becomes the first half. The second half is a new list.
    """

    source.refresh()
    if source.head is None or source.tail is None or source.tail.next is not source.head:
        raise ValueError(
            "List must be circular, with the tail pointing back at the head."
        )

    length = len(source)
    first_length = (length + 1) // 2  # ceil(n / 2) without floating point

    # A single node is already the whole first half. Just open the cycle.
    if first_length == length:
        source.tail.next = None
        source.refresh()
        return source, LinkedList()

    cut = source.node_at(first_length - 1)
    second_head = cut.next
    assert second_head is not None
    cut.next = None
    source.tail.next = None

    second: LinkedList[T] = LinkedList()
    second.head = second_head
    source.refresh()
    second.refresh()
    return source, second
