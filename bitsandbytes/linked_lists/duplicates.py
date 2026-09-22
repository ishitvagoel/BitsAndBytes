"""Drop duplicate values from a linked list.

A sorted list only needs to compare each node with its successor. Equal
neighbours are unlinked in place, so the kept node stays and the scan does
not advance until the next value actually changes. That removes a whole run
of duplicates in one visit.

An unsorted list has no neighbour relationship. Remember every value already
kept. A later repeat is unlinked, and the first occurrence stays where it
was, so the surviving order is the order of first appearance. The set needs
hashable values and O(n) extra memory. The sorted pass needs O(1).

Both are O(n) time.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList

T = TypeVar("T")


def remove_sorted_duplicates(lst: LinkedList[T]) -> None:
    """Keep one copy of each run of equal values. ``lst`` must be sorted.

    Cost
    ----
    Let n be the number of nodes. The scan advances once per kept node and
    also once per deleted duplicate, so every node is examined a constant
    number of times. Each examination compares two values and maybe rewrites
    one pointer: O(1). Time is O(n). ``refresh`` walks the survivors, still
    O(n). No auxiliary collection: O(1) extra memory.

    Peak extra memory is O(n) while ``require_linear`` runs its ``seen`` set.
    """

    lst.require_linear()
    current = lst.head
    while current is not None and current.next is not None:
        if current.data == current.next.data:
            # Skip the duplicate and detach it. Stay on ``current`` in case
            # the next node is another copy of the same value.
            duplicate = current.next
            current.next = duplicate.next
            duplicate.next = None
        else:
            current = current.next
    lst.refresh()


def remove_unsorted_duplicates(lst: LinkedList[T]) -> None:
    """Keep the first occurrence of each value. Values must be hashable.

    Cost
    ----
    Each of the n nodes is visited once. Membership in a set is O(1)
    expected, and unlinking is O(1). Time is O(n) expected. The set stores
    one entry per distinct value, at most n, so extra memory is O(n). The
    sorted version avoids that set only because equal values are neighbours.
    Peak extra memory is O(n) while ``require_linear`` runs its ``seen`` set.
    """

    lst.require_linear()
    seen: set[T] = set()
    previous = None
    current = lst.head
    while current is not None:
        if current.data in seen:
            assert previous is not None
            upcoming = current.next
            previous.next = upcoming
            current.next = None
            current = upcoming
        else:
            seen.add(current.data)
            previous = current
            current = current.next
    lst.refresh()
