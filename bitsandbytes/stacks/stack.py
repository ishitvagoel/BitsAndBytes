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
    """Refuse the call when the stack cannot take another item."""

    @wraps(method)
    def wrapper(self: Stack, *args, **kwargs):
        if len(self._items) >= self.limit:
            raise StackFullError(f"Stack is full (limit {self.limit}).")
        return method(self, *args, **kwargs)

    return wrapper


def _reject_if_empty(method: Callable) -> Callable:
    """Refuse the call when there is no top item to read."""

    @wraps(method)
    def wrapper(self: Stack, *args, **kwargs):
        if not self._items:
            raise StackEmptyError("Stack is empty.")
        return method(self, *args, **kwargs)

    return wrapper


class Stack(Generic[T]):
    """LIFO stack with a fixed capacity. The default limit is 10."""

    def __init__(self, limit: int = 10) -> None:
        if limit < 0:
            raise ValueError("limit cannot be negative.")
        self.limit = limit
        self._items: list[T] = []

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r}, limit={self.limit})"

    @property
    def is_empty(self) -> bool:
        return not self._items

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.limit

    @_reject_if_full
    def push(self, item: T) -> T:
        """Push ``item`` and return it."""

        self._items.append(item)
        return item

    @_reject_if_empty
    def pop(self) -> T:
        """Remove and return the top item."""

        return self._items.pop()

    @_reject_if_empty
    def peek(self) -> T:
        """Return the top item without removing it."""

        return self._items[-1]
