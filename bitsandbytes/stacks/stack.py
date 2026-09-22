"""Bounded stack.

``push`` and ``pop`` only move an item. The full and empty checks are
decorators, so the methods stay a single list operation and the guard can be
reused (``peek`` uses the same empty check as ``pop``).

``functools.wraps`` keeps the original method name. Without it the wrapper
replaced every method's ``__name__`` with ``execute``.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Generic, TypeVar

T = TypeVar("T")


class StackFullError(Exception):
    """Raised when ``push`` is called and the stack is already at its limit."""


class StackEmptyError(Exception):
    """Raised when ``pop`` or ``peek`` is called on an empty stack."""


def _reject_if_full(method: Callable) -> Callable:
    """Refuse the call when the stack cannot take another item.

    Cost
    ----
    The wrapper compares ``len(self._items)`` with ``limit``. Both are
    already known, so the check is O(1). It then calls the wrapped method,
    whose own cost is unchanged. Building the wrapper at decoration time is
    O(1) and happens once, not once per push.
    """

    @wraps(method)
    def wrapper(self: Stack, *args, **kwargs):
        """Reject a full stack, otherwise call the wrapped method.

        Cost
        ----
        Comparing the current length with ``limit`` is O(1). The wrapped
        method then runs at its own cost.
        """

        if len(self._items) >= self.limit:
            raise StackFullError(f"Stack is full (limit {self.limit}).")
        return method(self, *args, **kwargs)

    return wrapper


def _reject_if_empty(method: Callable) -> Callable:
    """Refuse the call when there is no top item to read.

    Cost
    ----
    Testing whether the list is empty is O(1). The wrapped ``pop`` or
    ``peek`` then runs at its own cost. Decoration itself is O(1), once.
    """

    @wraps(method)
    def wrapper(self: Stack, *args, **kwargs):
        """Reject an empty stack, otherwise call the wrapped method.

        Cost
        ----
        Testing the list for emptiness is O(1). The wrapped method then
        runs at its own cost.
        """

        if not self._items:
            raise StackEmptyError("Stack is empty.")
        return method(self, *args, **kwargs)

    return wrapper


class Stack(Generic[T]):
    """LIFO stack with a fixed capacity. The default limit is 10."""

    def __init__(self, limit: int = 10) -> None:
        """Create an empty stack that holds at most ``limit`` items.

        Cost
        ----
        Allocating an empty list and storing ``limit`` is O(1) time and O(1)
        extra memory. No items are copied.
        """

        if limit < 0:
            raise ValueError("limit cannot be negative.")
        self.limit = limit
        self._items: list[T] = []

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        CPython stores the list length, so ``len`` is O(1). The items are
        not counted one by one.
        """

        return len(self._items)

    def __repr__(self) -> str:
        """Return the items from bottom to top, plus the limit.

        Cost
        ----
        Formatting n items copies each of them into the string. Time and
        extra memory are O(n).
        """

        return f"Stack({self._items!r}, limit={self.limit})"

    @property
    def is_empty(self) -> bool:
        """Return whether ``pop`` would fail.

        Cost
        ----
        The underlying list knows its length. The test is O(1) time.
        """

        return not self._items

    @property
    def is_full(self) -> bool:
        """Return whether ``push`` would fail.

        Cost
        ----
        Compare the stored length with ``limit``. O(1) time.
        """

        return len(self._items) >= self.limit

    @_reject_if_full
    def push(self, item: T) -> T:
        """Push ``item`` and return it.

        Cost
        ----
        The item is appended at the end of a Python list. Appending at the
        end is amortized O(1): most calls write one slot, and occasionally
        the list allocates a larger array and copies n items. Across n pushes
        those copies sum to O(n), so the average per push is O(1). The
        fullness check in front of this method is also O(1). Worst case of a
        single push that triggers a resize is O(n).
        """

        self._items.append(item)
        return item

    @_reject_if_empty
    def pop(self) -> T:
        """Remove and return the top item.

        Cost
        ----
        ``list.pop()`` with no index removes the last element. No items are
        shifted, so this is O(1) time. The emptiness check is O(1). Extra
        memory is O(1).
        """

        return self._items.pop()

    @_reject_if_empty
    def peek(self) -> T:
        """Return the top item without removing it.

        Cost
        ----
        The top is ``_items[-1]``, a direct index. O(1) time, O(1) extra
        memory. The emptiness check is O(1).
        """

        return self._items[-1]
