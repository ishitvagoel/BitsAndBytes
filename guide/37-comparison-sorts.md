---
title: Comparison sorts
slug: comparison-sorts
order: 37
status: present
module: bitsandbytes.sorting.bubble_sort, bitsandbytes.sorting.insertion_sort, bitsandbytes.sorting.selection_sort
---

## The idea

A comparison sort decides order only by asking whether one key is less than another. Insertion sort keeps a sorted prefix and inserts the next key into it. Selection sort grows a sorted prefix by swapping the minimum of the suffix into place. Bubble sort walks neighbors and swaps inversions. All three are Θ(n²) in the worst case. They differ in the best case, in stability, and in how many writes they perform. Insertion sort on a sorted list is Θ(n) because each new key is already in place. The library function insertion_sort([3, 1, 2]) returns [1, 2, 3]. Python's list.sort uses Timsort, a stable merge sort. It is O(n log n) and it keeps runs that are already ordered.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Sorted | result = [1, 2, 3] | insertion_sort returns the sorted list. |

## Why it is correct

The insertion invariant is the sorted prefix from the loop-invariants lesson. After inserting 1, every item in the prefix is in order and every item outside it is still untouched. The next step considers 2 only against that prefix. Selection sort's invariant is different. The prefix holds the smallest items so far, in order, and the algorithm does not promise stability. Because a swap can move an equal key from the suffix in front of an equal key in the prefix. Knowing which invariant you have tells you which bugs are possible.

## What it costs

Worst-case time for these simple sorts is Θ(n²) comparisons. Insertion sort's best case is Θ(n). Extra memory is O(1) for the in-place versions. Merge sort, next, spends Θ(n) extra memory to bring the worst case down to Θ(n log n). The simple sorts are the right tool for tiny or nearly sorted prefixes, not for a large worst-case input.

On [3, 1, 2] insertion sort shifts once to place 1 and once to place 2. A reverse-sorted list of n items shifts about n² / 2 times. That is the worst case you are accepting if you call insertion sort on arbitrary input.

## Run it

```python
from bitsandbytes.sorting.insertion_sort import insertion_sort
print(insertion_sort([3, 1, 2]))
# prints: [1, 2, 3]
```

## Practice and next step

Answer the checkpoints, then open Merge sort. The checkpoint stays in this browser.
