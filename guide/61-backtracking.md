---
title: Backtracking search
slug: backtracking
order: 61
status: present
module: bitsandbytes.backtracking.search
---

## Explore choices with reversible state

Backtracking builds a partial solution, tries a valid choice, recurses, then undoes that choice. The recursion tree captures the work: permutations have n! leaves, while subsets have 2ⁿ leaves before accounting for work at each node.

## Prune only impossible branches

A pruning rule is correct only when it proves no completion below the current state can succeed. Keep the base case, choice set, state update and undo paired so sibling branches start from the same state.

## Practice

Trace subset generation and identify which state is copied versus mutated. Then count leaves for an input of size n.

Source: [`search.py`](../bitsandbytes/backtracking/search.py).
