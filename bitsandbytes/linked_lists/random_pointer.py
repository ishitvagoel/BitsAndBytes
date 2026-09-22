"""Clone a linked list whose nodes also point at an arbitrary node.

A ``random`` pointer may aim at any node in the list, or at nothing. A plain
walk cannot copy it yet, because the node it should aim at may not have been
cloned.

The straightforward clone stores ``original → copy`` in a dictionary, then
makes a second pass to wire ``next`` and ``random``. That is O(n) time and
O(n) extra memory, and it is the version to write first.

The interleaved clone removes the dictionary:

1. Insert each copy directly after its original.
   ``A → B → C`` becomes ``A → A' → B → B' → C → C'``.
2. The copy of ``node.random`` is ``node.random.next``, because the copy was
   just inserted after the original random target.
3. Split the chain back into the original list and the clone. The original
   ``next`` pointers are restored.

Time O(n). The interleaved clone uses O(1) extra memory besides the clone
itself, which any correct copy has to allocate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(eq=False, slots=True, repr=False)
class RandomNode(Generic[T]):
    """A node with a successor and one extra pointer that may land anywhere."""

    data: T
    next: RandomNode[T] | None = None
    random: RandomNode[T] | None = None

    def __repr__(self) -> str:
        """Return this node's value without following ``next`` or ``random``.

        Cost
        ----
        One value is formatted. ``random`` can point backward or at this
        node, so following it would not be O(1) and might not terminate.
        Time O(1), extra memory O(1).
        """

        return f"RandomNode(data={self.data!r})"


def clone_with_map(head: RandomNode[T] | None) -> RandomNode[T] | None:
    """Clone ``head`` using a dictionary from each original node to its copy.

    Cost
    ----
    Let n be the number of nodes. The first loop creates n copies: O(n).
    The second loop wires ``next`` and ``random`` with two dictionary reads
    per node. A dictionary read is O(1) expected, so the second loop is O(n)
    expected. Total time O(n) expected. The dictionary stores n entries:
    O(n) extra memory, on top of the n cloned nodes which are the output.
    """

    if head is None:
        return None
    copies: dict[int, RandomNode[T]] = {}
    current: RandomNode[T] | None = head
    while current is not None:
        copies[id(current)] = RandomNode(current.data)
        current = current.next

    current = head
    while current is not None:
        copy = copies[id(current)]
        if current.next is not None:
            copy.next = copies[id(current.next)]
        if current.random is not None:
            copy.random = copies[id(current.random)]
        current = current.next
    return copies[id(head)]


def clone_interleaved(head: RandomNode[T] | None) -> RandomNode[T] | None:
    """Clone ``head`` by weaving each copy into the original chain, then splitting.

    Cost
    ----
    Three passes each visit every original node once, and the woven chain
    has 2n nodes during the middle pass. Each pass does a constant amount of
    pointer work per node. Time is 3 * O(n) = O(n). No dictionary is kept.
    Scratch memory is a few references: O(1), besides the n cloned nodes
    that form the result.
    """

    if head is None:
        return None

    current: RandomNode[T] | None = head
    while current is not None:
        copy = RandomNode(current.data, current.next)
        current.next = copy
        current = copy.next

    current = head
    while current is not None:
        copy = current.next
        assert copy is not None
        if current.random is not None:
            # The copy of the random target was inserted immediately after it.
            copy.random = current.random.next
        current = copy.next

    clone_head = head.next
    current = head
    while current is not None:
        copy = current.next
        assert copy is not None
        current.next = copy.next
        following = copy.next
        copy.next = following.next if following is not None else None
        current = current.next
    return clone_head
