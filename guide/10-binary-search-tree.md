---
title: Binary search tree
slug: binary-search-tree
order: 10
status: present
module: bitsandbytes.trees.bst, bitsandbytes.trees.traversals, bitsandbytes.trees.llrb
---

* `trees/bst.py` — insert, search, delete, and in-order walk. O(h) per operation for height h.
* `trees/traversals.py` — preorder, postorder, and level order in O(n) time.
* `trees/llrb.py` — left-leaning red-black tree with `rank` and `select` in O(log n).

## Industry

A working engineer reaches for a B-tree when keys must answer equality and
range comparisons. PostgreSQL's index documentation says `CREATE INDEX`
builds a B-tree by default, and that a B-tree handles `<`, `<=`, `=`, `>=`,
and `>`. The binary search tree in this lesson is that comparison walk in
memory. Sorted insertion makes its height linear, which is why the
left-leaning red-black tree keeps the height logarithmic.
