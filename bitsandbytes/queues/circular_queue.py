"""Fixed-capacity queue in a circular array.

The head and tail indexes chase each other around one Python list. Enqueue
writes at ``tail`` and advances; dequeue reads at ``head`` and advances. When
``head == tail`` after a dequeue the queue is empty. After an enqueue that
lands ``tail`` on ``head``, the queue is full.

That full-versus-empty ambiguity is why a circular buffer needs either a
count, a sacrificed slot, or a boolean flag. This version keeps an explicit
``size`` counter.
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class CircularQueue(Generic[T]):
    """FIFO queue with fixed capacity backed by a ring buffer."""

    def __init__(self, capacity: int) -> None:
        """Create a queue that holds at most ``capacity`` items.

        Cost
        ----
        Allocate a list of ``capacity`` slots: O(capacity) time and memory.
        """

        if capacity < 1:
            raise ValueError("capacity must be at least 1.")
        self._capacity = capacity
        self._slots: list[T | None] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        The counter is updated on enqueue and dequeue: O(1).
        """

        return self._size

    @property
    def is_full(self) -> bool:
        """Return whether ``enqueue`` would fail.

        Cost
        ----
        Compare ``size`` with ``capacity``: O(1).
        """

        return self._size == self._capacity

    @property
    def is_empty(self) -> bool:
        """Return whether ``dequeue`` would fail.

        Cost
        ----
        Compare ``size`` with zero: O(1).
        """

        return self._size == 0

    def enqueue(self, item: T) -> None:
        """Add ``item`` at the back.

        Cost
        ----
        One write at ``tail`` and index arithmetic modulo ``capacity``: O(1).
        """

        if self.is_full:
            raise IndexError("enqueue on full circular queue")
        self._slots[self._tail] = item
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> T:
        """Remove and return the front item.

        Cost
        ----
        One read at ``head`` and index arithmetic: O(1).
        """

        if self.is_empty:
            raise IndexError("dequeue from empty circular queue")
        item = self._slots[self._head]
        assert item is not None
        self._slots[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item
