---
title: Binary search
slug: binary-search
order: 6
status: present
module: bitsandbytes.search.binary_search
---

## Find a value by ruling out half the list

**By the end of this lesson, you can** trace binary search, explain why each discarded index cannot contain the answer, handle a missing value and duplicate values, and distinguish the cost of searching from the cost of inserting.

**Before you start:** You should be comfortable reading a Python list, comparing values, and following `while` loops. No prior search-algorithm knowledge is required. Set aside about **15 minutes** for the explanation and practice.

## Start with a prediction

The numbers below are already sorted. You want to find `7`:

```text
index:  0  1  2  3  4
value:  1  3  5  7  9
```

If you inspect the middle value first, which indexes can you rule out after seeing that it is `5`?

Pause on your prediction, then use the trace controls below to check it and step through the search.

## The idea: keep only possible answers

Binary search needs values in sorted order and a way to access the middle position directly. Keep two indexes, `left` and `right`, for the still-possible range. At each step:

1. Choose the middle index of that range.
2. If its value is too small, keep only the part to its right.
3. If its value is too large, keep only the part to its left.
4. If neither comparison is true, the value matches.

The important invariant is: **if the target is in the sequence, it is somewhere in the current range**. Each comparison preserves that statement while making the range smaller.

## Trace the search

This implementation uses a closed, or inclusive, range: both `left` and `right` are possible indexes.

1. **Start:** `left = 0`, `right = 4`. The whole list, indexes 0 through 4, is possible.
2. **First comparison:** `middle = 2`, whose value is 5. Since `7 > 5`, set `left = middle + 1`. Indexes 3 through 4 remain possible.
3. **Second comparison:** `middle = 3`, whose value is 7. The target is found at index 3.

When the target is smaller than the middle value, set `right = middle - 1` instead. The middle index itself is excluded because its value has already been shown to be too large.

## Read the implementation

This is the repository’s actual inclusive-range `binary_search` function. The site inserts the marked function directly from `bitsandbytes/search/binary_search.py` during its build, so the displayed code follows the source implementation.

[[source-excerpt:binary-search]]

The loop condition is `left <= right` because a range containing exactly one index is still worth checking. If the range becomes empty (`left > right`), the target was not present, so the function returns `-1`.

The code uses two `<` comparisons instead of requiring values to support `<=`. If neither value is less than the other, they are equivalent for this search order and the function returns that index. The input must be non-decreasing under `<`.

### A different convention: half-open ranges

The repository’s `lower_bound` and `upper_bound` functions use a half-open range, `[left, right)`: include the left endpoint but exclude the right endpoint. They start with `right = len(values)`, so the range can represent the insertion point just after the last item. Their loop condition is `left < right`; when the indexes meet, that index is the answer. These bounds are useful, but mixing their loop condition or endpoint updates with the inclusive implementation above causes off-by-one errors.

## Missing values, duplicates and boundaries

- **Missing value:** For `[1, 3, 5, 7, 9]`, searching for `6` eventually makes the range empty and returns `-1`.
- **One item:** `[8]` searching for `8` checks index 0 once. Searching for `2` checks it once and returns `-1`.
- **Empty input:** With `[]`, `right` starts at `-1`; `0 <= -1` is false, so the result is `-1` without indexing the list.
- **Duplicates:** `binary_search` may return any matching index. Use bounds when you need the full matching interval. In `[1, 2, 2, 2, 3]`, `lower_bound(..., 2)` is 1 and `upper_bound(..., 2)` is 4. The number of matches is `4 - 1 = 3`.

The corresponding cases are covered by the repository’s [binary-search tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py).

## Why the search takes logarithmic time

Suppose there are `n` candidates. After one comparison there are at most `n/2`; after two, at most `n/4`. After `k` comparisons, at most `n / 2^k` remain. The range is empty or has one candidate once `2^k` is at least `n`, which takes about `log₂(n)` comparisons. Therefore search takes **O(log n)** time and stores only a few indexes, so it uses **O(1)** extra space.

This analysis assumes the sequence is already sorted, comparisons take constant time, and indexing reaches a middle element in constant time, as it does for a Python list. Sorting first has its own cost and is not included. Binary search on a linked list does not get the same time bound because reaching each middle position requires traversal.

Finding an insertion point is also logarithmic with Python’s [`bisect`](https://docs.python.org/3/library/bisect.html) module. Inserting into the middle of a Python list is still **O(n)** in the worst case: later elements need to shift to make room. Thus `bisect.insort` is O(n) overall even though its search step is O(log n).

## Practice: predict, debug and transfer

Use the checkpoint cards below to make a prediction, diagnose a non-shrinking range, transfer the bounds idea to duplicates, and explain why searching for an insertion point does not make list insertion logarithmic. Each response includes feedback explaining the reasoning.

## Next step

Try tracing a target that is absent and explain why every discarded index is impossible. Then continue to [binary search on an answer](./binary-search-on-answer.md) to apply the shrinking-range idea to a monotone yes/no condition, followed by [sorting](./05-sorting.md).
