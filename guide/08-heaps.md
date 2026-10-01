---
title: Heaps
slug: heaps
order: 8
status: present
module: bitsandbytes.heaps.heapsort, bitsandbytes.heaps.priority_queue
---

* `heaps/heapsort.py` — `heapify` is O(n); `heapsort` is O(n log n) time and O(1) extra memory. Not stable.
* `heaps/priority_queue.py` — min-heap with `decrease_key` through an index map. Push, pop, and decrease-key are O(log n).
