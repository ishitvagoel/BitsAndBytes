"""Stack whose minimum is readable in constant time.

A plain stack can report its minimum only by scanning every item, which is
O(n). A second unbounded ``Stack`` stores the minima. It receives a value only when that value is less than or
equal to the current minimum, so its top is always the minimum of the main
stack. ``push``, ``pop``, and ``minimum`` each touch a constant number of
stack tops.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, TypeVar

from bitsandbytes.stacks.stack import Stack, StackEmptyError

T = TypeVar("T")


class MinStack(Generic[T]):
    """LIFO stack with an O(1) ``minimum``.

    Values are compared with ``<=``. Equal minima are stored again on the
    minima stack so popping one copy leaves the earlier minimum in place.
    ``T`` must support ``<=`` for minimum tracking.
    """

    def __init__(self) -> None:
        """Create an empty min-stack.

        Cost
        ----
        Two empty stacks are allocated: O(1) time and O(1) extra memory.
        """

        self._items: Stack[T] = Stack(limit=None)
        self._minima: Stack[T] = Stack(limit=None)

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        The stack stores its length: O(1).
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

        return f"MinStack({list(self)!r})"

    def push(self, value: T) -> None:
        """Push ``value`` and update the recorded minimum.

        Cost
        ----
        One ``Stack.push`` on the main stack is amortized O(1). The
        minima stack receives at most one push when ``value`` is less than or
        equal to the current minimum: also amortized O(1). Extra memory grows
        by one slot per push on the main stack and, for a non-increasing
        sequence, one slot per push on the minima stack as well.
        """

        self._items.push(value)
        if self._minima.is_empty or value <= self._minima.peek():
            self._minima.push(value)

    def pop(self) -> T:
        """Remove and return the top item, dropping a minimum if it was one.

        Cost
        ----
        Two stack pops in the worst case when the top equals the recorded
        minimum. Each pop is O(1). Extra memory is O(1).
        """

        if self._items.is_empty:
            raise StackEmptyError("Stack is empty.")
        value = self._items.pop()
        if value == self._minima.peek():
            self._minima.pop()
        return value

    def peek(self) -> T:
        """Return the top item without removing it.

        Cost
        ----
        One ``peek`` on the main stack: O(1).
        """

        if self._items.is_empty:
            raise StackEmptyError("Stack is empty.")
        return self._items.peek()

    def minimum(self) -> T:
        """Return the smallest value currently stored.

        Cost
        ----
        One ``peek`` on the minima stack: O(1). Does not scan all n items.
        """

        if self._minima.is_empty:
            raise StackEmptyError("Stack is empty.")
        return self._minima.peek()
