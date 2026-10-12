---
title: Approximate membership structures
slug: approximate-membership
order: 67
status: present
module: bitsandbytes.approximate.structures
---

## The idea

A filter with 64 bits and 3 hashes inserts cat, and maybe_contains(cat) is true.

A Bloom filter answers membership with a bit array and several hash functions. add sets the bits those hashes name. maybe_contains returns true only when every one of those bits is set. BloomFilter with 64 bits, 3 hashes, and seed 0 inserts cat. maybe_contains cat returns true. A false answer means the item was definitely never added, because add would have set those bits. A true answer means the item might have been added, or other items may have set the same bits. That is a false positive. The uninserted strings that collide depend on the process hash salt, so this lesson does not pin a particular miss. This filter has no delete. Clearing a bit could erase the evidence of a different item. The library states that contract on the class. A definite miss is the useful answer. It lets a storage engine skip a disk read.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Add | key = cat | add cat sets the three bits that hash names. |
| Hit | hit = true | maybe_contains cat is true. Every required bit is set. |
| Bits | bits = 3 | A clear bit would be a definite miss. This query has none. |

## Why it is correct

There are no false negatives for items that were actually added, as long as nobody clears bits. Each add only sets bits, and maybe_contains only checks those bits. If any bit is clear, at least one add that should have set it did not happen, so the item is absent. If all bits are set, every required bit was set by someone, and that someone might not have been this item. More bits or a different hash count changes how often unrelated items overlap. The seed fixes the hash functions so a test can repeat.

## A common mistake

A hit can be a false positive. A miss means the item was not added.

## What it costs

add and maybe_contains hash the item k times, so they are proportional to k, not to the number of items inserted. Extra memory is the bit array, which you choose up front. A dictionary would be exact and would grow with the items. The filter spends a false-positive rate to keep a fixed size. Say the rate you are willing to accept before you treat a hit as a fact. add is Θ(k) time, and the bit array is fixed extra memory.

## Run it

```python
from bitsandbytes.approximate.structures import BloomFilter
bloom = BloomFilter(bit_count=64, hash_count=3, seed=0)
bloom.add('cat')
print(bloom.maybe_contains('cat'))
# prints: True
```

## Practice and next step

Open Storage engines and locality next. Storage engines place the same keys in a tree or in a sequential scan.
