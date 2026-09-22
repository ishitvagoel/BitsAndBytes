"""Disjoint-set union with and without union-by-rank and path compression.

Without the heuristics, a sequence of unions can build a chain of height n,
so ``find`` costs O(n). With rank and compression, the inverse-Ackermann bound
is the textbook result; this module exposes both implementations so the worse
tree has code to point at.

Worked trace (naive union of 0-1 and 1-2):

* After ``union(0,1)``, parent[1]=0.
* After ``union(1,2)``, parent[2]=0 through find(1).
* ``find(2)`` walks two links.
"""

from __future__ import annotations


class DisjointSet:
    """Disjoint-set forest with optional heuristics."""

    def __init__(self, size: int, *, use_heuristics: bool = True) -> None:
        """Create ``size`` singleton sets labeled ``0 .. size-1``.

        Cost
        ----
        O(size) time and memory to fill parent (and rank) arrays.
        """

        if size < 0:
            raise ValueError("size cannot be negative.")
        self._parent = list(range(size))
        self._rank = [0] * size
        self._use_heuristics = use_heuristics

    def find(self, item: int) -> int:
        """Return the representative of ``item``'s set.

        Cost
        ----
        Without heuristics, worst-case O(n) on a chain. With path compression,
        the amortized bound is inverse Ackermann. Extra memory O(1) besides
        the arrays.
        """

        if item < 0 or item >= len(self._parent):
            raise IndexError("item out of range")
        if not self._use_heuristics:
            while self._parent[item] != item:
                item = self._parent[item]
            return item
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[item] != item:
            parent = self._parent[item]
            self._parent[item] = root
            item = parent
        return root

    def union(self, first: int, second: int) -> None:
        """Merge the sets containing ``first`` and ``second``.

        Cost
        ----
        Two ``find`` operations plus O(1) pointer writes. Same asymptotics as
        ``find``.
        """

        root_first = self.find(first)
        root_second = self.find(second)
        if root_first == root_second:
            return
        if not self._use_heuristics:
            self._parent[root_second] = root_first
            return
        if self._rank[root_first] < self._rank[root_second]:
            root_first, root_second = root_second, root_first
        self._parent[root_second] = root_first
        if self._rank[root_first] == self._rank[root_second]:
            self._rank[root_first] += 1

    def connected(self, first: int, second: int) -> bool:
        """Return whether ``first`` and ``second`` are in the same set.

        Cost
        ----
        Two ``find`` calls.
        """

        return self.find(first) == self.find(second)
