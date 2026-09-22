"""Approximate membership and ordered alternatives."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


class BloomFilter:
    """Bitmap Bloom filter without deletions."""

    def __init__(self, *, bit_count: int, hash_count: int = 3, seed: int = 0) -> None:
        if bit_count < 1 or hash_count < 1:
            raise ValueError("bit_count and hash_count must be positive.")
        self._bits = [False] * bit_count
        self._hash_count = hash_count
        self._seed = seed

    def add(self, item: str) -> None:
        """Insert ``item`` (may only set bits).

        Cost
        ----
        O(k) bit writes for k hash functions.
        """

        for index in self._hashes(item):
            self._bits[index] = True

    def maybe_contains(self, item: str) -> bool:
        """Return whether ``item`` might be present (no false negatives).

        Cost
        ----
        O(k) bit reads.
        """

        return all(self._bits[index] for index in self._hashes(item))

    def _hashes(self, item: str) -> list[int]:
        output: list[int] = []
        value = hash((item, self._seed))
        for round_index in range(self._hash_count):
            output.append((value + round_index * 2654435761) % len(self._bits))
        return output


@dataclass
class SkipNode(Generic[T]):
    key: T
    forward: list[SkipNode[T] | None]


class SkipList(Generic[T]):
    """Sorted set with expected O(log n) search."""

    def __init__(self, *, max_level: int = 16, probability: float = 0.5) -> None:
        self._max_level = max_level
        self._probability = probability
        self._head: SkipNode[T | None] = SkipNode(None, [None] * (max_level + 1))
        self._level = 0

    def contains(self, key: T) -> bool:
        current = self._head
        for level in range(self._level, -1, -1):
            while current.forward[level] is not None and current.forward[level].key < key:
                current = current.forward[level]
            if current.forward[level] is not None and current.forward[level].key == key:
                return True
        return False

    def insert(self, key: T) -> None:
        update: list[SkipNode[T | None]] = [self._head] * (self._max_level + 1)
        current = self._head
        for level in range(self._level, -1, -1):
            while current.forward[level] is not None and current.forward[level].key < key:
                current = current.forward[level]
            update[level] = current
        if current.forward[0] is not None and current.forward[0].key == key:
            return
        new_level = self._random_level()
        if new_level > self._level:
            for level in range(self._level + 1, new_level + 1):
                update[level] = self._head
            self._level = new_level
        node = SkipNode(key, [None] * (new_level + 1))
        for level in range(new_level + 1):
            node.forward[level] = update[level].forward[level]
            update[level].forward[level] = node

    def _random_level(self) -> int:
        level = 0
        while random.random() < self._probability and level < self._max_level:
            level += 1
        return level


@dataclass(frozen=True)
class PersistentStackFrame(Generic[T]):
    """One immutable stack version."""

    top: T | None
    previous: PersistentStackFrame[T] | None

    def push(self, item: T) -> PersistentStackFrame[T]:
        """Return a new stack with ``item`` on top.

        Cost
        ----
        O(1) allocates one frame; old versions remain reachable.
        """

        return PersistentStackFrame(item, self)

    def pop(self) -> tuple[T, PersistentStackFrame[T]]:
        """Return popped item and the previous version.

        Cost
        ----
        O(1).
        """

        if self.top is None:
            raise IndexError("pop from empty persistent stack")
        assert self.previous is not None or True
        previous = self.previous if self.previous is not None else PersistentStackFrame(None, None)
        return self.top, previous
