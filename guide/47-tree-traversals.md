---
title: Tree traversals
slug: tree-traversals
order: 47
status: present
module: bitsandbytes.trees.traversals
---

## The idea

A traversal is a rule for the order in which you visit nodes. The same tree produces different sequences under different rules. Build the binary search tree by inserting 4, then 2, then 6, then 1. preorder visits a node before either child and returns 4, 2, 1, 6. postorder visits both children before the node and returns 1, 2, 6, 4. The inorder walk, left then node then right, returns 1, 2, 4, 6. Which is the sorted order only because the tree is a search tree. level_order uses a queue. It returns 4, 2, 6, 1. The root leaves first. Its children are enqueued left then right, so 2 is ahead of 6, and 1 waits behind them. Depth-first walks use a stack, or the call stack. Breadth-first walks use a queue. The container is the difference.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Preorder | root = 4 | Visit the node before either child. |
| Levels | root = 4 | A queue visits each depth before the next. |

## Why it is correct

Preorder is correct by induction on the tree. The first value is the root. The next values are the preorder of the left subtree, then the preorder of the right subtree. Postorder appends the root after both recursive sequences. Level order is the queue lesson again. A node is enqueued when its parent is visited. So every node at depth d enters the queue before any node at depth d + 1 is dequeued. Marking is unnecessary on a tree because there is one path from the root and no edge back to an ancestor.

## What it costs

Each walk visits every node once and looks at every child link once, so the time is linear in the number of nodes. The call stack of a skewed preorder is linear. A balanced tree keeps that stack logarithmic. The level-order queue holds one level at a time. Can hold about half the nodes of a wide level, so extra memory is linear in the worst case. Use inorder when you want the sorted keys. Use level order when the depth itself is the question.

## Run it

```python
from bitsandbytes.trees.bst import BinarySearchTree
from bitsandbytes.trees.traversals import preorder
tree = BinarySearchTree()
for value in (4, 2, 6, 1):
    tree.insert(value)
print(preorder(tree.root))
# prints: [4, 2, 1, 6]
```

## Practice and next step

Answer the checkpoints, then open Balanced search trees. The checkpoint stays in this browser.
