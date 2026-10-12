---
title: Binary search tree operations
slug: binary-search-tree-operations
order: 46
status: present
module: bitsandbytes.trees.bst
---

## The idea

Insert 4, then 2, then 6, then 1. The inorder walk is 1, 2, 4, 6.

A binary search tree node holds a key, a left child, and a right child. Every key in the left subtree is < the node's key, and every key in the right subtree is > it. Insert walks that rule until it finds an empty child, then hangs the new key there. Inserting 4, 2, 6, 1 puts 4 at the root, 2 on its left, 6 on its right, and 1 on the left of 2. The library's inorder walk visits left, node, right, so it returns [1, 2, 4, 6]. A duplicate key is ignored.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| root | parent = None | 4 becomes the root child of None. |
| left | parent = 4 | 2 becomes the left child of 4. |
| right | parent = 4 | 6 becomes the right child of 4. |
| left | parent = 2 | 1 becomes the left child of 2. |

## Why it is correct

The search invariant is that the target, if it exists, lies in the subtree still being walked. Going left throws away the node and its right subtree because those keys are ≥ the node and the target is smaller. Going right throws away the left subtree for the symmetric reason. Insert uses the same walk and writes the new node only at an empty child, so the parent comparison that led there is still true. Inorder returns sorted keys because it emits the whole left subtree, then the node, then the whole right subtree, and both subtrees are themselves ordered.

## A common mistake

The successor of a node with no right child is an ancestor, not the left child.

## What it costs

Each insert or lookup does one comparison per level, so the time is Θ(h) where h is the height. A balanced tree has h = Θ(log n). Inserting sorted keys makes a chain and h = n, so the same operations are Θ(n). The call in this library is a loop, so extra memory is O(1) besides the nodes. The nodes themselves are Θ(n). Deletion has the same height cost. The successor is the next inorder key, the leftmost node of the right subtree when a right child exists.

## Run it

```python
from bitsandbytes.trees.bst import BinarySearchTree
tree = BinarySearchTree()
for value in (4, 2, 6, 1):
    tree.insert(value)
print(tree.inorder())
# prints: [1, 2, 4, 6]
```

## Practice and next step

Open Tree traversals next. Traversals visit that same tree in preorder, postorder, and level order.
