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
        """Return the name without following ``next``.

        Cost
        ----
        Formatting one name is O(1) in the size of the circle. Following
        ``next`` would not terminate.
        """

        return f"Reviewer({self.name!r})"


class ReviewersList:
    """Round-robin reviewers stored as a circular singly linked list."""

    def __init__(self) -> None:
        """Start with no reviewers.

        Cost
        ----
        Three empty references: O(1) time and O(1) extra memory.
        """

        self._head: Reviewer | None = None
        self._current: Reviewer | None = None
        self._size = 0

    def __len__(self) -> int:
        """Return how many reviewers are in the circle.

        Cost
        ----
        The size is cached on insert. O(1) time. The circle is not walked.
        """

        return self._size

    def __iter__(self) -> Iterator[Reviewer]:
        """Yield each reviewer once, starting from the first person added.

        Cost
        ----
        The loop runs ``_size`` times, once per reviewer. n reviewers take
        n steps: O(n) time, O(1) extra memory. The cached size is what stops
        the circle from being walked forever.
        """

        node = self._head
        for _ in range(self._size):
            assert node is not None and node.next is not None
            yield node
            node = node.next

    @property
    def current(self) -> Reviewer:
        """Return the reviewer who holds the cursor.

        Cost
        ----
        One attribute read and maybe one exception. O(1) time.
        """

        if self._current is None:
            raise RuntimeError("No reviewers have been added.")
        return self._current

    @property
    def current_name(self) -> str:
        """Name of the reviewer who currently holds the cursor.

        Cost
        ----
        ``current`` is O(1) and reading ``name`` is O(1). Total O(1).
        """

        return self.current.name

    def add_reviewer(self, name: str) -> Reviewer:
        """Insert ``name`` just after the cursor and return the new node.

        The cursor does not move. On an empty list the new reviewer becomes
        the cursor and points at themselves.

        Cost
        ----
        The new node is linked to ``current.next``, which is already known.
        No scan of the circle: O(1) time. One new node is allocated.
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
        """Advance the cursor one step and return that reviewer.

        Cost
        ----
        Follow one ``next`` pointer. O(1) time, O(1) extra memory, regardless
        of how many reviewers are in the circle.
        """

        current = self.current
        assert current.next is not None
        self._current = current.next
        return self._current
