"""Reverse a linear linked list, iteratively and recursively."""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def reverse_iterative(lst: LinkedList[T]) -> None:
    """Reverse ``lst`` with three pointers and no call stack.

    ``previous`` is the reversed prefix, ``current`` is the node being
    flipped, and ``upcoming`` is saved before ``current.next`` is overwritten.

    Cost
    ----
    Let n be the length. The loop body runs once per node: n iterations.
    Each iteration reads and writes a constant number of pointers. Time is
    n * O(1) = O(n). Three references are stored: O(1) extra memory for the
    reversal loop. ``require_linear`` adds an O(n) peak from the ``seen`` set
    inside ``refresh`` while that guard runs. ``refresh`` after the loop is
    another O(n) walk with the same peak shape.

    Peak extra memory is O(n) while ``require_linear`` runs its ``seen`` set.
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

    Cost
    ----
    ``_reverse`` is called once per node, so there are n calls. Each call
    does O(1) pointer work on the way back. Time is O(n). The calls are
    nested n deep before any of them returns, so the call stack is O(n)
    extra memory. ``require_linear`` adds an O(n) peak from the ``seen`` set
    while that guard runs.
    """

    lst.require_linear()

    def _reverse(node: Node[T]) -> Node[T]:
        """Reverse the chain at ``node`` and return ``node`` after it is linked.

        Cost
        ----
        One call per node in the suffix. The work outside the recursive call
        is O(1). Summed over n nodes the time is O(n), and the deepest stack
        holds n frames: O(n) extra memory.
        """

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
