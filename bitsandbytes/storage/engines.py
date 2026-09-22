"""In-memory B-tree, toy LSM, WAL, locality, and brute-force search."""

from __future__ import annotations

import time
from collections.abc import Sequence
from typing import Generic, TypeVar

from bitsandbytes.approximate.structures import BloomFilter
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree

T = TypeVar("T")
K = TypeVar("K")


class BTree(Generic[T]):
    """In-memory B-tree with minimum degree ``branching`` (t >= 2)."""

    def __init__(self, branching: int = 3) -> None:
        if branching < 2:
            raise ValueError("branching must be at least 2.")
        self.branching = branching
        self.root: _BNode[T] = _BNode[T](leaf=True)

    def search(self, key: T) -> bool:
        return self._search(self.root, key)

    def insert(self, key: T) -> None:
        root = self.root
        if len(root.keys) == 2 * self.branching - 1:
            new_root: _BNode[T] = _BNode[T](leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _search(self, node: _BNode[T], key: T) -> bool:
        index = 0
        while index < len(node.keys) and key > node.keys[index]:
            index += 1
        if index < len(node.keys) and key == node.keys[index]:
            return True
        if node.leaf:
            return False
        return self._search(node.children[index], key)

    def _insert_non_full(self, node: _BNode[T], key: T) -> None:
        index = len(node.keys) - 1
        if node.leaf:
            node.keys.append(key)
            while index >= 0 and key < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
        else:
            while index >= 0 and key < node.keys[index]:
                index -= 1
            index += 1
            if len(node.children[index].keys) == 2 * self.branching - 1:
                self._split_child(node, index)
                if key > node.keys[index]:
                    index += 1
            self._insert_non_full(node.children[index], key)

    def _split_child(self, parent: _BNode[T], index: int) -> None:
        branching = self.branching
        full = parent.children[index]
        middle = branching - 1
        promoted = full.keys[middle]
        right = _BNode[T](leaf=full.leaf)
        right.keys = full.keys[middle + 1 :]
        full.keys = full.keys[:middle]
        if not full.leaf:
            right.children = full.children[middle + 1 :]
            full.children = full.children[: middle + 1]
        parent.keys.insert(index, promoted)
        parent.children.insert(index + 1, right)


class _BNode(Generic[T]):
    def __init__(self, *, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: list[T] = []
        self.children: list[_BNode[T]] = []


class WriteAheadLog:
    """Append-only log replayed into a memtable on recovery."""

    def __init__(self) -> None:
        self._entries: list[tuple[str, str]] = []

    def append(self, operation: str, key: str) -> None:
        self._entries.append((operation, key))

    def replay(self, memtable: LeftLeaningRedBlackTree[str]) -> None:
        for operation, key in self._entries:
            if operation == "put":
                memtable.insert(key)
            elif operation == "delete":
                memtable.delete(key)


class ToyLSM:
    """Memtable, Bloom-filtered runs, and merge compaction."""

    def __init__(self) -> None:
        self.memtable: LeftLeaningRedBlackTree[str] = LeftLeaningRedBlackTree()
        self.runs: list[tuple[BloomFilter, list[str]]] = []
        self.wal = WriteAheadLog()

    def put(self, key: str) -> None:
        self.wal.append("put", key)
        self.memtable.insert(key)
        if len(self.memtable) >= 8:
            self._flush()

    def maybe_contains(self, key: str) -> bool:
        if self.memtable.contains(key):
            return True
        for bloom, run in self.runs:
            if not bloom.maybe_contains(key):
                continue
            if key in run:
                return True
        return False

    def _flush(self) -> None:
        keys = self.memtable.inorder()
        bloom = BloomFilter(bit_count=max(32, len(keys) * 8))
        for key in keys:
            bloom.add(key)
        self.runs.append((bloom, keys))
        self.memtable = LeftLeaningRedBlackTree()


def sequential_scan_sum(values: Sequence[int]) -> int:
    """Sum ``values`` for locality comparison with indexed access.

    Cost
    ----
    O(n) additions; wall time may vary with layout but operation count is n.
    """

    return sum(values)


def locality_scan_benchmark(values: Sequence[int], *, repeats: int = 3) -> float:
    """Return median wall seconds to scan ``values`` ``repeats`` times.

    Cost
    ----
    The measured loop is O(repeats · n); timing is allowed to be noisy.
    """

    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        sequential_scan_sum(values)
        timings.append(time.perf_counter() - start)
    timings.sort()
    return timings[len(timings) // 2]


def nearest_neighbor_linear(
    points: Sequence[tuple[float, ...]],
    query: Sequence[float],
) -> int:
    """Return index of closest point under squared Euclidean distance.

    Cost
    ----
    O(nd) for n points of dimension d.
    """

    best_index = 0
    best_distance = float("inf")
    for index, point in enumerate(points):
        distance = sum((a - b) ** 2 for a, b in zip(point, query, strict=True))
        if distance < best_distance:
            best_distance = distance
            best_index = index
    return best_index
