"""Rotate a list by moving a suffix to the front.

A right rotation by ``k`` makes the last ``k`` nodes the new prefix.
``[1, 2, 3, 4, 5]`` rotated right by 2 is ``[4, 5, 1, 2, 3]``.

``k`` can be larger than the length, and it can be negative. Python's
remainder already normalises both: ``k % n`` is the equivalent non-negative
right rotation, and a negative ``k`` becomes a right rotation of
``n - (abs(k) % n)``, which is a left rotation.

The list is joined into a circle for one assignment, the new tail is the
node just before the new head, and that link is cut. No node is allocated.

Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList

T = TypeVar("T")


def rotate_right(lst: LinkedList[T], k: int) -> None:
    """Rotate ``lst`` to the right by ``k`` places.

    Cost
    ----
    ``require_linear`` is O(n). ``k % n`` is O(1). ``node_at`` walks to index
    ``n - (k % n) - 1``, which is at most n steps: O(n). Closing and cutting
    the circle is O(1), and ``refresh`` is another O(n). Total time O(n).
    No new node is allocated for the values: O(1) extra memory.
    """

    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError("k must be an integer.")
    lst.require_linear()
    if lst.head is None or lst.head.next is None or k == 0:
        return

    length = len(lst)
    k %= length
    if k == 0:
        return

    # Index of the new tail: everything after it moves in front.
    new_tail = lst.node_at(length - k - 1)
    new_head = new_tail.next
    assert lst.tail is not None and new_head is not None
    lst.tail.next = lst.head
    new_tail.next = None
    lst.head = new_head
    lst.refresh()
