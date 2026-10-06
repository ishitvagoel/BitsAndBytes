---
title: Two-pointer patterns
slug: two-pointers
order: 58
status: present
module: bitsandbytes.patterns.arrays
---

## Move pointers with a reason

Two pointers scan a sequence from opposite ends, at different speeds, or across two inputs. A correct scan needs a decision rule showing why the pointer that moves cannot skip a valid answer. Sorted order often supplies that rule.

## Count total work

If each pointer only moves forward or inward, the total number of moves is O(n), even when there is a nested-looking loop. State the invariant and the monotone movement before claiming linear time.

## Practice

Trace the inward scan for a target pair in a sorted array. At each comparison, justify which side can no longer participate in a solution.

Source: [`arrays.py`](../bitsandbytes/patterns/arrays.py).
