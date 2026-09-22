"""Stack whose minimum is readable in constant time.

A plain stack can report its minimum only by scanning every item, which is
O(n). A second stack stores the minima. It receives a value only when that
value is less than or equal to the current minimum, so its top is always the
minimum of the main stack. ``push``, ``pop``, and ``minimum`` each touch a
constant number of ends of a list.
"""

from __future__ import annotations

from bitsandbytes.stacks.stack import StackEmptyError


class MinStack:
    """LIFO stack with an O(1) ``minimum``.

    Equal minima are stored again. Popping one copy of the minimum must
    leave the earlier copy in place, so the second stack records every
    value that ties the current minimum, not only strict improvements.
    """

    def __init__(self) -> None:
        """Create an empty min-stack.

        Cost
        ----
        Two empty lists are allocated. Time and extra memory are O(1).
        """

        self._items: list[int] = []
        self._minima: list[int] = []

    def __len__(self) -> int:
        """Return how many items are stored.

        Cost
        ----
        The list stores its length. Reading it is O(1).
        """

        return len(self._items)

    def push(self, value: int) -> None:
        """Push ``value`` and update the recorded minimum.

        Cost
        ----
        Appending to the main list is amortized O(1). The minima list is
        appended only when it is empty or ``value`` is less than or equal
        to its top, which is one comparison and at most one append, also
        amortized O(1). Extra memory grows by one slot on the main stack
        and, in the worst case of a non-increasing sequence, one slot on
        the minima stack as well: O(1) per push, O(n) after n pushes.
        """

        self._items.append(value)
        if not self._minima or value <= self._minima[-1]:
            self._minima.append(value)

    def pop(self) -> int:
        """Remove and return the top item, dropping a minimum if it was one.

        Cost
        ----
        ``list.pop()`` with no index removes the last item in O(1). If that
        item equals the recorded minimum, the minima list pops once, also
        O(1). An empty stack raises before either pop. Extra memory is O(1).
        """

        if not self._items:
            raise StackEmptyError("Stack is empty.")
        value = self._items.pop()
        if value == self._minima[-1]:
            self._minima.pop()
        return value

    def peek(self) -> int:
        """Return the top item without removing it.

        Cost
        ----
        The top is the last index of the main list. O(1) time, O(1) extra
        memory. An empty stack raises before the index.
        """

        if not self._items:
            raise StackEmptyError("Stack is empty.")
        return self._items[-1]

    def minimum(self) -> int:
        """Return the smallest value currently stored.

        Cost
        ----
        The minima stack's top is that value, so this is one index: O(1)
        time and O(1) extra memory. It does not scan the n stored items.
        An empty stack raises before the index.
        """

        if not self._minima:
            raise StackEmptyError("Stack is empty.")
        return self._minima[-1]
