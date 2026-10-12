---
title: Balanced search trees
slug: balanced-search-trees
order: 48
status: present
module: bitsandbytes.trees.llrb
---

## The idea

Inserting 1, then 2, then 3 leaves 2 at the root. Inorder is still 1, 2, 3.

A plain binary search tree becomes a chain when keys arrive in sorted order. Every operation then walks n nodes. A balanced tree keeps the height logarithmic by local rotations. The library's left-leaning red-black tree encodes a 2-3 tree. A red link to a left child means two keys share a node. Right-leaning red links are rotated away. Insert 1, then 2, then 3. The inorder walk is 1, 2, 3, so the search-tree order survives. The root key is 2, not 3, so the tree did not become a chain. select(1) returns 2, the second smallest key. rank(2) returns 1, the number of keys strictly smaller than 2. Those order statistics come from subtree sizes stored on the nodes.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Insert | root = 1 | After inserting 1, the root is 1. Inorder is [1]. |
| Insert | root = 2 | After inserting 2, the root is 2. Inorder is [1, 2]. |
| Insert | root = 2 | After inserting 3, the root is 2. Inorder is [1, 2, 3]. |

## Why it is correct

A rotation changes which node is the parent and which is the child. It does not change inorder. The keys that were left of a node stay left, and the keys that were right stay right. Only the shape moves. The red-black rules limit how many black links appear on a path from the root to a leaf. A red link cannot simply stack on another red link. That bound is why the height stays logarithmic after the sorted inserts. select walks by subtree size. If the left subtree holds more than k keys, the answer is in the left subtree. Otherwise it is the node itself or a key in the right subtree.

## A common mistake

A rotation changes the parent. It does not reverse inorder.

## What it costs

Insert, delete, rank, and select are logarithmic because the height is logarithmic. A rotation is a constant number of pointer writes. Extra memory is one node per key, plus the color and the size. The plain search tree uses the same memory and loses the height bound. Use the balanced tree when the input order is not under your control and later lookups must stay fast. Insert is Θ(log n) time, and the nodes use Θ(n) extra memory.

## Run it

```python
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree
tree = LeftLeaningRedBlackTree()
for value in (1, 2, 3):
    tree.insert(value)
print(tree.inorder())
# prints: [1, 2, 3]
```

## Practice and next step

Open Heap operations next. Heap operations expose the extreme key without sorting the whole array.
