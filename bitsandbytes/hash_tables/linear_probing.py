"""Open-addressing hash table with linear probing."""

from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

_TOMBSTONE = object()


class LinearProbingHashTable(MutableMapping[K, V]):
    """Mutable mapping with linear probing and tombstones on delete."""

    def __init__(self, *, capacity: int = 8) -> None:
        """Create an empty table with at least ``capacity`` slots.

        Cost
        ----
        O(capacity) time and memory for the slot arrays.
        """

        if capacity < 1:
            raise ValueError("capacity must be at least 1.")
        self._capacity = capacity
        self._keys: list[K | None | object] = [None] * capacity
        self._values: list[V | None] = [None] * capacity
        self._size = 0

    def __len__(self) -> int:
        """Return how many keys are stored.

        Cost
        ----
        O(1).
        """

        return self._size

    def __iter__(self) -> Iterator[K]:
        """Yield every stored key once.

        Cost
        ----
        O(capacity) scan in the worst case.
        """

        for key in self._keys:
            if key is not None and key is not _TOMBSTONE:
                yield key

    def __getitem__(self, key: K) -> V:
        """Return the value for ``key``.

        Cost
        ----
        Probe until empty slot: expected O(1) when load factor stays bounded
        away from 1; worst O(n) if the table clusters.
        """

        for index in self._probe(key):
            slot_key = self._keys[index]
            if slot_key is None:
                break
            if slot_key is _TOMBSTONE:
                continue
            if slot_key == key:
                value = self._values[index]
                assert value is not None
                return value
        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """Store ``value`` under ``key``.

        Cost
        ----
        Same probing cost as lookup. Rehash when load exceeds one half.
        """

        if self._size * 2 >= self._capacity:
            self._rehash(self._capacity * 2)
        for index in self._probe(key):
            slot_key = self._keys[index]
            if slot_key is None or slot_key is _TOMBSTONE:
                self._keys[index] = key
                self._values[index] = value
                self._size += 1
                return
            if slot_key == key:
                self._values[index] = value
                return
        raise RuntimeError("linear probing table is unexpectedly full")

    def __delitem__(self, key: K) -> None:
        """Remove ``key`` leaving a tombstone.

        Cost
        ----
        One probe sequence: expected O(1), worst O(n).
        """

        for index in self._probe(key):
            slot_key = self._keys[index]
            if slot_key is None:
                break
            if slot_key is _TOMBSTONE:
                continue
            if slot_key == key:
                self._keys[index] = _TOMBSTONE
                self._values[index] = None
                self._size -= 1
                return
        raise KeyError(key)

    def load_factor(self) -> float:
        """Return ``size / capacity``.

        Cost
        ----
        O(1).
        """

        return self._size / self._capacity

    def _probe(self, key: K) -> Iterator[int]:
        start = hash(key) % self._capacity
        for offset in range(self._capacity):
            yield (start + offset) % self._capacity

    def _rehash(self, new_capacity: int) -> None:
        entries = list(self.items())
        self._capacity = new_capacity
        self._keys = [None] * new_capacity
        self._values = [None] * new_capacity
        self._size = 0
        for key, value in entries:
            self[key] = value


def degenerate_chain_length(key_count: int, bucket_count: int) -> int:
    """Return bucket length when every key lands in one bucket.

    With ``bucket_count == 1``, separate chaining devolves to scanning a list
    of length ``key_count``. CPython randomizes hashes in production ``dict``
    so another process cannot be forced into this shape cheaply.

    Cost
    ----
    O(1) arithmetic.
    """

    if key_count < 0:
        raise ValueError("key_count cannot be negative.")
    if bucket_count < 1:
        raise ValueError("bucket_count must be at least 1.")
    if bucket_count == 1:
        return key_count
    return (key_count + bucket_count - 1) // bucket_count
