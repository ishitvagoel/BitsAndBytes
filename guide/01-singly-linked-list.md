---
title: Singly linked list
slug: singly-linked-list
order: 1
status: present
module: bitsandbytes.linked_list
---

* `bitsandbytes/linked_list.py` — one `Node` chain with a cached tail and a cached length. `append`, `prepend`, and `len` are O(1). `node_at`, `insert`, and `insert_sorted` are O(n). `pop` of the tail is O(n) because the predecessor is not stored. `require_linear` and `refresh` are O(n) time; while they run they hold a `seen` set, so peak extra memory is O(n).
