---
title: Asymptotic growth
slug: asymptotic-growth
order: 27
status: present
module: bitsandbytes.complexity
---

## The idea

An exact count such as 3n + 20 is useful, and it is also more precise than the decision you usually need. Big O, Θ, and Ω compare growth. O(f) says the work is at most a constant times f for large n. Ω(f) says it is at least a constant times f. Θ(f) says both, so f is a tight description. 3n + 20 is Θ(n) because (3n + 20) / n approaches 3. It is also O(n²), since a looser upper bound is still true, but Θ(n²) is false. When you write a cost in this guide, prefer the tight bound and say so.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| n = 4 | n = 4, n log2 n = 8, n² = 16 | Linear is still the smallest, but the three are close. |
| n = 16 | n = 16, n log2 n = 64, n² = 256 | n² is already 256. n log2 n is 64. |
| n = 1024 | n = 1024, n log2 n = 10240, n² = 1048576 | The quadratic count is about a million. The linear count is still 1024. |

## Why it is correct

The limit test is the reason the constant and the added 20 disappear. For any fixed c, (cn + d) / n approaches c. A function is Θ(n) when two positive constants sandwich it between multiples of n for all large n. 3n + 20 sits between 3n and 4n once n is at least 20. It does not sit between two multiples of n², because (3n + 20) / n² approaches 0.

## What it costs

Using the notation does not change the algorithm. It changes the claim. A Θ(n) scan of a million items is a different engineering choice from a Θ(n²) pair scan of the same list. The trace shows n² overtaking n log n once n leaves the toy range.

Write the exact count first, as the previous lesson did for pairs, and only then replace it with Θ. If you start from Θ you can hide a bug such as an extra nested loop. The notation is a compression step, not a substitute for the count.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
