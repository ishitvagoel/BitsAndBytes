---
title: Comparison sorts
slug: comparison-sorts
order: 37
status: present
module: bitsandbytes.sorting.bubble_sort, bitsandbytes.sorting.insertion_sort, bitsandbytes.sorting.selection_sort
---

## The idea

insertion_sort on [3, 1, 2] writes [1, 3, 2] and then [1, 2, 3].

A comparison sort decides order only by asking whether one key is less than another. Insertion sort keeps a sorted prefix and inserts the next key into it. On a sorted list each new key is already in place, so the best case is Θ(n). The worst case is still Θ(n²). The library function insertion_sort([3, 1, 2]) returns [1, 2, 3]. Python's list.sort uses Timsort. It is O(n log n) and it keeps runs that are already ordered.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| start | list = [3, 1, 2] | The input is 3, 1, 2. Nothing is inserted yet. |
| insert | list = [1, 3, 2] | Inserted 1. The list is now [1, 3, 2]. |
| insert | list = [1, 2, 3] | Inserted 2. The list is now [1, 2, 3]. |

## Why it is correct

The insertion invariant is the sorted prefix from the loop-invariants lesson. After inserting 1, every item in the prefix is in order and every item outside it is still untouched. The next step considers 2 only against that prefix. Selection sort is a different invariant, covered here only as a cost comparison. Its prefix holds the smallest items so far, and a swap can move an equal key past another equal key.

## A common mistake

A strict less-than does not swap equal keys. Calling the sort unstable is the wrong claim.

## What it costs

Worst-case time for insertion sort is Θ(n²) comparisons. The best case is Θ(n). Extra memory is O(1). Selection sort and bubble sort share the Θ(n²) worst case and also use O(1) extra memory. Merge sort, next, spends Θ(n) extra memory to bring the worst case down to Θ(n log n).

On [3, 1, 2] insertion sort shifts once to place 1 and once to place 2. A reverse-sorted list of n items shifts about n² / 2 times. That is the worst case you are accepting if you call insertion sort on arbitrary input.

## Run it

```python
from bitsandbytes.sorting.insertion_sort import insertion_sort
print(insertion_sort([3, 1, 2]))
# prints: [1, 2, 3]
```

## Practice and next step

Open Merge sort next. Merge sort keeps that stability and brings the worst case down to n log n.
