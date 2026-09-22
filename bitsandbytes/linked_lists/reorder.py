"""Reorder a list as L0 → Ln → L1 → Ln-1 → L2 → ...

``[1, 2, 3, 4, 5]`` becomes ``[1, 5, 2, 4, 3]``. The shape is "fold the list
in half and zip the second half, reversed, into the first".

Three ideas already used elsewhere, in order:

1. ``end_of_first_half`` finds where the left half stops (slow/fast pointers).
2. The right half is reversed, the same walk as an ordinary list reversal.
3. The two halves are zipped. Each step takes one node from the reversed
   right half and inserts it after the current left node.

Cutting ``end.next`` before the zip stops the left half from still pointing
into the right half. The right half is never longer than the left, so the
zip ends when the right half is used up. The middle node of an odd-length
list stays at the end.

Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node
from bitsandbytes.linked_lists.middle import end_of_first_half

T = TypeVar("T")


def reorder(lst: LinkedList[T]) -> None:
    """Fold ``lst`` so nodes from the ends alternate toward the middle.

    Cost
    ----
    Finding the end of the first half is O(n). Reversing the right half
    visits at most n / 2 nodes: O(n). The zip then takes one node from each
    half per step, again O(n) pointer writes. ``refresh`` is O(n). The sum
    of a constant number of O(n) passes is still O(n) time. Extra memory is
    a handful of references: O(1).

    Peak extra memory is O(n) while ``require_linear`` runs its ``seen`` set.
    """

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return

    split = end_of_first_half(lst.head)
    second = _reverse(split.next)
    split.next = None

    first: Node[T] | None = lst.head
    while second is not None and first is not None:
        first_next = first.next
        second_next = second.next
        first.next = second
        second.next = first_next
        first = first_next
        second = second_next
    lst.refresh()


def _reverse(head: Node[T] | None) -> Node[T] | None:
    """Reverse the chain that starts at ``head`` and return its new head.

    Cost
    ----
    Let k be the number of nodes in this chain. The loop runs k times and
    each iteration rewrites one ``next``: O(k) time, O(1) extra memory.
    """

    previous: Node[T] | None = None
    current = head
    while current is not None:
        upcoming = current.next
        current.next = previous
        previous = current
        current = upcoming
    return previous
