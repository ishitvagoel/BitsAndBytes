---
title: Prefix sums
slug: prefix-sums
order: 60
status: present
module: bitsandbytes.patterns.arrays
---

## Turn a range sum into two lookups

Define prefix[0] = 0 and prefix[i+1] = prefix[i] + values[i]. Then the sum on half-open range [left, right) is prefix[right] − prefix[left]. Building the array takes O(n) time and space; each range sum takes O(1).

## Count subarrays with a running total

For a target sum k, each current prefix p needs earlier prefixes equal to p−k. A frequency map counts those earlier values before the current prefix is inserted, which prevents counting an empty range.

## Practice

For a short list with positive and negative values, list prefix sums and count every subarray totaling k. Explain why a two-pointer sum window would not generally work.

Source: [`arrays.py`](../bitsandbytes/patterns/arrays.py).
