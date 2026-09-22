"""Union-find and percolation."""

from bitsandbytes.union_find import DisjointSet
from bitsandbytes.union_find.percolation import Percolation


def test_disjoint_set_without_heuristics_chain() -> None:
    dsu = DisjointSet(3, use_heuristics=False)
    dsu.union(0, 1)
    dsu.union(1, 2)
    assert dsu.connected(0, 2)


def test_percolation_does_not_connect_until_path_exists() -> None:
    grid = Percolation(2)
    grid.open(1, 0)
    grid.open(1, 1)
    assert not grid.percolates()
    grid.open(0, 1)
    assert grid.percolates()
