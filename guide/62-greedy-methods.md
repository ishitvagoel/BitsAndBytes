---
title: Greedy methods
slug: greedy-methods
order: 62
status: present
module: bitsandbytes.greedy.classic
---

## A locally best choice needs a proof

A greedy algorithm commits to a choice without revisiting it. Sorting by earliest finish solves unweighted interval scheduling because an exchange argument shows an optimal schedule can begin with that interval. Fractional knapsack permits taking part of an item; indivisible knapsack does not share the same guarantee.

## Separate rule from justification

Examples are not a proof of optimality. State the exchange, cut, or stay-ahead argument, and identify which input assumptions it uses. Huffman coding's repeated merge of the two least frequencies follows an exchange argument about prefix-code trees.

## Practice

Construct a tempting greedy counterexample for indivisible knapsack. Explain which assumption made the fractional version different.

Source: [`classic.py`](../bitsandbytes/greedy/classic.py).
