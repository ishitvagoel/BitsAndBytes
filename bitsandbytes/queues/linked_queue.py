"""FIFO queue backed by a doubly linked list.

``append`` at the tail and ``remove_node`` on the head are both O(1) because
each node stores ``prev``. A singly linked queue would make dequeue O(n) when
finding the predecessor of the head.
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
