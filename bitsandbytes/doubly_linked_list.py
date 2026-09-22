"""Doubly linked list.

Each node stores ``prev`` as well as ``next``. The extra pointer is what makes
"delete this node" and "insert beside this node" O(1). A singly linked list
has to walk from the head to find the predecessor, which is O(n).

The head's ``prev`` and the tail's ``next`` are ``None``. There is no sentinel
node. Sentinels remove a few empty-list branches, but they also hide the
empty cases that are worth seeing once. The branches are short and local.

Reversal swaps the two pointers on every node and then swaps the head with
the tail. After the swap, following ``next`` walks the old list backwards.

Time for insert, append, prepend, and delete-given-the-node is O(1).
Indexing is still O(n): the second pointer does not create random access.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(eq=False, slots=True, repr=False)
class DoublyNode(Generic[T]):
    """One link with neighbours on both sides.

    Equality is identity. Two nodes may hold the same value and still be
    different positions.
    """

    data: T
    prev: DoublyNode[T] | None = None
    next: DoublyNode[T] | None = None

    def __repr__(self) -> str:
        return f"DoublyNode(data={self.data!r})"


class DoublyLinkedList(Generic[T]):
    """Doubly linked list with an O(1) append, prepend, and node deletion."""

    def __init__(self, values: Iterable[T] | None = None) -> None:
        self._head: DoublyNode[T] | None = None
        self._tail: DoublyNode[T] | None = None
        self._size = 0
        if values is not None:
            for value in values:
                self.append(value)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __repr__(self) -> str:
        return f"DoublyLinkedList({list(self)!r})"

    @property
    def head(self) -> DoublyNode[T] | None:
        return self._head

    @property
    def tail(self) -> DoublyNode[T] | None:
        return self._tail

    def append(self, data: T) -> DoublyNode[T]:
        """Add ``data`` after the tail and return the new node."""

        node = DoublyNode(data)
        node.prev = self._tail
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1
        return node

    def prepend(self, data: T) -> DoublyNode[T]:
        """Add ``data`` before the head and return the new node."""

        node = DoublyNode(data)
        self._link_front(node)
        self._size += 1
        return node

    def insert_after(self, node: DoublyNode[T], data: T) -> DoublyNode[T]:
        """Insert ``data`` immediately after ``node`` and return the new node.

        ``node`` must already belong to this list.
        """

        created = DoublyNode(data)
        created.prev = node
        created.next = node.next
        node.next = created
        if created.next is None:
            self._tail = created
        else:
            created.next.prev = created
        self._size += 1
        return created

    def remove_node(self, node: DoublyNode[T]) -> T:
        """Unlink ``node`` in O(1) and return its value.

        ``node`` must belong to this list. The list does not search for it:
        the previous and next pointers are enough.
        """

        self._unlink(node)
        self._size -= 1
        return node.data

    def pop_tail(self) -> T:
        """Remove the tail value."""

        if self._tail is None:
            raise IndexError("pop from empty doubly linked list")
        return self.remove_node(self._tail)

    def move_to_front(self, node: DoublyNode[T]) -> None:
        """Move ``node`` to the head without changing its value.

        Used by structures that order nodes by recent use, such as an LRU
        cache. Moving the current head is a no-op.
        """

        if node is self._head:
            return
        self._unlink(node)
        self._link_front(node)

    def reverse(self) -> None:
        """Reverse the list by swapping each node's two links."""

        current = self._head
        while current is not None:
            # ``next`` is saved by the swap: after it, the old successor is ``prev``.
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self._head, self._tail = self._tail, self._head

    def _unlink(self, node: DoublyNode[T]) -> None:
        """Detach ``node`` and leave the size unchanged."""

        if node.prev is not None:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self._tail = node.prev
        node.prev = None
        node.next = None

    def _link_front(self, node: DoublyNode[T]) -> None:
        """Place an unlinked node at the head. Does not change the size."""

        node.prev = None
        node.next = self._head
        if self._head is None:
            self._tail = node
        else:
            self._head.prev = node
        self._head = node
