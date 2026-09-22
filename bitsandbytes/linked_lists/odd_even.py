"""Group odd positions in front of even positions.

Positions are 1-based, so the first node stays first. ``[1, 2, 3, 4, 5]``
becomes ``[1, 3, 5, 2, 4]``. This is about *positions*, not about whether the
stored numbers are odd.

Keep the odd chain and the even chain interleaved and pull the next odd node
forward one pair at a time:

* ``odd.next`` skips the even node and takes the following odd node.
* ``even.next`` then takes the node that now follows that odd node.

The head of the even chain was saved before the walk. When the walk ends, the
odd tail points at that even head and the two chains become one.

Time O(n), extra memory O(1). The values themselves are not reordered inside
an odd or even position.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList

T = TypeVar("T")


def group_by_position_parity(lst: LinkedList[T]) -> None:
    """Move even-positioned nodes behind the odd-positioned ones."""

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return

    odd = lst.head
    even = lst.head.next
    even_head = even
    while even is not None and even.next is not None:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    lst.refresh()
