---
title: Arrays and Python sequence costs
slug: arrays-and-python-costs
order: 30
status: present
module: bitsandbytes.library_costs
---

## The idea

A Python list is a dynamic array of references. Indexing list[i] is Θ(1) because the address is base + i times the reference size. append and pop() at the end are amortized Θ(1), which the next lesson counts. insert(0, x) and pop(0) move every later reference, so one call is Θ(n). A collections.deque stores blocks that can grow at either end, so append and popleft are Θ(1). Use a list when you need random access. Use a deque when both ends change and you do not need list[i] in the inner loop.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Before | length = 3 | b and c sit after a. |
| Shift | copies = 2 | b moves to index 0 and c moves to index 1. |
| After | length = 2 | The length is 2. One removal copied n - 1 references. |

## Why it is correct

The shift cost follows from the layout. If item i + 1 must occupy slot i, every index from 0 through n - 2 is written once. That is n - 1 writes, which is Θ(n). Nothing in CPython's list makes the front special. The overallocation that makes append cheap sits at the end, past the current length.

## What it costs

n front removals on a list copy about n + (n - 1) + ... + 1 references, which is Θ(n²). The same n removals on a deque are Θ(n) total. Random access on the deque is not the list's Θ(1) index. The choice is which operations the algorithm actually performs.

A worked check is n = 1000. One pop(0) moves about 999 references. Doing that once per item, to drain the list from the front, moves about half a million references. A deque draining the same list moves about 1000 nodes. The asymptotic symbols are the summary of that count. Indexing stays Θ(1) on the list either way, which is why a binary search later in the guide requires a list or another random-access sequence and not a linked chain.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
