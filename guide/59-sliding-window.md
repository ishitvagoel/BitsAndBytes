---
title: Sliding windows
slug: sliding-window
order: 59
status: present
module: bitsandbytes.patterns.arrays
---

## Reuse work between neighboring ranges

A sliding window represents a contiguous interval. Add the new right item and, while a constraint is broken, remove items from the left. The key proof obligation is that shrinking cannot discard a better feasible interval that the algorithm has not already measured.

## Know when the pattern applies

The standard variable window relies on a monotone feasibility condition: extending cannot restore validity after it is lost, or shrinking can restore validity in a predictable way. Negative values can invalidate familiar sum-window arguments.

## Practice

Trace the longest substring with at most k distinct values. Record the window, counts and best length after every expansion and contraction.

Source: [`arrays.py`](../bitsandbytes/patterns/arrays.py).
