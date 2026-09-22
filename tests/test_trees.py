"""Binary search tree."""

from bitsandbytes.trees import BinarySearchTree


def test_bst_insert_contains_and_inorder() -> None:
    tree: BinarySearchTree[int] = BinarySearchTree()
    for value in (5, 2, 8, 1, 3):
        tree.insert(value)
    assert tree.contains(3)
    assert not tree.contains(10)
    assert tree.inorder() == [1, 2, 3, 5, 8]
