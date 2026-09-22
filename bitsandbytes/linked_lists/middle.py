"""Find a midpoint with two pointers that move at different speeds.

A linked list has no index, so "the middle" is not ``length // 2`` unless you
are willing to walk the list twice. One walk is enough if a second pointer
moves twice as fast: when the fast pointer reaches the end, the slow pointer
has covered half the nodes.

Two conventions matter, and mixing them up breaks later algorithms:

* ``middle_node`` stops when the fast pointer can no longer take a full
  two-step jump that starts on a real node. On an even-length list this is the
  second of the two middle nodes. ``[1, 2, 3, 4]`` yields ``3``.
* ``end_of_first_half`` stops one step sooner, when the fast pointer's *next*
  node has no successor. On an even-length list this is the last node of the
  left half. ``[1, 2, 3, 4]`` yields ``2``. Palindrome checking and reordering
  split the list here, then reverse everything after that node.

On an odd-length list both conventions land on the single middle node.

Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def middle_node(lst: LinkedList[T]) -> Node[T] | None:
    """Return the middle node, or the second middle when the length is even."""

    lst.require_linear()
    slow = lst.head
    fast = lst.head
    while fast is not None and fast.next is not None:
        assert slow is not None and slow.next is not None
        slow = slow.next
        fast = fast.next.next
    return slow


def end_of_first_half(head: Node[T]) -> Node[T]:
    """Return the last node of the left half.

    Odd length: the middle node. Even length: the left of the two middles.
    ``head`` must be the first node of a non-empty linear list.
    """

    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        assert slow.next is not None
        slow = slow.next
        fast = fast.next.next
    return slow
