---
title: Limits and approximation
slug: limits-and-approximation
order: 20
status: present
module: bitsandbytes.limits.approximation
---

* `limits/approximation.py` — 2-approximation vertex cover.

## Focused lesson

- [Approximation guarantees](./69-approximation-guarantees.md)

## Industry

A working engineer distinguishes a proven lower bound from an unresolved
complexity assumption. General minimum vertex cover is NP-hard; no exact
polynomial-time algorithm is known. For a simple approximation, repeatedly
choose an uncovered edge and add its endpoints. The chosen edges are pairwise
vertex-disjoint, giving a 2-approximation.
