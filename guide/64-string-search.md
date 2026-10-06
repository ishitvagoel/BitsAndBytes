---
title: String search algorithms
slug: string-search
order: 64
status: present
module: bitsandbytes.strings.algorithms
---

## Reuse information while matching

KMP preprocesses a pattern's longest proper prefix that is also a suffix. On mismatch it shifts the pattern according to that table instead of restarting from the beginning, giving O(n + m) time for text length n and pattern length m.

## Hashing trades exact verification for fast filtering

Rabin–Karp compares rolling hashes, then verifies candidate matches because distinct strings can collide. A hash match alone is not proof of equal text.

## Practice

Trace KMP's fallback positions on a pattern with a repeated prefix. Explain why the text pointer does not move backward.

Source: [`algorithms.py`](../bitsandbytes/strings/algorithms.py).
