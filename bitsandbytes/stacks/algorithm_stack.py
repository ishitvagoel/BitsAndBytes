"""Unbounded LIFO stack for algorithm lessons.

``Stack`` in ``stack.py`` teaches a fixed capacity and decorator guards. The
monotonic-stack scans, min stack, and sort-a-stack lessons only need push,
pop, and peek at the end of a Python list, with no limit check on every call.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from bitsandbytes.stacks.stack import StackEmptyError

T = TypeVar("T")


class AlgorithmStack(Generic[T]):
    """LIFO stack with no fixed capacity."""

    def __init__(self) -> None:
        """Create an empty stack.

        Cost
        ----
        One empty list is allocated: O(1) time and O(1) extra memory.
        """

        self._items: list[T] = []

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        CPython stores the list length: O(1).
        """

        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        """Yield items from bottom to top.

        Cost
        ----
        n yields. O(n) time, O(1) extra memory.
        """

        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        """Return whether ``item`` is stored.

        Cost
        ----
        Scan n items. O(n) time, O(1) extra memory.
        """

        return item in self._items

    def __repr__(self) -> str:
        """Return the items in iteration order.

        Cost
        ----
        Formatting n items is O(n) time and O(n) extra memory.
        """

        return f"AlgorithmStack({list(self)!r})"

    @property
    def is_empty(self) -> bool:
        """Return whether ``pop`` would fail.

        Cost
        ----
        Testing list emptiness is O(1).
        """

        return not self._items

    def push(self, item: T) -> T:
        """Push ``item`` and return it.

        Cost
        ----
        Appending at the end of a Python list is amortized O(1). A single
        resize that copies n items is O(n), but n pushes amortize those
        copies to O(1) each on average.
        """

        self._items.append(item)
        return item

    def pop(self) -> T:
        """Remove and return the top item.

        Cost
        ----
        ``list.pop()`` with no index is O(1) time and O(1) extra memory.
        """

        if not self._items:
            raise StackEmptyError("Stack is empty.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it.

        Cost
        ----
        Index ``-1`` is O(1) time and O(1) extra memory.
        """

        if not self._items:
            raise StackEmptyError("Stack is empty.")
        return self._items[-1]
