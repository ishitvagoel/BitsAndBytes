"""Binary search tree.

Insert walks from the root comparing with ``<``. Search is the same walk.
The height of the tree controls the cost: balanced shapes are O(log n) per
operation; a sorted insert chain is O(n).

In-order traversal visits left subtree, node, right subtree. The iterative
version uses the same stack as depth-first search on a tree.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

from bitsandbytes.stacks.algorithm_stack import AlgorithmStack

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

        stack: AlgorithmStack[TreeNode[T]] = AlgorithmStack()
        node = self.root
        while node is not None or not stack.is_empty:
            while node is not None:
                stack.push(node)
                node = node.left
            current = stack.pop()
            yield current.data
            node = current.right
