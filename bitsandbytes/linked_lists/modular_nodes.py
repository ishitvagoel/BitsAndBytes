"""Find the last node whose position is a multiple of ``k``.

Positions are 1-based. From the start, the scan remembers every hit and
returns the last one, which is the greatest qualifying index.

From the end, position 1 is the tail. The same "last hit wins" rule returns
the greatest qualifying position, which is the match farthest from the tail.
With ``n`` nodes that position is ``k * (n // k)``, and the node is at
0-based index ``n % k`` from the head. Fewer than ``k`` nodes means there is
no match.

The original end-of-list function was ``pass``.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

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
    The nodes are collected once: O(n) time and O(n) extra memory for the
    list. The index ``n % k`` is then arithmetic: O(1). Total time O(n),
    extra memory O(n). A two-pointer gap of ``n % k`` would avoid the list
    and use O(1) extra memory; the index form makes the formula obvious.
    """

    _require_positive(k)
    nodes = list(lst.iter_nodes())
    length = len(nodes)
    if length < k:
        return None
    position_from_end = k * (length // k)
    # ``length % k`` is 0 when ``length`` itself is a multiple of ``k``,
    # which correctly selects the head: its distance from the tail is ``n``.
    return position_from_end, nodes[length % k]


def _require_positive(k: int) -> None:
    """Reject a non-positive or non-integer ``k``.

    Cost
    ----
    A constant number of checks: O(1) time, O(1) extra memory.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer.")
