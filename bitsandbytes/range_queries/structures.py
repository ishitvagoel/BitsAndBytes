"""Range query structures."""

from __future__ import annotations

from collections.abc import Sequence


class FenwickTree:
    """Binary indexed tree for prefix sums with point updates."""

    def __init__(self, size: int) -> None:
        """Create a tree of length ``size`` initialized to zero.

        Cost
        ----
        O(size) memory.
        """

        if size < 0:
            raise ValueError("size cannot be negative.")
        self._size = size
        self._tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        """Add ``delta`` at ``index`` (0-based).

        Cost
        ----
        O(log n) index hops.
        """

        position = index + 1
        while position <= self._size:
            self._tree[position] += delta
            position += position & -position

    def prefix_sum(self, index: int) -> int:
        """Return sum of ``[0, index]`` inclusive.

        Cost
        ----
        O(log n).
        """

        total = 0
        position = index + 1
        while position > 0:
            total += self._tree[position]
            position -= position & -position
        return total


class SegmentTree:
    """Segment tree with lazy range addition on leaf values."""

    def __init__(self, values: Sequence[int]) -> None:
        """Build over ``values``.

        Cost
        ----
        O(n) build.
        """

        self._values = list(values)
        self._size = len(values)
        self._lazy = [0] * (4 * max(1, self._size))

    def range_add(self, left: int, right: int, delta: int) -> None:
        """Add ``delta`` to every index in ``[left, right]``.

        Cost
        ----
        O(log n) lazy propagation.
        """

        self._update(1, 0, self._size - 1, left, right, delta)

    def point_query(self, index: int) -> int:
        """Return value at ``index`` after pending lazy updates.

        Cost
        ----
        O(log n).
        """

        return self._point(1, 0, self._size - 1, index)

    def _apply(self, node: int, left: int, right: int, delta: int) -> None:
        self._lazy[node] += delta

    def _push(self, node: int, left: int, right: int) -> None:
        if self._lazy[node] == 0 or left == right:
            return
        middle = (left + right) // 2
        self._lazy[node * 2] += self._lazy[node]
        self._lazy[node * 2 + 1] += self._lazy[node]
        self._lazy[node] = 0

    def _update(
        self,
        node: int,
        left: int,
        right: int,
        qleft: int,
        qright: int,
        delta: int,
    ) -> None:
        if qright < left or right < qleft:
            return
        if qleft <= left and right <= qright:
            self._apply(node, left, right, delta)
            return
        self._push(node, left, right)
        middle = (left + right) // 2
        self._update(node * 2, left, middle, qleft, qright, delta)
        self._update(node * 2 + 1, middle + 1, right, qleft, qright, delta)

    def _point(self, node: int, left: int, right: int, index: int) -> int:
        if left == right:
            return self._values[index] + self._lazy[node]
        self._push(node, left, right)
        middle = (left + right) // 2
        if index <= middle:
            return self._point(node * 2, left, middle, index)
        return self._point(node * 2 + 1, middle + 1, right, index)


class SparseTable:
    """Static range minimum queries on an idempotent operation (min)."""

    def __init__(self, values: Sequence[int]) -> None:
        """Preprocess ``values``.

        Cost
        ----
        O(n log n) time and memory.
        """

        import math

        self._values = list(values)
        length = len(values)
        levels = max(1, length.bit_length())
        self._table = [[0] * length for _ in range(levels)]
        if length:
            self._table[0] = list(values)
            for level in range(1, levels):
                span = 1 << level
                half = span >> 1
                for index in range(0, length - span + 1):
                    self._table[level][index] = min(
                        self._table[level - 1][index],
                        self._table[level - 1][index + half],
                    )

    def range_min(self, left: int, right: int) -> int:
        """Return minimum on ``[left, right]`` inclusive.

        Cost
        ----
        O(1) after O(n log n) build.
        """

        import math

        length = right - left + 1
        level = length.bit_length() - 1
        span = 1 << level
        return min(self._table[level][left], self._table[level][right - span + 1])
