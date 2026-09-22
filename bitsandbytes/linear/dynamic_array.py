"""Dynamic array (stretchy list).

Geometric doubling makes n appends copy O(n) elements in total: the sizes
1, 2, 4, … sum to less than 2n. That aggregate argument is the same one used
inside ``Stack.push``.

Worked trace (three appends starting from capacity 1):

* Append ``a``: length 1, capacity 1, no copy.
* Append ``b``: length 2, capacity doubled to 2, one element copied.
* Append ``c``: length 3, capacity doubled to 4, two elements copied.
"""

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """Append-mostly dynamic array with geometric growth."""

    def __init__(self, *, initial_capacity: int = 1) -> None:
        """Create an empty array with at least ``initial_capacity`` slots.

        Cost
        ----
        Allocate one list: O(initial_capacity) time and memory.
        """

        if initial_capacity < 1:
            raise ValueError("initial_capacity must be at least 1.")
        self._items: list[T | None] = [None] * initial_capacity
        self._length = 0
        self._capacity = initial_capacity

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        O(1).
        """

        return self._length

    def __iter__(self) -> Iterator[T]:
        """Yield stored items from first to last.

        Cost
        ----
        n yields: O(n) time, O(1) extra memory.
        """

        for index in range(self._length):
            value = self._items[index]
            assert value is not None
            yield value

    def append(self, item: T) -> None:
        """Append ``item`` at the end, resizing when full.

        Cost
        ----
        Without a resize, one write: O(1). When capacity doubles, the copy
        moves ``length`` references. Charge each element O(1) amortized across
        the doublings that move it. Extra memory is O(n) for n stored items.
        """

        if self._length == self._capacity:
            self._grow()
        self._items[self._length] = item
        self._length += 1

    def pop(self) -> T:
        """Remove and return the last item.

        Cost
        ----
        O(1) time. This teaching type does not shrink capacity on pop.
        """

        if self._length == 0:
            raise IndexError("pop from empty DynamicArray")
        self._length -= 1
        value = self._items[self._length]
        assert value is not None
        self._items[self._length] = None
        return value

    def __getitem__(self, index: int) -> T:
        """Return the item at ``index``.

        Cost
        ----
        O(1) time for a valid index.
        """

        if index < 0 or index >= self._length:
            raise IndexError("DynamicArray index out of range")
        value = self._items[index]
        assert value is not None
        return value

    def total_copy_cost_for_appends(self, append_count: int) -> int:
        """Return total reference copies if capacity starts at 1 and doubles.

        Used in tests to verify the aggregate O(n) copy bound without waiting
        for billions of appends.

        Cost
        ----
        O(log append_count) arithmetic steps: O(1) extra memory.
        """

        if append_count < 0:
            raise ValueError("append_count cannot be negative.")
        copies = 0
        capacity = 1
        length = 0
        for _ in range(append_count):
            if length == capacity:
                copies += length
                capacity *= 2
            length += 1
        return copies

    def _grow(self) -> None:
        """Double capacity and copy live items.

        Cost
        ----
        O(length) time to copy ``length`` references.
        """

        new_capacity = self._capacity * 2
        new_items: list[T | None] = [None] * new_capacity
        for index in range(self._length):
            new_items[index] = self._items[index]
        self._items = new_items
        self._capacity = new_capacity
