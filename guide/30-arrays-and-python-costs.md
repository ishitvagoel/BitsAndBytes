---
title: Arrays and Python sequence costs
slug: arrays-and-python-costs
order: 30
status: present
module: bitsandbytes.library_costs
---

## The idea

One pop(0) on 4 items slides 3 references.

A Python list is a dynamic array of references. Indexing list[i] is Θ(1) because the address is base + i times the reference size. append and pop() at the end are cheap on average, which the next lesson counts. insert(0, x) and pop(0) move every later reference, so one call is Θ(n). A collections.deque stores blocks that can grow at either end, so append and popleft are Θ(1). Use a list when you need random access. Use a deque when both ends change and you do not need list[i] in the inner loop.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Start | moved = 0 | Front removal has slid 0 references toward index 0. |
| Slide | moved = 1 | Front removal has slid 1 references toward index 0. |
| Slide | moved = 2 | Front removal has slid 2 references toward index 0. |

## Why it is correct

The shift cost follows from the layout. If item i + 1 must occupy slot i, every index from 0 through n - 2 is written once. That is n - 1 writes, which is Θ(n). Nothing in CPython's list makes the front special. The overallocation that makes append cheap sits at the end, past the current length.

## A common mistake

The cheap end of a Python list is the last index, not index 0.

## What it costs

n front removals on a list copy about n + (n - 1) + ... + 1 references, which is Θ(n²). The same n removals on a deque are Θ(n) total. Random access on the deque is not the list's Θ(1) index. The choice is which operations the algorithm actually performs. The list block uses Θ(n) extra memory for n references.

A worked check is n = 1000. One pop(0) moves about 999 references. Doing that once per item moves about half a million references. A deque draining the same list moves about 1000 nodes. The asymptotic symbols summarize that count. Indexing stays Θ(1) on the list either way. A later binary search needs a random-access sequence, not a linked chain.

## Run it

```python
from bitsandbytes.library_costs import list_pop_front_cost_demo
print(list_pop_front_cost_demo(1000))
# prints: 999
```

## Practice and next step

Open Dynamic-array growth next. Dynamic-array growth explains why append at that cheap end stays cheap on average.
