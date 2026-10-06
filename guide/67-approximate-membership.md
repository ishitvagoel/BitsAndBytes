---
title: Approximate membership structures
slug: approximate-membership
order: 67
status: present
module: bitsandbytes.approximate.structures
---

## Trade exactness for compact summaries

A Bloom filter can report “definitely absent” or “possibly present.” It has false positives but no false negatives when used under its standard insertion/query model. It cannot enumerate stored keys or delete entries with a basic bit array.

## State the probability and workload assumptions

False-positive rate depends on bit-array size, number of inserted elements and number of hash probes. Approximate membership is useful when a false positive only triggers an extra exact lookup and memory is constrained.

## Practice

Explain why a Bloom-filter “maybe” must be checked in the underlying store, while “absent” can avoid that lookup.

Source: [`structures.py`](../bitsandbytes/approximate/structures.py).
