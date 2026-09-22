"""Least-recently-used cache.

An LRU cache of capacity ``k`` remembers the last ``k`` keys that were read
or written. Past that, the key that has gone unused the longest is evicted.

Two structures together make every operation O(1):

* A dictionary maps a key to the node that holds it, so lookup does not walk
  the list.
* A doubly linked list orders those nodes by use. The head is the most
  recently used and the tail is the least recently used. ``move_to_front`` and
  ``remove_node`` are O(1) only because each node knows its predecessor. A
  singly linked list would make eviction O(k).

``get`` moves the key to the front. ``put`` of an existing key updates the
value and moves it to the front. ``put`` of a new key evicts the tail when the
cache is already full, then inserts the new key at the front.

Capacity must be at least 1. A missing ``get`` returns ``None``.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from bitsandbytes.doubly_linked_list import DoublyLinkedList, DoublyNode

K = TypeVar("K")
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """Fixed-capacity cache that evicts the least recently used key."""

    def __init__(self, capacity: int) -> None:
        """Create an empty cache that keeps at most ``capacity`` keys.

        Cost
        ----
        An empty dictionary and an empty doubly linked list are O(1) to
        allocate. No keys are copied.
        """

        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be a positive integer.")
        self.capacity = capacity
        self._nodes: dict[K, DoublyNode[tuple[K, V]]] = {}
        self._order: DoublyLinkedList[tuple[K, V]] = DoublyLinkedList()

    def __len__(self) -> int:
        """Return how many keys are currently stored.

        Cost
        ----
        The dictionary stores its size. ``len`` is O(1).
        """

        return len(self._nodes)

    def get(self, key: K) -> V | None:
        """Return the value for ``key``, or ``None`` if it is not cached.

        A hit counts as a use, so the key becomes the most recently used.

        Cost
        ----
        Dictionary lookup is O(1) expected. ``move_to_front`` uses ``prev``
        and ``next``, so it is O(1). A miss returns after the lookup. Total
        O(1) expected time, O(1) extra memory. Scanning a list of capacity k
        would be O(k); the dictionary is what removes that scan.
        """

        node = self._nodes.get(key)
        if node is None:
            return None
        self._order.move_to_front(node)
        return node.data[1]

    def put(self, key: K, value: V) -> None:
        """Store ``value`` under ``key``, evicting the stale tail if needed.

        Cost
        ----
        Lookup, update, ``move_to_front``, ``remove_node``, and ``prepend``
        are each O(1) expected (dictionary) or O(1) exact (the doubly linked
        list). At most one of those list edits runs. Time is O(1) expected.
        Extra memory is O(1) per call. The cache as a whole holds at most
        ``capacity`` nodes, so its resident memory is O(capacity).
        """

        existing = self._nodes.get(key)
        if existing is not None:
            existing.data = (key, value)
            self._order.move_to_front(existing)
            return

        if len(self._nodes) == self.capacity:
            stale = self._order.tail
            assert stale is not None
            del self._nodes[stale.data[0]]
            self._order.remove_node(stale)

        self._nodes[key] = self._order.prepend((key, value))
