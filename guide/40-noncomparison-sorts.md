---
title: Counting and radix sorts
slug: noncomparison-sorts
order: 40
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## Use key structure to avoid comparisons

Comparison sorting is a general method, but some keys have a bounded integer range or fixed-width digits. Counting sort records frequencies; radix sort orders one digit at a time using a stable pass.

**By the end of this overview, you can** state when counting or radix sort can outperform comparison sorting and name the memory tradeoff.

Counting sort for `n` values in `[0, k]` takes O(n + k) time and O(k) extra memory. Its cost depends on the value range, not just the number of values. LSD radix sort uses stable digit passes; with `d` digits and base `b`, this implementation takes O(d(n+b)) time and O(n+b) memory per pass. These bounds rely on restrictions on key representation and digit processing.

## Practice and next step

For `[3, 1, 3, 0]`, write the count table for maximum value 3 and reconstruct the output. Then name a range where that table would use more space than the input. See [the repository sorting-extra tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py).
