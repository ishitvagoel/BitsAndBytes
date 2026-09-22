"""Binary tree traversals on explicit ``TreeNode`` objects."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Generic, TypeVar

from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.stacks.algorithm_stack import AlgorithmStack
from bitsandbytes.trees.bst import TreeNode

T = TypeVar("T")


def preorder(root: TreeNode[T] | None) -> list[T]:
    """Return root, then left subtree, then right subtree.

    Cost
    ----
    Each node is pushed and popped once on the stack: O(n) time, O(h) extra
    memory for height h (O(n) if the tree is a chain).
    """

    if root is None:
        return []
    order: list[T] = []
    stack: AlgorithmStack[TreeNode[T]] = AlgorithmStack()
    stack.push(root)
    while not stack.is_empty:
        node = stack.pop()
        order.append(node.data)
        if node.right is not None:
            stack.push(node.right)
        if node.left is not None:
            stack.push(node.left)
    return order


def postorder(root: TreeNode[T] | None) -> list[T]:
    """Return left subtree, right subtree, then root.

    Cost
    ----
    Two passes with a stack, still O(n) time and O(h) extra memory.
    """

    if root is None:
        return []
    order: list[T] = []
    stack: AlgorithmStack[tuple[TreeNode[T], bool]] = AlgorithmStack()
    stack.push((root, False))
    while not stack.is_empty:
        node, visited_children = stack.pop()
        if visited_children:
            order.append(node.data)
        else:
            stack.push((node, True))
            if node.right is not None:
                stack.push((node.right, False))
            if node.left is not None:
                stack.push((node.left, False))
    return order


def level_order(root: TreeNode[T] | None) -> list[T]:
    """Return nodes in breadth-first order.

    Cost
    ----
    Each node enqueued once: O(n) time. The queue holds at most one frontier:
    O(n) extra memory in the worst case (complete last level).
    """

    if root is None:
        return []
    order: list[T] = []
    queue: LinkedQueue[TreeNode[T]] = LinkedQueue()
    queue.enqueue(root)
    while not queue.is_empty:
        node = queue.dequeue()
        order.append(node.data)
        if node.left is not None:
            queue.enqueue(node.left)
        if node.right is not None:
            queue.enqueue(node.right)
    return order


def map_inorder(root: TreeNode[T] | None, visit: Callable[[T], None]) -> None:
    """Call ``visit`` on each value in sorted order for a BST.

    Cost
    ----
    Same as ``BinarySearchTree.inorder_iter``: O(n) time, O(h) stack memory.
    """

    stack: AlgorithmStack[TreeNode[T]] = AlgorithmStack()
    node = root
    while node is not None or not stack.is_empty:
        while node is not None:
            stack.push(node)
            node = node.left
        current = stack.pop()
        visit(current.data)
        node = current.right


def inorder_iter(root: TreeNode[T] | None) -> Iterator[T]:
    """Yield values in in-order sequence.

    Cost
    ----
    O(n) time, O(h) extra memory.
    """

    stack: AlgorithmStack[TreeNode[T]] = AlgorithmStack()
    node = root
    while node is not None or not stack.is_empty:
        while node is not None:
            stack.push(node)
            node = node.left
        current = stack.pop()
        yield current.data
        node = current.right
