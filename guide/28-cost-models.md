---
title: Cost models and assumptions
slug: cost-models
order: 28
status: present
module: bitsandbytes.complexity, bitsandbytes.library_costs
---

## State what counts as one step

A complexity claim depends on its model. The word-RAM model treats a fixed-width comparison, pointer write, and word-sized arithmetic operation as constant cost. That makes it useful for comparing common algorithms, but it is an assumption about the input representation.

**By the end of this overview, you can** state the assumptions behind a time bound and separate algorithmic work from Python container work.

## Apply the model to a real operation

Binary search uses O(log n) comparisons on an already sorted, random-access sequence when each comparison and index operation has constant cost. A linked list does not offer constant-time access to the middle, so the same comparison count does not imply O(log n) elapsed work there.

Python's list is a dynamic array. Reading `values[i]` uses direct indexing, while inserting near the front moves later references. A `deque` is designed for changes at both ends. Python's [`bisect` documentation](https://docs.python.org/3/library/bisect.html) explains that `insort` takes O(n) overall because insertion dominates its logarithmic search; [`deque`](https://docs.python.org/3/library/collections.html#collections.deque) documents approximately O(1) endpoint appends and pops.

Count the data structure operation your code actually performs. Do not call hashing constant-time for arbitrarily large keys without stating a key-size assumption, and count recursion stack separately from loop variables.

## Practice and next step

Explain why binary search is logarithmic on a list but not on a linked list. Then compare `list.pop(0)` with `deque.popleft()`. Continue to [loop invariants](./loop-invariants.md) to connect a cost count to a correctness argument.
