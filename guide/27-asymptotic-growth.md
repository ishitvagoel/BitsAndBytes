---
title: Asymptotic growth
slug: asymptotic-growth
order: 27
status: present
module: bitsandbytes.complexity
---

## The idea

At n = 64, n log2 n is 384 and n squared is 4096.

An exact count such as 3n + 20 is useful, and it is also more precise than the decision you usually need. Big O, Θ, and Ω compare growth. O(f) says the work is at most a constant times f for large n. Ω(f) says it is at least a constant times f. Θ(f) says both, so f is a tight description. 3n + 20 is Θ(n) because (3n + 20) / n approaches 3. It is also O(n²), since a looser upper bound is still true, but Θ(n²) is false. When you write a cost in this guide, prefer the tight bound and say so.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| n=4 | n = 4 | At n = 4, n log2 n is 8 and n squared is 16. |
| n=16 | n = 16 | At n = 16, n log2 n is 64 and n squared is 256. |
| n=64 | n = 64 | At n = 64, n log2 n is 384 and n squared is 4096. |
| n=256 | n = 256 | At n = 256, n log2 n is 2048 and n squared is 65536. |

## Why it is correct

The limit test is the reason the constant and the added 20 disappear. For any fixed c, (cn + d) / n approaches c. A function is Θ(n) when two positive constants sandwich it between multiples of n for all large n. 3n + 20 sits between 3n and 4n once n is at least 20. It does not sit between two multiples of n², because (3n + 20) / n² approaches 0.

## A common mistake

A looser upper bound is still true, so O(n squared) does not mean the tight bound is n squared.

## What it costs

Using the notation does not change the algorithm. It changes the claim. A Θ(n) scan of a million items is a different engineering choice from a Θ(n²) pair scan of the same list. The trace shows n squared pulling away from n log n as n leaves the toy range. Comparing the formulas uses O(1) extra memory.

Write the exact count first, as the previous lesson did for pairs. Only then replace it with Θ. If you start from Θ you can hide a bug such as an extra nested loop. The notation is a compression step, not a substitute for the count.

## Run it

```python
from bitsandbytes.complexity import growth_table
print(growth_table((64,))[0])
# prints: (64, 384, 4096)
```

## Practice and next step

Open Cost models and assumptions next. Cost models ask which Python operation that bound is actually counting.
