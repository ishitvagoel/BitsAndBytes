---
title: Loop invariants
slug: loop-invariants
order: 29
status: present
module: bitsandbytes.complexity
---

## Explain why a loop is correct

A loop invariant is a statement that is true before an iteration and remains true after its update. It connects what the loop has processed to the answer the function promises.

**By the end of this overview, you can** state the initialization, preservation and termination checks used in a loop-correctness argument.

## Use three checks

For a running sum, a useful invariant is: after processing the first `i` values, `total` equals their sum. It is true before the loop because both sides are zero. Adding the next value preserves it. When `i` reaches the list length, the invariant says `total` is the sum of the whole list.

For binary search, the invariant is that if the target exists, it remains in the current candidate range. Each comparison discards only indexes proved too small or too large. Progress also matters: every update must shrink the range, or the loop may repeat forever even if its invariant remains true.

An invariant is not just a comment. It must match the initialization, every state change and the exit condition. If one of those does not support the statement, revise the algorithm or the invariant.

## Practice and next step

Write a one-sentence invariant for a loop that counts values greater than 10. Check it before the first iteration, after one update, and when the loop terminates. Continue to [arrays and Python sequence costs](./arrays-and-python-costs.md).
