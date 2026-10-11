"""Shared typing protocols for ordered keys."""

from typing import Any, Protocol, TypeVar


class SupportsLessThan(Protocol):
    """A value that can be ordered with ``<``."""

    def __lt__(self, other: Any, /) -> bool:
        """Return whether this value is less than ``other``."""


Ordered = TypeVar("Ordered", bound=SupportsLessThan)
