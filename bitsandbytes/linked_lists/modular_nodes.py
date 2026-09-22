"""Find the last node whose position is a multiple of ``k``.

Positions are 1-based. From the start, the scan remembers every hit and
returns the last one, which is the greatest qualifying index.

From the end, position 1 is the tail. The same "last hit wins" rule returns
the greatest qualifying position, which is the match farthest from the tail.
With ``n`` nodes that position is ``k * (n // k)``. The node is the one that
many steps from the tail along ``next`` links, which is the same node as
``nth_from_end`` with that distance. Fewer than ``k`` nodes means there is
no match.

The original end-of-list function was ``pass``.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node
from bitsandbytes.linked_lists.nth_from_end import nth_from_end

T = TypeVar("T")


def modular_node_from_start(
    lst: LinkedList[T],
    k: int,
) -> tuple[int, Node[T]] | None:
    """Return ``(position, node)`` for the last start-position divisible by ``k``.

    Cost
    ----
    ``iter_nodes`` yields each of the n nodes once, and the loop body is one
    modulo and maybe one assignment: O(1). Time O(n). One tuple is kept:
    O(1) extra memory beyond the iterator's ``seen`` set, which is O(n).
    """

    _require_positive(k)
    found: tuple[int, Node[T]] | None = None
    for position, node in enumerate(lst.iter_nodes(), start=1):
        if position % k == 0:
            found = (position, node)
    return found


def modular_node_from_end(
    lst: LinkedList[T],
    k: int,
) -> tuple[int, Node[T]] | None:
    """Return ``(position from the end, node)`` for the last such match.

    Cost
    ----
    ``require_linear`` is O(n) time with peak O(n) extra memory for its
    ``seen`` set. ``nth_from_end`` walks two pointers with a fixed gap:
    O(n) time and O(1) extra memory besides that peak. Total time O(n),
    peak extra memory O(n) from the guard only.

    Peak extra memory is O(n) while ``require_linear`` runs its ``seen`` set.
    """

    _require_positive(k)
    lst.require_linear()
    length = len(lst)
    if length < k:
        return None
    position_from_end = k * (length // k)
    return position_from_end, nth_from_end(lst, position_from_end)


def _require_positive(k: int) -> None:
    """Reject a non-positive or non-integer ``k``.

    Cost
    ----
    A constant number of checks: O(1) time, O(1) extra memory.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer.")
