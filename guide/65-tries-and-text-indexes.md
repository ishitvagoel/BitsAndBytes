---
title: Tries and text indexes
slug: tries-and-text-indexes
order: 65
status: present
module: bitsandbytes.strings.algorithms
---

## Choose an index from the query

A trie shares prefixes and supports prefix queries in O(L) character steps for query length L, with memory proportional to stored nodes and edges. An inverted index maps terms to document postings. A suffix array orders suffix starts and supports binary search over text substrings, with preprocessing and LCP storage costs.

## Include the build cost

An index speeds queries by spending time and memory before the query arrives. State whether the cost includes construction, stored text, and output size; outputting k matches alone costs at least Ω(k).

## Practice

Choose among a trie, inverted index and suffix array for autocomplete, document search and substring queries. Name the query each structure makes efficient.

Source: [`algorithms.py`](../bitsandbytes/strings/algorithms.py).
