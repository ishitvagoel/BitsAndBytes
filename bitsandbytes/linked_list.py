"""Singly linked list shared by every list algorithm.

Representation
--------------
Each ``Node`` stores a value and a reference to the next node. The list keeps
the head, the tail, and a cached length so append is O(1).

There is no sentinel (dummy) head. The old scripts mixed a real head with a
dummy node whose data was ``-100000``, which collided with legitimate values
and made every algorithm reimplement the same class. Callers now always start
at ``head``, which is ``None`` when the list is empty.

Cycles
------
``make_circular`` points the tail back at the head. ``refresh`` rebuilds the
cached tail and length after an algorithm rewires ``next`` pointers. A cycle
that does not return to the head cannot be stored in this shape, so ``refresh``
raises ``ValueError`` if it finds one. Floyd's cycle finder lives in
``bitsandbytes.linked_lists.cycle`` and does not use the cache.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

# Printed form used by the original examples: "1 --> 2 --> 3".
SEPARATOR = " --> "


@dataclass(eq=False, slots=True, repr=False)
class Node(Generic[T]):
    """One link in a singly linked list.

    Equality is identity (``is``), not value equality. Two nodes can hold the
    same data and still be different positions, which is what cycle detection
    and list intersection need.
    """

    data: T
    next: Node[T] | None = None

    def __repr__(self) -> str:
        """Return this node's value without following ``next``.

        Cost
        ----
        Formatting one value is O(1) in the length of the list. Following
        ``next`` would be O(n) and would not terminate on a cycle, so the
        repr stops at this node.
        """

        return f"Node(data={self.data!r})"


class LinkedList(Generic[T]):
    """Singly linked list with an O(1) append via a cached tail."""

    def __init__(self, values: Iterable[T] | None = None) -> None:
        """Build an empty list, then append each value in ``values``.

        Cost
        ----
        An empty list is O(1). Supplying k values calls ``append`` k times.
        Each append is O(1), so construction is O(k).
        """

        self.head: Node[T] | None = None
        self._tail: Node[T] | None = None
        self._size = 0
        if values is not None:
            self.extend(values)

    def __len__(self) -> int:
        """Return the cached number of nodes.

        Cost
        ----
        The length is stored on each insert and removal, so this reads one
        integer: O(1). It does not walk the chain.
        """

        return self._size

    def __iter__(self) -> Iterator[T]:
        """Yield each value once.

        Cost
        ----
        One step per node, and each step reads ``data`` and ``next``. n nodes
        take n steps: O(n) time. The iterator holds one node reference: O(1)
        extra memory, plus the set inside ``iter_nodes``.
        """

        for node in self.iter_nodes():
            yield node.data

    def __eq__(self, other: object) -> bool:
        """Compare values in order, ignoring node identity.

        Cost
        ----
        Both lists are walked once and compared element by element. Let n and
        m be their lengths. The walk stops at the first difference, so the
        worst case is O(n + m) time when the lists are equal. Building the two
        temporary lists uses O(n + m) extra memory.
        """

        if not isinstance(other, LinkedList):
            return NotImplemented
        return list(self) == list(other)

    def __repr__(self) -> str:
        """Return a constructor-style view of the values.

        Cost
        ----
        Collecting the values visits n nodes, then formatting them is
        proportional to n. Time and extra memory are both O(n).
        """

        return f"LinkedList({list(self)!r})"

    def __str__(self) -> str:
        """Join the values with `` --> ``.

        Cost
        ----
        Each of the n values is converted and copied into one string. That is
        one pass: O(n) time and O(n) extra memory for the result.
        """

        return SEPARATOR.join(str(value) for value in self)

    @property
    def tail(self) -> Node[T] | None:
        """Return the last node.

        Cost
        ----
        The tail is cached, so this is one attribute read: O(1). It is stale
        only after ``next`` pointers are rewritten by hand; ``refresh`` walks
        the chain to repair it.
        """

        return self._tail

    def iter_nodes(self) -> Iterator[Node[T]]:
        """Yield each node once.

        Identity is tracked so a cycle (back to the head, or a loop further
        along the chain) cannot spin forever. The second visit is not yielded.

        Cost
        ----
        The loop body runs once per distinct node: n iterations. Each
        iteration hashes one id, which is O(1) expected. Time is O(n). The
        ``seen`` set stores n ids, so extra memory is O(n). That set is the
        price of refusing to loop forever on a cycle.
        """

        node = self.head
        seen: set[int] = set()
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            yield node
            node = node.next

    def node_at(self, index: int) -> Node[T]:
        """Return the node at ``index`` (negative indexes count from the end).

        Cost
        ----
        There is no array of nodes. Reaching index i follows ``next`` i times,
        so the walk is O(i). The last node costs O(n). A negative index is
        rewritten with the cached length in O(1), then walked the same way.
        Extra memory is the one ``node`` reference: O(1).
        """

        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("linked list index out of range")
        node = self.head
        assert node is not None
        for _ in range(index):
            assert node.next is not None
            node = node.next
        return node

    def append(self, data: T) -> Node[T]:
        """Add ``data`` after the current tail and return the new node.

        Cost
        ----
        ``_tail`` already points at the last node, so the new node is linked
        with a constant number of pointer writes. No walk: O(1) time and O(1)
        extra memory for the new node, which is part of the list afterwards.
        """

        self._ensure_linear()
        node = Node(data)
        if self._tail is None:
            self.head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1
        return node

    def prepend(self, data: T) -> Node[T]:
        """Add ``data`` before the current head and return the new node.

        Cost
        ----
        The new node points at the current head and becomes ``head``. That is
        a constant number of writes, independent of n: O(1) time and O(1)
        extra memory.
        """

        self._ensure_linear()
        node = Node(data, self.head)
        self.head = node
        if self._tail is None:
            self._tail = node
        self._size += 1
        return node

    def insert(self, index: int, data: T) -> Node[T]:
        """Insert ``data`` so that it lands at ``index``, as ``list.insert`` does.

        Cost
        ----
        Index 0 delegates to ``prepend`` and index ``n`` delegates to
        ``append``, both O(1). Any other index first calls ``node_at(index -
        1)``, which walks ``index - 1`` links. The splice itself is O(1).
        Worst case, inserting in the middle, is O(n) time. Extra memory is
        the new node: O(1).
        """

        self._ensure_linear()
        if index < 0:
            index += self._size
        if index < 0 or index > self._size:
            raise IndexError("insert index out of range")
        if index == 0:
            return self.prepend(data)
        if index == self._size:
            return self.append(data)
        previous = self.node_at(index - 1)
        node = Node(data, previous.next)
        previous.next = node
        self._size += 1
        return node

    def extend(self, values: Iterable[T]) -> None:
        """Append every value from ``values``.

        Cost
        ----
        k values each call ``append``, and each append is O(1). Total time is
        O(k). Extra memory is the k new nodes, which become part of the list.
        """

        for value in values:
            self.append(value)

    def insert_sorted(self, data: T) -> Node[T]:
        """Insert ``data`` into an ascending list.

        The scan stops at the first value strictly greater than ``data``, so
        equal keys stay in insertion order. Comparisons use ``<`` only.

        Cost
        ----
        The scan follows ``next`` until it passes every value that is not
        strictly greater than ``data``. In the worst case that is every node:
        n steps, each one comparison, so O(n) time. The link update is O(1).
        Extra memory is the new node: O(1). A value smaller than the head
        stops immediately and is O(1) via ``prepend``.
        """

        self._ensure_linear()
        if self.head is None or data < self.head.data:
            return self.prepend(data)

        previous = self.head
        current = self.head.next
        # Keep walking while the current value is less than or equal to ``data``,
        # so a new equal key is placed after the ones already in the list.
        while current is not None and not (data < current.data):
            previous = current
            current = current.next
        node = Node(data, current)
        previous.next = node
        if current is None:
            self._tail = node
        self._size += 1
        return node

    def pop(self, index: int = -1) -> T:
        """Remove and return the value at ``index`` (default: the tail).

        Cost
        ----
        Popping the head rewrites ``head`` in O(1). Any other index, including
        the default tail, first walks to the predecessor with ``node_at``,
        which is O(index) and O(n) at the tail. The unlink is then O(1).
        Extra memory is O(1). The cached tail makes append O(1); it does not
        make deleting the tail O(1), because the predecessor is still unknown.
        """

        self._ensure_linear()
        if self._size == 0:
            raise IndexError("pop from empty linked list")
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("pop index out of range")
        if index == 0:
            node = self.head
            assert node is not None
            self.head = node.next
            if self.head is None:
                self._tail = None
            self._size -= 1
            node.next = None
            return node.data

        previous = self.node_at(index - 1)
        node = previous.next
        assert node is not None
        previous.next = node.next
        if node is self._tail:
            self._tail = previous
        self._size -= 1
        node.next = None
        return node.data

    def remove(self, data: T) -> None:
        """Remove the first node whose value equals ``data``.

        Cost
        ----
        The scan compares each node with ``data`` until the first match or the
        end. Worst case, the value is missing or last: n comparisons, O(n)
        time. Unlinking the match is O(1). Extra memory is the ``previous``
        reference: O(1).
        """

        self._ensure_linear()
        previous: Node[T] | None = None
        current = self.head
        while current is not None:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self._tail:
                    self._tail = previous
                current.next = None
                self._size -= 1
                return
            previous = current
            current = current.next
        raise ValueError(f"{data!r} is not in the list")

    def make_circular(self) -> None:
        """Point the tail at the head.

        The list stays the same length. Further inserts and pops are rejected
        until the cycle is broken (see ``split_circular``).

        Cost
        ----
        The tail is cached, so pointing it at the head is one assignment:
        O(1) time and O(1) extra memory. No node is visited.
        """

        if self.head is None or self._tail is None:
            raise ValueError("Cannot make an empty list circular.")
        if self._tail.next not in (None, self.head):
            raise ValueError("Tail is not the end of a linear list.")
        self._tail.next = self.head

    def refresh(self) -> None:
        """Recompute the cached tail and length from ``head``.

        Stops when ``next`` comes back to ``head`` (a simple circular list).
        Any other repeat means the chain is not a single line or circle, and
        the cache cannot describe it.

        Cost
        ----
        The loop advances once per node and stops when ``next`` returns to
        ``head`` or becomes ``None``. That is n iterations. Each iteration
        hashes one id: O(1) expected. Time is O(n). The ``seen`` set holds n
        ids: O(n) extra memory.
        """

        node = self.head
        if node is None:
            self._tail = None
            self._size = 0
            return

        seen = {id(node)}
        count = 1
        while node.next is not None and node.next is not self.head:
            if id(node.next) in seen:
                raise ValueError(
                    "Cycle does not return to the head; the list cache cannot represent it."
                )
            node = node.next
            seen.add(id(node))
            count += 1
        self._tail = node
        self._size = count

    def display(self) -> None:
        """Print the list in the original ``1 --> 2 --> 3`` form.

        Cost
        ----
        ``str(self)`` already walks n nodes and builds an O(n) string.
        Printing that string is O(n) as well. Total time O(n), extra memory
        O(n) for the string.
        """

        print(self)

    def require_linear(self) -> None:
        """Rebuild the cache from ``head`` and reject a circular list.

        Algorithms call this before following ``next`` so a cycle cannot turn
        the walk into an infinite loop. A cycle that does not return to the
        head fails inside ``refresh``.

        Cost
        ----
        This is one ``refresh`` plus a constant check of ``tail.next``.
        ``refresh`` is O(n) time and O(n) extra memory, and the check is O(1),
        so the total is O(n) time and O(n) extra memory.
        """

        self.refresh()
        self._ensure_linear()

    def _ensure_linear(self) -> None:
        """Reject a list whose cached tail already points at another node.

        Cost
        ----
        One comparison of ``tail.next``. No walk: O(1) time and O(1) extra
        memory. The caller must already trust the cache; ``require_linear``
        rebuilds it first.
        """

        if self._tail is not None and self._tail.next is not None:
            raise ValueError("This operation requires a linear linked list.")
