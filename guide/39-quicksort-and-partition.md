---
title: Quicksort and partition
slug: quicksort-and-partition
order: 39
status: present
module: bitsandbytes.sorting.quick_sort
---

## The idea

Quicksort picks a pivot, partitions the range so every value before the pivot is ≤ the pivot and every value after it is > the pivot, and then sorts the two sides. The library's partition swaps the chosen pivot to the end and scans once. boundary is the next slot that should receive a value ≤ pivot. For pivot 2 at the end of [3, 1, 4, 2], the scan swaps 1 to index 0 and then swaps 2 into index 1, leaving [1, 2, 4, 3]. The recursive calls sort the two sides. quick_sort on this input returns [1, 2, 3, 4]. The pivot index itself is random unless you pass a Random instance.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Pivot at end | pivot = 2, boundary = 0 | 2 is the pivot. The boundary starts at 0. |
| See 3 | boundary = 0 | 3 > 2, so the boundary stays 0. |
| See 1 | boundary = 1 | 1 ≤ 2. Swap it with the boundary and advance. |
| Place pivot | pivot index = 1 | 4 > 2, so it stays. Swap the pivot into index 1. |

## Why it is correct

The partition invariant is that every index before boundary holds a value ≤ pivot, and every index from boundary to the scan cursor holds a value > pivot. It is true before the scan because that region is empty. Seeing a value > pivot extends the right region without moving boundary. Seeing a value ≤ pivot swaps it into the boundary slot and advances the boundary, which restores the invariant. The final swap puts the pivot at boundary. Everything before it is ≤ pivot and everything after it is > pivot, so the pivot is in its final sorted index.

## What it costs

One partition of k items is Θ(k) time and O(1) extra memory. If every pivot splits off one item, the recurrence is T(n) = T(n - 1) + Θ(n), which is Θ(n²), and the call stack is Θ(n) deep. Balanced pivots give T(n) = 2 T(n/2) + Θ(n), which is Θ(n log n) time and Θ(log n) stack. The sort is not stable, because the swaps move equal keys past each other. A three-way partition gathers equals in the middle so a run of duplicate keys does not fall into the n² case.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
