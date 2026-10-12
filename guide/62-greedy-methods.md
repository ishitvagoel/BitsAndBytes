---
title: Greedy methods
slug: greedy-methods
order: 62
status: present
module: bitsandbytes.greedy.classic
---

## The idea

Intervals (1, 3), (2, 4), and (3, 5) yield 2 compatible intervals.

A greedy algorithm makes a local choice and does not take it back. The choice needs an argument that some optimal solution agrees with it. interval_scheduling_max_count on (1, 3, a), (2, 4, b), and (3, 5, c) returns 2. The rule sorts by finish time and takes the next interval that starts at or after the previous finish. Interval a finishes first and is taken. b overlaps a and is skipped. c starts when a finishes and is taken. An example with three intervals does not prove the rule. The exchange argument does. Huffman coding is another greedy choice. huffman_codes on frequencies a 3, b 1, and c 1 gives a the code 1, the short code, because a is the frequent symbol. The two rare symbols share the longer branch. The library builds that tree by repeatedly combining the two lightest weights with a min-heap.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| take | count = 1 | Take interval a. The count is 1. |
| skip | count = 1 | Skip interval b. The count is 1. |
| take | count = 2 | Take interval c. The count is 2. |

## Why it is correct

Suppose an optimal schedule's first interval is not the one that finishes first. Swap it for the earliest-finishing interval. The swap stays feasible because that interval finishes even sooner, so everything that fit after the old first interval still fits. The count does not drop. Repeating the swap produces the greedy schedule without losing optimality. That is the proof. A single worked example only shows the rule on one input. The Huffman exchange argument says the two lightest symbols can be siblings in some optimal tree. Combining them and repeating builds the codes.

## A common mistake

One worked example is not a proof. The exchange argument is the proof.

## What it costs

Sorting the intervals is n log n, and the scan that follows is linear. Huffman does n heap operations, also n log n, and the output codes are linear in the number of symbols. Extra memory is the sorted copy or the heap. Do not quote the bound until you can say why the local choice is safe. A different sort key, such as shortest interval, needs its own argument or a counterexample. Sorting the intervals is Θ(n log n) time and uses Θ(n) extra memory.

## Run it

```python
from bitsandbytes.greedy.classic import interval_scheduling_max_count
print(interval_scheduling_max_count([(1, 3, 'a'), (2, 4, 'b'), (3, 5, 'c')]))
# prints: 2
```

## Practice and next step

Open Dynamic programming next. Dynamic programming stores a state so the same subproblem is solved once.
