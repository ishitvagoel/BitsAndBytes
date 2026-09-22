"""Tree traversals and BST deletion."""

from bitsandbytes.trees import BinarySearchTree, TreeNode
from bitsandbytes.trees.traversals import level_order, postorder, preorder


def _tree() -> TreeNode[int]:
    tree: BinarySearchTree[int] = BinarySearchTree()
    for value in (4, 2, 6, 1, 3, 5, 7):
        tree.insert(value)
    assert tree.root is not None
    return tree.root


def test_bst_delete_cases() -> None:
    tree: BinarySearchTree[int] = BinarySearchTree()
    for value in (2, 1, 3):
        tree.insert(value)
    assert tree.delete(1)
    assert tree.inorder() == [2, 3]
    assert not tree.delete(9)
    tree.insert(1)
    assert tree.delete(2)
    assert tree.inorder() == [1, 3]


def test_traversals_on_sample_tree() -> None:
    root = _tree()
    assert preorder(root) == [4, 2, 1, 3, 6, 5, 7]
    assert postorder(root) == [1, 3, 2, 5, 7, 6, 4]
    assert level_order(root) == [4, 2, 6, 1, 3, 5, 7]
