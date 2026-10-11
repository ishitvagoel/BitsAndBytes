---
title: Tries and text indexes
slug: tries-and-text-indexes
order: 65
status: present
module: bitsandbytes.strings.algorithms
---

## The idea

A trie stores strings along a path of characters. Trie.insert walks or creates a child for each character. contains walks the same path and succeeds only when the whole key was inserted. After inserting cat and car, contains car is true, contains cat is true, and contains ca is false. ca is a prefix of both keys, and this trie does not treat a prefix as a stored key. A suffix array is a different index. suffix_array_with_lcp on banana returns the suffix starts 5, 3, 1, 0, 4, 2 and an LCP array whose third entry is 3. The suffixes in that order are a, ana, anana, banana, na, nana. Equal prefixes sit together, which is why a pattern query can binary-search the array. The LCP says how long the shared prefix of neighbors is, so you do not recompare those characters.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Keys | hit = car | car is a stored key. ca is only a prefix. |

## Why it is correct

Trie lookup is correct because each step consumes one character and the path is unique. Missing a child means the key was never inserted. Stopping in the middle is not a hit unless insert marked that node as a key, and this contains requires the full key. The suffix array is the sorted order of every suffix. Binary search is valid because that order is alphabetical. The LCP of two adjacent suffixes is a lower bound on comparisons you can skip. Construction has to be counted separately from a single query.

## What it costs

Inserting or looking up a key in the trie is proportional to the key length, not to the number of stored keys, unless you are scanning children linearly. The trie memory is proportional to the number of distinct prefixes. Building a suffix array by sorting suffixes naively is more expensive than one query, and the array itself is linear in the text length. Include that build when you compare a trie with a scan of the raw text. A query-only bound hides the index.

## Run it

```python
from bitsandbytes.strings.algorithms import Trie
trie = Trie()
trie.insert('cat')
trie.insert('car')
print(trie.contains('car'), trie.contains('ca'))
# prints: True False
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
