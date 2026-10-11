---
title: Sliding windows
slug: sliding-window
order: 59
status: present
module: bitsandbytes.patterns.arrays
---

## The idea

A sliding window is a contiguous slice that moves across the input. You keep a fact about the slice and update it when the slice grows or shrinks, instead of recomputing from scratch. sliding_window_maximum on 1, 3, 2, 5 with window 2 returns 3, 3, 5. A deque stores indexes of candidates. The front is the index of the current maximum. A new value pops the candidates it beats, because they are smaller and older. So they cannot be the maximum of this window or a later one. An index that falls off the left of the window is popped from the front. longest_unique_substring_length on abcabcbb returns 3. The window grows on the right and shrinks on the left whenever a repeated character enters. Both ends move only forward.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Windows | window = 2 | Each window of length 2 reports its maximum. |

## Why it is correct

The deque stays decreasing in value. The front is therefore the maximum of the indexes that are still inside the window. Popping a smaller tail preserves that order. Dropping an index that is left of the window preserves the window bounds. The unique-substring window's invariant is that every character inside it appears once. When a new character repeats one inside the window, the left end advances past that earlier copy. The length of the window after each step is a candidate for the answer. The maximum of those lengths is 3.

## What it costs

Each index enters and leaves the deque at most once, so the window maximum is linear time. The deque uses linear extra memory in the worst case. The unique-substring scan is also linear because both ends move forward at most n steps. A fresh scan of each window would be quadratic. The monotonicity you need is the decreasing candidate list, or the fact that the left end never needs to move backward. If the predicate is not of that shape, the window method does not apply.

## Run it

```python
from bitsandbytes.patterns.arrays import sliding_window_maximum
print(sliding_window_maximum([1, 3, 2, 5], 2))
# prints: [3, 3, 5]
```

## Practice and next step

Answer the checkpoints, then open Prefix sums. The checkpoint stays in this browser.
