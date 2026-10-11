---
title: String search algorithms
slug: string-search
order: 64
status: present
module: bitsandbytes.strings.algorithms
---

## The idea

A naive search tries the pattern at every index of the text and compares characters until one differs. Knuth-Morris-Pratt avoids restarting the text index after a partial match. kmp_search of pattern ababa in text ababcababa returns 5. Index 0 matches four characters and then fails, because the text has c where the pattern needs a. The failure links say how long a prefix of the pattern is also a suffix of the part just matched, so the search resumes in the middle of the pattern instead of at its first character. rabin_karp_search on the same strings also returns 5. It compares a rolling hash of the pattern with the hash of each window, and it still checks the characters when the hashes agree. A hash hit is a candidate, not a proof.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Match | index = 5 | The first full match of ababa starts at index 5. |

## Why it is correct

The failure link at a position is the longest proper prefix that is also a suffix of the pattern up to that position. Following it on a mismatch preserves the characters that are already known to match. That is why the text index does not move backward. Rabin-Karp's window hash can be updated in constant time by removing the character that leaves and adding the character that enters. Equal hashes can still be different strings, so the character check is part of correctness. Unequal hashes are a sure miss.

## What it costs

The failure table is linear in the pattern length. The search is linear in the text length. Extra memory is the failure table. The naive search is linear in the product of the two lengths. Rabin-Karp is linear in expectation and can degrade if every window collides. Use KMP when you want a worst-case linear bound. Use a rolling hash when you already have a modulus you trust and you verify candidates.

## Run it

```python
from bitsandbytes.strings.algorithms import kmp_search
print(kmp_search('ababcababa', 'ababa'))
# prints: 5
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
