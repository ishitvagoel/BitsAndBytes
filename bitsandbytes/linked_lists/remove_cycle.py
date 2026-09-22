"""Break a cycle once Floyd's algorithm has found where it begins.

``find_cycle_start`` returns the entrance. The node that points back at that
entrance is the last node of the cycle. Clearing its ``next`` opens the list
into a line that still contains every node exactly once.

``1 → 2 → 3 → 4 → 5 → 3`` becomes ``1 → 2 → 3 → 4 → 5``. A node that points
at itself becomes a one-node list. A list that is already linear is left
alone and the function returns ``False``.

Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.cycle import find_cycle_start

T = TypeVar("T")


def remove_cycle(lst: LinkedList[T]) -> bool:
    """Open a cycle if there is one. Return whether a cycle was removed."""

    found = find_cycle_start(lst)
    if found is None:
        return False
    _position, entrance = found
    cursor = entrance
    while cursor.next is not entrance:
        assert cursor.next is not None
        cursor = cursor.next
    cursor.next = None
    lst.refresh()
    return True
