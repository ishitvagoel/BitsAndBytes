---
title: Dynamic programming
slug: dynamic-programming
order: 14
status: present
module: bitsandbytes.dynamic_programming.classic
---

## The idea

Dynamic programming applies when a problem repeats smaller versions of itself and you can order those versions so each one is ready before you need it. The Fibonacci recurrence F(n) = F(n - 1) + F(n - 2), with F(0) = 0 and F(1) = 1, is the smallest example. A naive recursion recomputes F(3) many times. A bottom-up table fills each index once. The library function fibonacci_modulo keeps only the last two values and returns F(n) mod m. For n = 6 and m = 1000 the result is 8.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Base | n = 1, value = 1 | F(0) and F(1) are given. |
| Through F(3) | n = 3, value = 2 | 1 + 1 = 2, and that cell is F(3). |
| Through F(5) | n = 5, value = 5 | 2 + 3 = 5. |
| F(6) | n = 6, value = 8 | 3 + 5 = 8. |

## Why it is correct

The table is correct by induction. The base cells match the definition. If cells n - 1 and n - 2 hold F(n - 1) and F(n - 2), their sum is F(n) by the recurrence, so writing that sum into cell n preserves the claim. The fill order matters. Cell n is written only after the two cells it reads. A recursion with memoization is the same idea stored in a dictionary instead of an array. The state is the argument n. The transition is the sum. The base cases are the two starting cells.

## What it costs

The table version does Θ(1) work per cell and fills n cells, so the time is Θ(n). The full table uses Θ(n) extra memory. Keeping two running values uses Θ(1) extra memory and the same Θ(n) time, which is what fibonacci_modulo does. The naive recursion without a table does Θ(φ^n) additions because it repeats work. The win is not the recurrence. The win is computing each state once. Larger problems add a second index, and the cost becomes the number of states times the cost of one transition.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
