---
title: Binary search tree operations
slug: binary-search-tree-operations
order: 46
status: present
module: bitsandbytes.trees.bst
---

## Keep smaller keys left and larger keys right

For each node in a binary search tree, keys in its left subtree are smaller and keys in its right subtree are larger under the tree's comparison rule. Search chooses one child after each comparison.

**By the end of this overview, you can** trace search and explain why operation cost depends on tree height.

Search, insert and delete each follow O(h) nodes for tree height `h`. A balanced tree has logarithmic height; inserting already sorted keys into an unbalanced tree can create height `n`, making an operation O(n). Deleting a node with two children replaces it with an adjacent ordered key, then removes that replacement from its original location.

An in-order traversal visits keys in sorted order. The ordering invariant is local to every node, so a broken link can violate order across an entire subtree.

## Practice and next step

Insert `4, 2, 6, 1, 3`, then trace search for 3. Delete node 2 and identify the replacement that preserves ordering. Compare with [the repository tree tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_trees.py) and continue to [tree traversals](./tree-traversals.md).
