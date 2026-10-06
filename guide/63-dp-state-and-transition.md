---
title: Dynamic programming state and transitions
slug: dp-state-and-transition
order: 63
status: present
module: bitsandbytes.dynamic_programming.classic
---

## Define state before writing a recurrence

Dynamic programming applies when subproblems repeat and an optimal solution can be built from smaller states. Define exactly what dp[state] means, identify transitions, and establish base cases before choosing top-down memoization or bottom-up order.

## Count states and transitions

Time is usually the number of reachable states times the transition work per state. Memory is the retained state space, which may differ from time if old rows can be discarded. Memoization does not make an exponential state space polynomial by itself.

## Practice

For edit distance, state what dp[i][j] represents and list the match, replacement, insertion and deletion transitions. Mark the dependencies that determine fill order.

Source: [`classic.py`](../bitsandbytes/dynamic_programming/classic.py).
