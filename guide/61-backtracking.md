---
title: Backtracking search
slug: backtracking
order: 61
status: present
module: bitsandbytes.backtracking.search
---

## The idea

Backtracking searches a tree of choices. You choose, recurse, and undo so the next choice sees the earlier state. permutations of 1, 2, 3 returns six lists, one for every order. The first position has three choices. The second has two remaining items. The third has one. The product is 6, and the function materializes each list. The undo step puts the chosen item back into the pool before the next sibling is tried. Without the undo, the later branches would see a shrinking pool that is not restored. n_queens_count uses the same shape. A queen is placed, the search goes to the next row, and the placement is removed on the way back. Pruning skips a placement that already shares a column or a diagonal with a queen.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Leaves | count = 6 | Three distinct items have six permutations. |

## Why it is correct

The state invariant is that the pool, or the board, matches the choices on the path from the root to the current call, and nothing else. Choose extends that path. Recurse searches below it. Undo returns to the parent path. A leaf is a complete choice, and it is recorded before the undo. Every permutation appears once because each item is chosen into each position from the items not yet used. The search tree is exhaustive unless a prune deletes a branch. A prune is correct only when every leaf under that branch would fail the same test.

## What it costs

The permutation tree has n! leaves, and building each list copies n items, so the time is proportional to n times n!. Extra memory is the current path, which is n, plus the output. Pruning does not change the worst-case shape. It changes which branches you actually enter. Estimate the tree before you code the search. If the unpruned tree is already enormous, a different state is the real fix.

## Run it

```python
from bitsandbytes.backtracking.search import permutations
print(len(permutations([1, 2, 3])))
# prints: 6
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
