---
title: Approximation guarantees
slug: approximation-guarantees
order: 69
status: present
module: bitsandbytes.limits.approximation
---

## Separate a feasible answer from an optimality claim

For minimum vertex cover, selecting both endpoints of every edge in a maximal matching yields a cover with at most twice the optimum size. Every matching needs distinct cover vertices, so the optimum is at least the matching size; the construction selects two per matched edge.

## State what the ratio means

A 2-approximation guarantees solution cost at most 2·OPT for this minimization problem. It does not promise a solution exactly twice optimal or a useful ratio for every optimization problem. Verify feasibility separately from the bound.

## Practice

Given a maximal matching, form the endpoint set. Prove it covers every edge and derive the factor-two bound from disjoint matched endpoints.

Source: [`approximation.py`](../bitsandbytes/limits/approximation.py).
