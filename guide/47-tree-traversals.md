---
title: Tree traversals
slug: tree-traversals
order: 47
status: present
module: bitsandbytes.trees.traversals
---

## Visit each node in a chosen order

Preorder visits node, left, right; postorder visits left, right, node; in-order visits left, node, right. Level order visits all nodes at one depth before moving to the next.

**By the end of this overview, you can** trace a recursive traversal and explain why breadth-first level order needs a queue.

Every traversal processes each of `n` nodes once, so time is O(n). Depth-first traversal uses O(h) call-stack space for height `h`; level order may store O(w) nodes, where `w` is the maximum level width. An unbalanced tree can make `h = n`.

The visit order determines what information is available. In-order on a binary search tree yields sorted keys. Postorder visits children before a parent, which is useful when a result depends on completed child computations.

## Practice and next step

For root 4 with left child 2 and right child 6, write preorder, in-order, postorder and level order. See [the repository traversal tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_trees.py) and continue to [balanced search trees](./balanced-search-trees.md).
