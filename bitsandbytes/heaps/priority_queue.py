"""Binary min-heap priority queue with decrease-key.

Items are ``(priority, token)`` pairs. ``token`` is a unique integer used by
``decrease_key`` to find the heap slot in O(1) through an index map.

Worked trace (push (5,a), push (3,b), pop):

* Heap ``[(3,b), (5,a)]`` after sift-up on ``b``.
* ``pop`` removes ``b``, moves ``(5,a)`` to the root, sifts down.
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """Min-priority queue backed by ``heapq`` with an index map."""

    def __init__(self) -> None:
        """Create an empty queue.

        Cost
        ----
        O(1) time and memory.
        """

        self._heap: list[tuple[int, int, T]] = []
        self._index: dict[int, int] = {}
        self._next_token = 0

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        O(1).
        """

        return len(self._heap)

    def push(self, priority: int, item: T) -> int:
        """Insert ``item`` with ``priority``. Return a token for ``decrease_key``.

        Cost
        ----
        Append and sift-up: O(log n) for n items. Index map update is O(1).
        """

        token = self._next_token
        self._next_token += 1
        self._heap.append((priority, token, item))
        self._index[token] = len(self._heap) - 1
        self._sift_up(len(self._heap) - 1)
        return token

    def pop(self) -> tuple[int, T]:
        """Remove and return the smallest ``(priority, item)`` pair.

        Cost
        ----
        Swap root with last, shrink, sift-down: O(log n).
        """

        if not self._heap:
            raise IndexError("pop from empty priority queue")
        root = self._heap[0]
        self._swap(0, len(self._heap) - 1)
        self._heap.pop()
        del self._index[root[1]]
        if self._heap:
            self._sift_down(0)
        return root[0], root[2]

    def peek(self) -> tuple[int, T]:
        """Return the smallest pair without removing it.

        Cost
        ----
        O(1).
        """

        if not self._heap:
            raise IndexError("peek from empty priority queue")
        priority, _token, item = self._heap[0]
        return priority, item

    def decrease_key(self, token: int, new_priority: int) -> None:
        """Lower the priority of the item identified by ``token``.

        Cost
        ----
        Index lookup is O(1). One sift-up is O(log n). A linear scan would
        be O(n) and would not earn the heap Dijkstra bound.
        """

        index = self._index[token]
        old_priority, _, item = self._heap[index]
        if new_priority > old_priority:
            raise ValueError("decrease_key requires a strictly smaller priority")
        if new_priority == old_priority:
            return
        self._heap[index] = (new_priority, token, item)
        self._sift_up(index)

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._heap[parent] <= self._heap[index]:
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index: int) -> None:
        size = len(self._heap)
        while True:
            left = 2 * index + 1
            right = left + 1
            smallest = index
            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == index:
                return
            self._swap(index, smallest)
            index = smallest

    def _swap(self, first: int, second: int) -> None:
        self._heap[first], self._heap[second] = self._heap[second], self._heap[first]
        self._index[self._heap[first][1]] = first
        self._index[self._heap[second][1]] = second
