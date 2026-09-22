"""Left-leaning red-black tree (2-3 tree encoding).

A red edge to the left child represents a 3-node: two keys share one left
link. The tree stays left-leaning (no right-leaning red edge) so every
insert or delete needs only O(log n) rotations along one root-to-leaf path.

Subtree sizes on each node support order statistics: ``rank`` counts keys
strictly smaller than a value; ``select(k)`` returns the k-th smallest key.

Worked trace (insert 1, 2, 3 in order):

* Insert 1: single black node.
* Insert 2: red link 1→2, rotate left so 2 is root, black, with red child 1.
* Insert 3: temporary right red under 2, color flip and rotation restore LLRB.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

RED = True
BLACK = False


@dataclass(eq=False)
class LLRBNode(Generic[T]):
    """One node with color and subtree size."""

    key: T
    color: bool = RED
    size: int = 1
    left: LLRBNode[T] | None = None
    right: LLRBNode[T] | None = None


class LeftLeaningRedBlackTree(Generic[T]):
    """Ordered set with O(log n) insert, delete, rank, and select."""

    def __init__(self) -> None:
        """Create an empty tree.

        Cost
        ----
        O(1).
        """

        self.root: LLRBNode[T] | None = None

    def __len__(self) -> int:
        """Return the number of keys.

        Cost
        ----
        O(1) if the root exists; otherwise 0.
        """

        return 0 if self.root is None else self.root.size

    def contains(self, key: T) -> bool:
        """Return whether ``key`` is stored.

        Cost
        ----
        O(log n) comparisons on a tree of n keys.
        """

        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return True
        return False

    def insert(self, key: T) -> None:
        """Insert ``key`` if absent.

        Cost
        ----
        One root-to-leaf walk with O(log n) rotations and color flips.
        Each ``_balance`` is O(1). Total O(log n) time, O(log n) call-stack
        memory recursively (O(1) if rewritten iteratively).
        """

        self.root = self._insert(self.root, key)
        if self.root is not None:
            self.root.color = BLACK

    def delete(self, key: T) -> bool:
        """Remove ``key`` if present.

        Cost
        ----
        Same O(log n) bound as insert along one path.
        """

        if self.root is None:
            return False
        if not self._is_red(self.root.left) and not self._is_red(self.root.right):
            self.root.color = RED
        removed = False
        if key < self.root.key:
            self.root, removed = self._delete_min_side(self.root, key)
        else:
            if self._is_red(self.root.left) and self.root.left is not None and key < self.root.left.key:
                self.root = self._rotate_right(self.root)
            if self.root.key == key:
                if self.root.right is None:
                    self.root = self.root.left
                    removed = True
                else:
                    successor = self._min_node(self.root.right)
                    assert successor is not None
                    self.root.key = successor.key
                    self.root.right, removed = self._delete_min(self.root.right)
            else:
                if self._is_red(self.root.right) and self.root.right.left is None:
                    self.root.right.color = BLACK
                self.root.right, removed = self._delete(self.root.right, key)
        if self.root is not None:
            self.root.color = BLACK
        return removed

    def rank(self, key: T) -> int:
        """Return the number of stored keys strictly less than ``key``.

        Cost
        ----
        O(log n) by walking and reading cached ``size`` fields.
        """

        return self._rank(self.root, key)

    def select(self, index: int) -> T:
        """Return the ``index``-th smallest key (0-based).

        Cost
        ----
        O(log n) using subtree sizes.
        """

        if index < 0 or index >= len(self):
            raise IndexError("select index out of range")
        return self._select(self.root, index)

    def inorder(self) -> list[T]:
        """Return keys in sorted order.

        Cost
        ----
        O(n) time, O(n) output memory.
        """

        output: list[T] = []
        self._inorder(self.root, output)
        return output

    def _insert(self, node: LLRBNode[T] | None, key: T) -> LLRBNode[T]:
        if node is None:
            return LLRBNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif node.key < key:
            node.right = self._insert(node.right, key)
        else:
            return node
        node = self._balance(node)
        self._refresh_size(node)
        return node

    def _delete(self, node: LLRBNode[T] | None, key: T) -> tuple[LLRBNode[T] | None, bool]:
        if node is None:
            return None, False
        if key < node.key:
            if node.left is not None and not self._is_red(node.left) and not self._is_red(node.left.left):
                node = self._move_red_left(node)
            node.left, removed = self._delete(node.left, key)
        else:
            if self._is_red(node.left):
                node = self._rotate_right(node)
            if node.key == key and node.right is None:
                return None, True
            if node.right is not None and not self._is_red(node.right) and not self._is_red(node.right.left):
                node = self._move_red_right(node)
            removed = False
            if node.key == key:
                successor = self._min_node(node.right)
                assert successor is not None
                node.key = successor.key
                node.right, removed = self._delete_min(node.right)
            else:
                node.right, removed = self._delete(node.right, key)
        if node is not None:
            node = self._balance(node)
            self._refresh_size(node)
        return node, removed

    def _delete_min_side(self, node: LLRBNode[T], key: T) -> tuple[LLRBNode[T], bool]:
        if node.left is not None and not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)
        node.left, removed = self._delete(node.left, key)
        if node.left is None and removed:
            return node, removed
        node = self._balance(node)
        self._refresh_size(node)
        return node, removed

    def _delete_min(self, node: LLRBNode[T]) -> tuple[LLRBNode[T] | None, bool]:
        if node.left is None:
            return node.right, True
        if not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)
        node.left, removed = self._delete_min(node.left)
        node = self._balance(node)
        self._refresh_size(node)
        return node, removed

    def _rank(self, node: LLRBNode[T] | None, key: T) -> int:
        if node is None:
            return 0
        if key <= node.key:
            return self._rank(node.left, key)
        left_size = 0 if node.left is None else node.left.size
        return left_size + 1 + self._rank(node.right, key)

    def _select(self, node: LLRBNode[T] | None, index: int) -> T:
        assert node is not None
        left_size = 0 if node.left is None else node.left.size
        if index < left_size:
            return self._select(node.left, index)
        if index == left_size:
            return node.key
        return self._select(node.right, index - left_size - 1)

    def _inorder(self, node: LLRBNode[T] | None, output: list[T]) -> None:
        if node is None:
            return
        self._inorder(node.left, output)
        output.append(node.key)
        self._inorder(node.right, output)

    def _min_node(self, node: LLRBNode[T]) -> LLRBNode[T] | None:
        while node.left is not None:
            node = node.left
        return node

    def _is_red(self, node: LLRBNode[T] | None) -> bool:
        return node is not None and node.color == RED

    def _size(self, node: LLRBNode[T] | None) -> int:
        return 0 if node is None else node.size

    def _refresh_size(self, node: LLRBNode[T]) -> None:
        node.size = 1 + self._size(node.left) + self._size(node.right)

    def _rotate_left(self, node: LLRBNode[T]) -> LLRBNode[T]:
        child = node.right
        assert child is not None
        node.right = child.left
        child.left = node
        child.color = node.color
        node.color = RED
        self._refresh_size(node)
        self._refresh_size(child)
        return child

    def _rotate_right(self, node: LLRBNode[T]) -> LLRBNode[T]:
        child = node.left
        assert child is not None
        node.left = child.right
        child.right = node
        child.color = node.color
        node.color = RED
        self._refresh_size(node)
        self._refresh_size(child)
        return child

    def _flip_colors(self, node: LLRBNode[T]) -> None:
        node.color = RED
        if node.left is not None:
            node.left.color = not node.left.color
        if node.right is not None:
            node.right.color = not node.right.color

    def _move_red_left(self, node: LLRBNode[T]) -> LLRBNode[T]:
        self._flip_colors(node)
        if node.right is not None and self._is_red(node.right.left):
            node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)
            self._flip_colors(node)
        return node

    def _move_red_right(self, node: LLRBNode[T]) -> LLRBNode[T]:
        self._flip_colors(node)
        if node.left is not None and self._is_red(node.left.left):
            node = self._rotate_right(node)
            self._flip_colors(node)
        return node

    def _balance(self, node: LLRBNode[T]) -> LLRBNode[T]:
        if node.right is not None and self._is_red(node.right):
            node = self._rotate_left(node)
        if node.left is not None and self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)
        if node.left is not None and node.right is not None and self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(node)
        self._refresh_size(node)
        return node
