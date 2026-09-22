"""Hash table with separate chaining.

Each bucket is a short list of ``(key, value)`` pairs. Collisions append to
the same bucket instead of probing forward in the array. Lookup scans only
that bucket. With a good hash and load factor, the expected bucket length
is O(1).

This table resizes when ``len(table) > 2 * bucket_count`` so buckets stay
short. Rehashing every entry costs O(n) but happens rarely enough that
insert stays O(1) amortized expected.
"""

from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class ChainingHashTable(MutableMapping[K, V]):
    """Mutable mapping implemented with separate chaining."""

    def __init__(self, *, bucket_count: int = 8) -> None:
        """Create an empty table with ``bucket_count`` buckets.

        Cost
        ----
        Allocate ``bucket_count`` empty lists: O(bucket_count) time and
        memory.
        """

        if bucket_count < 1:
            raise ValueError("bucket_count must be at least 1.")
        self._bucket_count = bucket_count
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(bucket_count)]
        self._size = 0

    def __len__(self) -> int:
        """Return how many keys are stored.

        Cost
        ----
        The size counter is O(1).
        """

        return self._size

    def __iter__(self) -> Iterator[K]:
        """Yield every stored key once.

        Cost
        ----
        Every bucket is scanned. With n entries and b buckets this is O(n + b)
        time in the worst case. Extra memory is O(1) besides the iterator.
        """

        for bucket in self._buckets:
            for key, _value in bucket:
                yield key

    def __getitem__(self, key: K) -> V:
        """Return the value for ``key``.

        Cost
        ----
        One hash and a scan of the bucket that holds ``key``. Expected
        O(1) when buckets stay short; worst case O(n) if every key collides.
        """

        for stored_key, value in self._buckets[self._bucket_index(key)]:
            if stored_key == key:
                return value
        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """Store ``value`` under ``key``.

        Cost
        ----
        Expected O(1) for the bucket scan plus maybe O(n) to rehash every
        entry when the table doubles. Amortized expected O(1) over many
        inserts.
        """

        bucket = self._buckets[self._bucket_index(key)]
        for index, (stored_key, _old) in enumerate(bucket):
            if stored_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > 2 * self._bucket_count:
            self._rehash()

    def __delitem__(self, key: K) -> None:
        """Remove ``key`` and its value.

        Cost
        ----
        Scan one bucket: expected O(1), worst O(n).
        """

        bucket = self._buckets[self._bucket_index(key)]
        for index, (stored_key, _value) in enumerate(bucket):
            if stored_key == key:
                del bucket[index]
                self._size -= 1
                return
        raise KeyError(key)

    def _bucket_index(self, key: K) -> int:
        """Map ``key`` to a bucket index.

        Cost
        ----
        ``hash`` and one modulo: O(1) expected.
        """

        return hash(key) % self._bucket_count

    def _rehash(self) -> None:
        """Double the bucket count and redistribute every entry.

        Cost
        ----
        Let n be ``self._size``. Every entry is reinserted once: O(n) time.
        The new bucket array holds O(n) slots after doubling.
        """

        entries = list(self.items())
        self._bucket_count *= 2
        self._buckets = [[] for _ in range(self._bucket_count)]
        self._size = 0
        for key, value in entries:
            self[key] = value
