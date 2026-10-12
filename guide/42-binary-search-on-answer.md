---
title: Binary search on a feasible answer
slug: binary-search-on-answer
order: 42
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## Find a boundary by asking a yes-or-no question

Sometimes the answer is not an item in a sorted list. Instead, you can test a candidate answer: “If the machine works at this rate, can it finish on time?” When those yes/no results change only once across an ordered range, binary search can locate the boundary.

**By the end of this lesson, you can** state the monotonicity condition, trace a smallest-feasible search, and multiply the number of feasibility checks by the cost of one check.

**Before you start:** You should be able to follow the `left`, `right` and midpoint updates in [binary search](./06-binary-search.md). Work through the trace and the checks.

## Make the decision monotone

Suppose four piles contain `[3, 6, 7, 11]` items. A machine processes one pile at a time and works at a fixed positive rate for one hour on each pile. What is the smallest integer rate that finishes in at most eight hours?

For a candidate rate `r`, the hours needed for a pile of size `p` are `ceil(p / r)`. Add those hours over all piles. A rate is feasible if the total is at most eight.

If a rate is feasible, every faster rate is also feasible. If a rate is too slow, every slower rate is also infeasible. The answers therefore look like `false, false, ..., true, true`; finding the first `true` is a boundary search.

This one-change pattern is the required **monotonicity condition**. If feasible and infeasible candidates alternate, rejecting half the range is not justified: the discarded half could still contain the first feasible answer.

## Keep the first feasible rate in range

Let `low` be the smallest rate still possible and `high` a rate already known to be feasible. Maintain the invariant: **the smallest feasible rate is somewhere in the inclusive interval `[low, high]`, and `high` is feasible**.

The largest pile size is a feasible upper bound when the number of available hours is at least the number of piles: at that rate every pile takes one hour. If fewer hours than piles are available, no rate can finish the work under these rules.

At the midpoint, a feasible rate may be the answer, so the library records it and sets `high = middle - 1`. An infeasible midpoint and every slower rate are too small, so set `low = middle + 1`. Both updates preserve the invariant and make the interval smaller.

| `low` | `high` | `middle` | Hours at `middle` | Decision | Next range |
|---:|---:|---:|---:|---|---|
| 1 | 11 | 6 | 6 | Feasible | high = 5 |
| 1 | 5 | 3 | 10 | Too slow | low = 4 |
| 4 | 5 | 4 | 8 | Feasible | high = 3 |

The answer is 4. The library tested 6, then 3, then 4. A feasible midpoint does not end the search: a smaller rate may also work.

## Connect the boundary to code and cost

`binary_search_on_answer` keeps an `answer` variable and sets `high = middle - 1` when a rate is feasible.

```python
from bitsandbytes.sorting.selection_and_radix import binary_search_on_answer

def hours_needed(piles: list[int], rate: int) -> int:
    return sum((pile + rate - 1) // rate for pile in piles)

piles = [3, 6, 7, 11]
answer = binary_search_on_answer(1, max(piles), lambda rate: hours_needed(piles, rate) <= 8)
print(answer)
# prints: 4
```

Each feasibility check visits `p` piles, so it costs O(p) time. The interval contains at most `M` rates, where `M` is the largest pile. Binary search makes O(log M) checks, for O(p log M) time and O(1) extra space beyond the input. The check is not free: if one feasibility test costs more, multiply that cost by the number of candidate rates tested.

The library raises ValueError when no rate in the range is feasible. If the problem changes, revisit both the feasibility predicate and the invariant before reusing the search.

## A common mistake

A feasible rate is not automatically the answer. Rate 6 finishes early, and the search still has to test slower rates. Stopping at the first feasible midpoint returns a rate that works and misses the smallest one.

## Practice and check the reasoning

For the four piles above and eight hours, predict rate 3, then rate 6, then rate 4. The library tests them in the order 6, 3, 4.

**Check your work:** Rate 6 takes 6 hours, so it is feasible and the high bound becomes 5. Rate 3 takes 10 hours, so it is too slow and the low bound becomes 4. Rate 4 takes 8 hours, so it is feasible and it is the smallest such rate.

Now change the deadline to three hours. There are four positive piles and at least one hour is required per pile, so no candidate rate is feasible. The library raises ValueError on that search.

Compare this problem with [binary search in a sorted list](./06-binary-search.md): one searches stored values, while the other searches the ordered answers to a monotone decision. The [repository implementation and tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py) provide related search examples.
