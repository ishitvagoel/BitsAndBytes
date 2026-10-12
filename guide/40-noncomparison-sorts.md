---
title: Counting and radix sorts
slug: noncomparison-sorts
order: 40
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## The idea

Keys 3, 1, 2, 1 with maximum 3 come out as 1, 1, 2, 3.

Comparison sorts need a logarithmic number of comparisons per item in the worst case when they learn order only by comparing keys. Counting sort skips comparisons when the keys are integers in a known range. counting_sort of 3, 1, 2, 1 with maximum 3 returns 1, 1, 2, 3. It counts how many keys have each value, then writes them into those slots. Equal keys keep their order if the write walks the input from left to right into the next free slot of that count. That stability is what a radix sort needs. lsd_radix_sort of 170, 45, 75, 90, 802, 24, 2, 66 returns 2, 24, 45, 66, 75, 90, 170, 802. Each pass sorts by one digit, starting at the least significant digit, and the next pass must not scramble the order the previous pass built. The digit alphabet is the base, here 10.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Place | digit = 1 | Place 2 copies of 1. Output is [1, 1]. |
| Place | digit = 2 | Place 1 copies of 2. Output is [1, 1, 2]. |
| Place | digit = 3 | Place 1 copies of 3. Output is [1, 1, 2, 3]. |

## Why it is correct

The count array is a correct histogram because every key increments exactly one slot. The prefix of those counts says where each value should start in the output. Writing a key into its slot and advancing the slot places each key once. Stability holds when equal keys are written in the order they appear in the input. A radix pass is a counting sort on one digit. After the least significant digit is stable, sorting the next digit groups larger place values without reordering keys that share that digit. The highest digit pass finishes the order.

## A common mistake

A huge maximum still allocates a count slot for every key up to that maximum.

## What it costs

Counting sort is linear in the number of keys plus the size of the key range. A huge maximum with a tiny list still allocates the count array, so the range belongs in the bound. Radix sort repeats that cost once per digit. With a constant number of digits the total is linear in the number of keys. Extra memory is the count array and the output. These sorts are the right tool for integers or fixed-width strings, not for arbitrary ordered objects. Counting sort is Θ(n + k) time and uses Θ(k) extra memory.

## Run it

```python
from bitsandbytes.sorting.selection_and_radix import counting_sort
print(counting_sort([3, 1, 2, 1], maximum=3))
# prints: [1, 1, 2, 3]
```

## Practice and next step

Open Order-statistic selection next. Order-statistic selection stops once the pivot lands on the rank you asked for.
