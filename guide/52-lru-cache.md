---
title: LRU cache
slug: lru-cache
order: 52
status: present
module: bitsandbytes.linked_lists.lru_cache
---

## The idea

An LRU cache of capacity k keeps the k most recently used keys. The library uses two structures. A dictionary maps a key to the node that holds it. A doubly linked list orders those nodes by use. The head side is the most recent key and the tail side is the least recent. get moves a hit to the front. put of an existing key updates the value and moves that node to the front. put of a new key evicts the tail when the cache is already full, then inserts the new key at the front. Start with capacity 2. put a, put b, get a, put c. b was used before a, so b is the tail and c evicts it. get b then returns None. get a returns 1 and get c returns 3. A missing get returns None rather than raising.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Evict | miss = b | b was the least recent key, so c replaces it. |

## Why it is correct

The recency order is the list order. Moving a node to the front is a constant-time unlink and insert because the node stores both neighbors. The dictionary is why get does not scan the list to find the node. Eviction removes the tail, which the list already knows, and deletes that key from the dictionary. After put c, the live keys are a and c. b is absent, so a later get cannot resurrect it. The capacity check happens before the new insert, so the size never stays above capacity.

## What it costs

get and put are expected constant time. The dictionary lookup is expected constant time and the list edit is constant time. A cache that scanned a singly linked list of k nodes would pay linear time in the capacity on every eviction. Extra memory is one dictionary entry and one node per live key, so it is proportional to the capacity, not to the history of every key you have ever seen. Name both structures when you explain the bound. Either one alone is not enough.

## Run it

```python
from bitsandbytes.linked_lists.lru_cache import LRUCache
cache = LRUCache(2)
cache.put('a', 1)
cache.put('b', 2)
cache.get('a')
cache.put('c', 3)
print(cache.get('b'))
# prints: None
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
