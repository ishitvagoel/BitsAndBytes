"""Deque on a doubly linked list.

Both ends are O(1) because ``DoublyLinkedList`` caches ``head`` and ``tail``
and each node stores ``prev``. Inserting in the middle still requires finding
the position, which is O(n).

Worked trace (``append_right`` 1, ``append_left`` 0, ``pop_left``):

* After ``1``: ``[1]``.
* ``append_left(0)``: ``[0, 1]``.
* ``pop_left`` returns ``0``, deque ``[1]``.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from bitsandbytes.doubly_linked_list import DoublyLinkedList, DoublyNode

T = TypeVar("T")


class LinkedDeque(Generic[T]):
    """Double-ended queue with O(1) operations at both ends."""

    def __init__(self) -> None:
        """Create an empty deque.

        Cost
        ----
        One empty doubly linked list: O(1).
        """

        self._items: DoublyLinkedList[T] = DoublyLinkedList()

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        Cached size: O(1).
        """

        return len(self._items)

    def append_left(self, item: T) -> None:
        """Insert ``item`` at the front.

        Cost
        ----
        ``prepend`` is O(1).
        """

        self._items.prepend(item)

    def append_right(self, item: T) -> None:
        """Insert ``item`` at the back.

        Cost
        ----
        ``append`` is O(1).
        """

        self._items.append(item)

    def pop_left(self) -> T:
        """Remove and return the front item.

        Cost
        ----
        ``remove_node`` on the head: O(1).
        """

        head = self._items.head
        if head is None:
            raise IndexError("pop from empty deque")
        return self._items.remove_node(head)

    def pop_right(self) -> T:
        """Remove and return the back item.

        Cost
        ----
        ``pop_tail`` is O(1).
        """

        return self._items.pop_tail()

    def __iter__(self):
        """Yield items from front to back.

        Cost
        ----
        O(n) time, O(1) extra memory.
        """

        yield from self._items

    def insert_at(self, index: int, item: T) -> None:
        """Insert ``item`` before the item currently at ``index``.

        Cost
        ----
        Finding the node at ``index`` walks up to n steps: O(n) time. The
        splice after that is O(1).
        """

        if index < 0 or index > len(self._items):
            raise IndexError("deque index out of range")
        if index == 0:
            self.append_left(item)
            return
        if index == len(self._items):
            self.append_right(item)
            return
        node = self._node_at(index)
        if node.prev is None:
            self.append_left(item)
        else:
            self._items.insert_after(node.prev, item)

    def _node_at(self, index: int) -> DoublyNode[T]:
        """Return the node at ``index`` by walking from the nearer end.

        Cost
        ----
        At most n/2 steps: O(n) time, O(1) extra memory.
        """

        size = len(self._items)
        if index < 0 or index >= size:
            raise IndexError("deque index out of range")
        if index <= size // 2:
            current = self._items.head
            for _ in range(index):
                assert current is not None and current.next is not None
                current = current.next
            assert current is not None
            return current
        current = self._items.tail
        for _ in range(size - 1 - index):
            assert current is not None and current.prev is not None
            current = current.prev
        assert current is not None
        return current
