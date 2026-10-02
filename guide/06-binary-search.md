---
title: Binary search
slug: binary-search
order: 6
status: present
module: bitsandbytes.search.binary_search
---

* `search/binary_search.py` — `binary_search`, `lower_bound`, and `upper_bound` on a sorted sequence. O(log n) time, O(1) extra memory each.

## Industry

A working engineer searches a sorted list with `bisect.bisect_left`, which
returns the insertion point to the left of any matching entries. The
`bisect` documentation states that this search is O(log n). `insort` is O(n)
only because the following list insertion moves elements.
