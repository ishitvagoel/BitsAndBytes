"""Find the node where a cycle begins, using Floyd's algorithm.

A slow pointer moves one step and a fast pointer moves two. On an acyclic
list the fast pointer falls off the end. On a cyclic list it laps the slow
pointer inside the cycle.

They meet ``mu`` steps before the entrance, modulo the cycle length, where
``mu`` is the distance from the head to the entrance. Walking one step at a
time from the head and from the meeting point therefore lands both pointers
on the entrance after ``mu`` steps.

The old method crashed on an empty list (``None.next``) and returned a
sentence. This returns ``(1-based index, node)`` or ``None``.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def find_cycle_start(lst: LinkedList[T]) -> tuple[int, Node[T]] | None:
    """Return where a cycle begins, or ``None`` when the list is acyclic.

    The index is 1-based, counting from the head along ``next`` links.
    """

    if lst.head is None:
        return None

    meeting = _meeting_point(lst.head)
    if meeting is None:
        return None

    # One pointer restarts at the head. The first node they share is the
    # entrance of the cycle.
    from_head = lst.head
    position = 1
    while from_head is not meeting:
        assert from_head.next is not None and meeting.next is not None
        from_head = from_head.next
        meeting = meeting.next
        position += 1
    return position, from_head


def _meeting_point(head: Node[T]) -> Node[T] | None:
    """Return a node inside the cycle, or ``None`` if there is no cycle."""

    slow: Node[T] | None = head
    fast: Node[T] | None = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return slow
    return None
