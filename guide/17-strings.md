---
title: Strings
slug: strings
order: 17
status: present
module: bitsandbytes.strings.algorithms
---

* `strings/algorithms.py` — trie, KMP, Rabin-Karp, inverted index, run-length encoding, suffix array with LCP.

## Focused lessons

- [String search algorithms](./64-string-search.md)
- [Tries and text indexes](./65-tries-and-text-indexes.md)

## Industry

A working engineer answers which documents contain a term with an inverted
index. PostgreSQL documents GIN indexes as inverted indexes: a separate
entry for each component value, so a query can test whether that value is
present. `InvertedIndex` in this module is that map from a term to its
posting list.
