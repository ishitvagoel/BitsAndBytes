"""Percolation as a union-find client.

Sites live on an ``n × n`` grid. Open sites union with open north, south,
east, and west neighbors. The bottom row connects to a virtual sink site so
``percolates`` is one ``connected`` query.

Worked trace (2×2, open (0,0), (1,0), (1,1)):

* Opens create unions along edges. The bottom row touches the virtual sink.
* Top row is not connected to the sink → no percolation until (0,1) opens.
"""

from __future__ import annotations

from bitsandbytes.union_find.disjoint_set import DisjointSet


class Percolation:
    """Dynamic connectivity on an ``n × n`` grid."""

    def __init__(self, size: int) -> None:
        """Create a grid with every site blocked.

        Cost
        ----
        O(size²) sites plus one virtual node: O(size²) memory.
        """

        if size < 1:
            raise ValueError("size must be at least 1.")
        self._size = size
        self._open_count = 0
        self._virtual = size * size
        self._sets = DisjointSet(size * size + 1)
        self._open: list[bool] = [False] * (size * size)

    def _index(self, row: int, column: int) -> int:
        return row * self._size + column

    def open(self, row: int, column: int) -> None:
        """Open site ``(row, column)`` and union with open neighbors.

        Cost
        ----
        At most four ``union`` calls, each O(α(n²)) with heuristics. O(1)
        extra memory per call.
        """

        if not (0 <= row < self._size and 0 <= column < self._size):
            raise IndexError("site out of bounds")
        index = self._index(row, column)
        if self._open[index]:
            return
        self._open[index] = True
        self._open_count += 1
        if row == self._size - 1:
            self._sets.union(index, self._virtual)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = row + dr, column + dc
            if 0 <= nr < self._size and 0 <= nc < self._size:
                neighbor = self._index(nr, nc)
                if self._open[neighbor]:
                    self._sets.union(index, neighbor)

    def is_open(self, row: int, column: int) -> bool:
        """Return whether ``(row, column)`` is open.

        Cost
        ----
        O(1).
        """

        index = self._index(row, column)
        return self._open[index]

    def percolates(self) -> bool:
        """Return whether any open site on the top row connects to the bottom.

        Cost
        ----
        One ``connected`` query per top-row open site in the naive check:
        O(size · α(size²)). Tests use small grids.
        """

        for column in range(self._size):
            top = self._index(0, column)
            if self._open[top] and self._sets.connected(top, self._virtual):
                return True
        return False

    @property
    def open_site_count(self) -> int:
        """Return how many sites have been opened.

        Cost
        ----
        O(1).
        """

        return self._open_count
