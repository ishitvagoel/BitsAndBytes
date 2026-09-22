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
        """Return this node's value without following either link.

        Cost
        ----
        One value is formatted. Neither neighbour is visited, so the cost does
        not grow with n: O(1) time and O(1) extra memory.
        """

        return f"DoublyNode(data={self.data!r})"


class DoublyLinkedList(Generic[T]):
    """Doubly linked list with an O(1) append, prepend, and node deletion."""

    def __init__(self, values: Iterable[T] | None = None) -> None:
        """Build an empty list, then append each supplied value.

        Cost
        ----
        Empty construction is O(1). k values each call ``append``, and each
        append is O(1), so the total is O(k) time.
        """

        self._head: DoublyNode[T] | None = None
        self._tail: DoublyNode[T] | None = None
        self._size = 0
        if values is not None:
            for value in values:
                self.append(value)

    def __len__(self) -> int:
        """Return the cached number of nodes.

        Cost
        ----
        The size is updated on every insert and removal, so this is one
        integer read: O(1) time.
        """

        return self._size

    def __iter__(self) -> Iterator[T]:
        """Yield values from head to tail.

        Cost
        ----
        The loop follows ``next`` once per node: n steps, each O(1). Time is
        O(n). Only the current node is kept: O(1) extra memory.
        """

        node = self._head
        while node is not None:
            yield node.data
            node = node.next

    def __repr__(self) -> str:
        """Return a constructor-style view of the values.

        Cost
        ----
        Iteration visits n nodes and the formatted string holds n values.
        Time and extra memory are both O(n).
        """

        return f"DoublyLinkedList({list(self)!r})"

    @property
    def head(self) -> DoublyNode[T] | None:
        """Return the first node.

        Cost
        ----
        The head is stored directly: O(1) time, no extra memory.
        """

        return self._head

    @property
    def tail(self) -> DoublyNode[T] | None:
        """Return the last node.

        Cost
        ----
        The tail is stored directly: O(1) time, no extra memory. Unlike a
        singly linked list, the predecessor of the tail is ``tail.prev``, so
        deleting the tail is also O(1).
        """

        return self._tail

    def append(self, data: T) -> DoublyNode[T]:
        """Add ``data`` after the tail and return the new node.

        Cost
        ----
        The new node is linked to the cached tail with a constant number of
        pointer writes. No walk: O(1) time. The new node is the only
        allocation.
        """

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
        """Add ``data`` before the head and return the new node.

        Cost
        ----
        ``_link_front`` rewrites a constant number of pointers. O(1) time.
        One new node is allocated.
        """

        node = DoublyNode(data)
        self._link_front(node)
        self._size += 1
        return node

    def insert_after(self, node: DoublyNode[T], data: T) -> DoublyNode[T]:
        """Insert ``data`` immediately after ``node`` and return the new node.

        ``node`` must already belong to this list.

        Cost
        ----
        The new node is spliced between ``node`` and ``node.next``. Both
        neighbours are already on ``node``, so nothing is searched. O(1) time,
        one new node.
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

        Cost
        ----
        ``_unlink`` follows ``prev`` and ``next``, which are stored on the
        node. That is a constant number of writes, not a scan of n nodes:
        O(1) time. A singly linked delete of an arbitrary node is O(n)
        because the predecessor must be found from the head.
        """

        self._unlink(node)
        self._size -= 1
        return node.data

    def pop_tail(self) -> T:
        """Remove the tail value.

        Cost
        ----
        The tail and its predecessor are both cached (``tail.prev``).
        ``remove_node`` is therefore O(1) time. Extra memory is O(1).
        """

        if self._tail is None:
            raise IndexError("pop from empty doubly linked list")
        return self.remove_node(self._tail)

    def move_to_front(self, node: DoublyNode[T]) -> None:
        """Move ``node`` to the head without changing its value.

        Used by structures that order nodes by recent use, such as an LRU
        cache. Moving the current head is a no-op.

        Cost
        ----
        Unlink is O(1) and linking at the front is O(1). The node is not
        copied. Total O(1) time and O(1) extra memory. If this required a
        search from the head it would be O(n); the ``prev`` pointer is why
        it is not.
        """

        if node is self._head:
            return
        self._unlink(node)
        self._link_front(node)

    def reverse(self) -> None:
        """Reverse the list by swapping each node's two links.

        Cost
        ----
        The loop body runs once per node: n iterations. Each iteration swaps
        two references, which is O(1). Time is n * O(1) = O(n). Only
        ``current`` is stored: O(1) extra memory. The head/tail swap at the
        end is O(1).
        """

        current = self._head
        while current is not None:
            # ``next`` is saved by the swap: after it, the old successor is ``prev``.
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self._head, self._tail = self._tail, self._head

    def _unlink(self, node: DoublyNode[T]) -> None:
        """Detach ``node`` and leave the size unchanged.

        Cost
        ----
        At most four pointer assignments, using ``node.prev`` and
        ``node.next`` directly. O(1) time, O(1) extra memory.
        """

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
        """Place an unlinked node at the head. Does not change the size.

        Cost
        ----
        The node is pointed at the current head and becomes ``head``. A
        constant number of writes: O(1) time, O(1) extra memory.
        """

        node.prev = None
        node.next = self._head
        if self._head is None:
            self._tail = node
        else:
            self._head.prev = node
        self._head = node
