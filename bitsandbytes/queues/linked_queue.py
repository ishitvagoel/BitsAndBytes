"""FIFO queue backed by a doubly linked list.

``enqueue`` calls ``append`` on the cached tail, which is O(1).
``dequeue`` calls ``remove_node`` on the head. That unlink follows
``prev`` and ``next`` already stored on the node, so it is O(1). The
head's ``prev`` is ``None``; dropping the head does not search for a
predecessor.

Industry
--------
A working engineer implements a queue with ``collections.deque``. The Python
tutorial says a ``list`` is a poor queue, because an insert or pop at the
beginning shifts every other element, and that ``collections.deque`` has
fast appends and pops at both ends. The deque documentation states
approximately the same O(1) performance in either direction, which is why
``list.pop(0)`` is the operation to avoid.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from bitsandbytes.doubly_linked_list import DoublyLinkedList

T = TypeVar("T")


class LinkedQueue(Generic[T]):
    """First-in-first-out queue with O(1) enqueue and dequeue."""

    def __init__(self) -> None:
        """Create an empty queue.

        Cost
        ----
        One empty doubly linked list: O(1) time and O(1) extra memory.
        """

        self._items: DoublyLinkedList[T] = DoublyLinkedList()

    def __len__(self) -> int:
        """Return how many items are waiting.

        Cost
        ----
        The list caches its length: O(1).
        """

        return len(self._items)

    @property
    def is_empty(self) -> bool:
        """Return whether ``dequeue`` would fail.

        Cost
        ----
        Compare cached length with zero: O(1).
        """

        return len(self._items) == 0

    def enqueue(self, item: T) -> None:
        """Add ``item`` at the back of the queue.

        Cost
        ----
        ``append`` uses the cached tail: O(1) time, one new node.
        """

        self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item.

        Cost
        ----
        ``remove_node`` on the head unlinks through ``head.next`` and
        ``head.prev``: O(1) time, O(1) extra memory.
        """

        head = self._items.head
        if head is None:
            raise IndexError("dequeue from empty queue")
        return self._items.remove_node(head)

    def peek(self) -> T:
        """Return the front item without removing it.

        Cost
        ----
        Read ``head.data``: O(1).
        """

        head = self._items.head
        if head is None:
            raise IndexError("peek from empty queue")
        return head.data
