"""Delete a node when the caller has that node and not the list head.

Unlinking a singly linked node normally requires its predecessor, because the
predecessor's ``next`` is what skips it. Given only the node itself, copy the
successor's value into this node and unlink the successor. The caller's
pointer still refers to the same object, but that object now holds the
successor's value and the successor is gone. To every walk that starts at the
head, the original value has disappeared.

This cannot delete the tail: there is no successor to copy. The tail has to
be removed from the head, where the predecessor is known.

If the node belongs to a :class:`~bitsandbytes.linked_list.LinkedList`, call
``refresh`` afterwards. The cached tail and length still describe the chain
from before the copy.

Time O(1), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import Node

T = TypeVar("T")


def delete_without_predecessor(node: Node[T]) -> None:
    """Erase ``node`` by sliding the successor's value and link into it."""

    successor = node.next
    if successor is None:
        raise ValueError("Cannot delete the tail without its predecessor.")
    node.data = successor.data
    node.next = successor.next
    successor.next = None
