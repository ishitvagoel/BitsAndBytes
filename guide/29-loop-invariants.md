---
title: Loop invariants
slug: loop-invariants
order: 29
status: present
module: bitsandbytes.complexity
---

## The idea

A loop invariant is a statement that is true before the loop and after every iteration. It is the reason the loop's final state means what you think it means. Three checks make the argument. Initialization says the statement holds before the first iteration. Preservation says one iteration that starts from a true statement ends with the statement still true. Termination says the loop stops, and the invariant plus the exit condition is the result you wanted. Insertion sort's invariant is that the prefix values[0:i] is sorted at the start of the outer step that inserts values[i].

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Before insert | prefix = [3], key = 1 | The prefix [3] is sorted. 1 is the next key. |
| Shift | hole = 0, key = 1 | 3 moves right because it is greater than 1. The hole is at index 0. |
| Place | prefix = [1, 3], i = 1 | 1 drops into the hole. The prefix of length 2 is sorted. |

## Why it is correct

Initialization holds because a prefix of one item is sorted, and the loop starts inserting at index 1. Preservation holds because the inner loop shifts every larger prefix item one slot right and writes the new key into the hole. The items that were sorted stay in order, and the new key sits between a smaller or equal left neighbor and a larger right neighbor. Termination holds because i runs from 1 to n - 1 and then stops. The prefix is the whole list, so the list is sorted. The library's insertion sort uses a strict < comparison, so an equal key does not move past an earlier equal key. That is why the sort is stable.

## What it costs

The invariant does not by itself give the time bound. Counting the shifts does. On reverse-sorted input the step for i shifts i items, and the sum is n(n - 1) / 2, so the time is Θ(n²). On sorted input the inner loop never shifts, so the time is Θ(n). Extra memory is the hole index and the saved key, O(1).

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
