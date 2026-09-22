"""Binary search tree.

Insert walks from the root comparing with ``<``. Search is the same walk.
The height of the tree controls the cost: balanced shapes are O(log n) per
operation; a sorted insert chain is O(n).

In-order traversal visits left subtree, node, right subtree. The iterative
version uses the same stack as depth-first search on a tree.

Worked trace (insert 5, 2, 8 then search 2):

* Insert 5 at root. Insert 2 as left child. Insert 8 as right child.
* Search compares at 5, goes left, finds 2 in two steps.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(eq=False, slots=True)
class TreeNode(Generic[T]):
    """One node in a binary search tree."""

    data: T
    left: TreeNode[T] | None = None
    right: TreeNode[T] | None = None


class BinarySearchTree(Generic[T]):
    """Binary search tree ordered by ``<`` on ``data``."""

    def __init__(self) -> None:
        """Create an empty tree.

        Cost
        ----
        O(1) time and O(1) extra memory.
        """

        self.root: TreeNode[T] | None = None

    def insert(self, value: T) -> None:
        """Insert ``value`` if it is not already present.

        Cost
        ----
        One comparison per level. h levels take h steps: O(h) time, O(h)
        call-stack memory for the recursive walk, O(1) if rewritten
        iteratively. Worst h is n on a sorted insert chain.
        """

        if self.root is None:
            self.root = TreeNode(value)
            return
        node = self.root
        while True:
            if value < node.data:
                if node.left is None:
                    node.left = TreeNode(value)
                    return
                node = node.left
            elif node.data < value:
                if node.right is None:
                    node.right = TreeNode(value)
                    return
                node = node.right
            else:
                return

    def contains(self, value: T) -> bool:
        """Return whether ``value`` is stored.

        Cost
        ----
        Same walk as ``insert`` without creating nodes: O(h) time, O(1)
        extra memory iteratively.
        """

        node = self.root
        while node is not None:
            if value < node.data:
                node = node.left
            elif node.data < value:
                node = node.right
            else:
                return True
        return False

    def inorder(self) -> list[T]:
        """Return values in sorted order.

        Cost
        ----
        Each node is pushed and popped once on the stack: O(n) time, O(h)
        extra memory for the stack where h is the height.
        """

        return list(self.inorder_iter())

    def inorder_iter(self) -> Iterator[T]:
        """Yield values in sorted order using an explicit stack.

        Cost
        ----
        Every node is visited once. Time O(n). The stack holds at most h
        nodes: O(h) extra memory.
        """

        from bitsandbytes.trees.traversals import inorder_iter

        yield from inorder_iter(self.root)

    def delete(self, value: T) -> bool:
        """Remove ``value`` if present. Return whether a node was removed.

        Worked trace (delete ``3`` from ``2 <- 3 -> 5``):

        * Search finds the node with one right child.
        * Replace its data with the in-order successor ``5``, then delete the
          successor leaf.

        Cost
        ----
        Search is O(h). Each case performs a constant number of pointer
        rewrites, except the two-child case which walks the right spine for
        the successor, still O(h). Total O(h) time, O(1) extra memory
        iteratively.
        """

        self.root, removed = _delete_node(self.root, value)
        return removed


def _delete_node(
    node: TreeNode[T] | None,
    value: T,
) -> tuple[TreeNode[T] | None, bool]:
    """Return the new subtree root and whether a deletion happened."""

    if node is None:
        return None, False
    if value < node.data:
        node.left, removed = _delete_node(node.left, value)
        return node, removed
    if node.data < value:
        node.right, removed = _delete_node(node.right, value)
        return node, removed
    # Match found.
    if node.left is None:
        return node.right, True
    if node.right is None:
        return node.left, True
    successor = node.right
    while successor.left is not None:
        successor = successor.left
    node.data = successor.data
    node.right, _ = _delete_node(node.right, successor.data)
    return node, True
