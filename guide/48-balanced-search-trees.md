---
title: Balanced search trees
slug: balanced-search-trees
order: 48
status: present
module: bitsandbytes.trees.llrb
---

## Keep height logarithmic as keys change

Balancing rules prevent a search tree from becoming a long chain. A left-leaning red-black tree encodes a balanced multiway tree using link colors and local rotations.

**By the end of this overview, you can** explain why the balancing invariant protects logarithmic search, insert and delete operations.

Red links represent connections within a 3-node. The implementation keeps red links leaning left, avoids consecutive red links, and balances black height from root to leaves. Rotations and color flips repair these properties after updates. With height O(log n), operations that follow one root-to-leaf path take O(log n).

The balancing invariant is more important than memorizing rotation code: after a local repair, the subtree must still contain the same ordered keys and satisfy the color/height rules. Rank and select use subtree sizes to find positions in logarithmic time.

## Practice and next step

Insert keys 1 through 5 in order into an ordinary BST and compare its height with a balanced tree. Then name which invariant a left rotation repairs. See [the repository balanced-tree tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_trees_extended.py).
