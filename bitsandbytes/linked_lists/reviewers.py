"""Circular list that hands reviews out in turn.

A newly added reviewer is linked in immediately after the current one, so
they are assigned next. The cursor stays put until ``next_reviewer`` moves it.
With one reviewer the circle points at itself, and the next assignment is
that same person.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(eq=False, slots=True, repr=False)
class Reviewer:
    """One person in the review rotation."""

    name: str
    next: Reviewer | None = None

    def __repr__(self) -> str:
        # Omit ``next`` so a circle does not recurse forever.
        return f"Reviewer({self.name!r})"


class ReviewersList:
    """Round-robin reviewers stored as a circular singly linked list."""

    def __init__(self) -> None:
        self._head: Reviewer | None = None
        self._current: Reviewer | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Reviewer]:
        """Yield each reviewer once, starting from the first person added."""

        node = self._head
        for _ in range(self._size):
            assert node is not None and node.next is not None
            yield node
            node = node.next

    @property
    def current(self) -> Reviewer:
        if self._current is None:
            raise RuntimeError("No reviewers have been added.")
        return self._current

    @property
    def current_name(self) -> str:
        """Name of the reviewer who currently holds the cursor."""

        return self.current.name

    def add_reviewer(self, name: str) -> Reviewer:
        """Insert ``name`` just after the cursor and return the new node.

        The cursor does not move. On an empty list the new reviewer becomes
        the cursor and points at themselves.
        """

        reviewer = Reviewer(name)
        if self._current is None:
            reviewer.next = reviewer
            self._head = reviewer
            self._current = reviewer
        else:
            reviewer.next = self._current.next
            self._current.next = reviewer
        self._size += 1
        return reviewer

    def next_reviewer(self) -> Reviewer:
        """Advance the cursor one step and return that reviewer."""

        current = self.current
        assert current.next is not None
        self._current = current.next
        return self._current
