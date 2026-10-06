---
title: Singly linked list
slug: singly-linked-list
order: 1
status: present
module: bitsandbytes.linked_list
---

## Follow the links

A singly linked list stores each value in a node whose `next` reference points to the following node. The list keeps a head, a cached tail, and a size. The central invariant is that following `next` from the head visits exactly `size` nodes and ends at the cached tail, whose `next` is empty.

Prepending changes the head in O(1) time. Appending changes the old tail's link and moves the cached tail in O(1). Finding an index requires walking from the head and takes O(n). Removing the tail also takes O(n), because the node before it is not stored. A cached size makes `len` O(1), but any operation that verifies or refreshes the whole chain takes O(n) time.

Before changing links, keep a reference to any successor that must remain reachable. When removing the head or tail, update the matching cached field as well as the link. Empty and one-node lists are the boundary cases that expose many broken updates.

## Practice and next step

Draw `A → B → C` and append `D`, then remove the head. Write head, tail, size and every changed link after each operation. Continue to the [focused pointer-pattern overviews](./fast-slow-pointer-patterns.md) or the [relinking overview](./linked-list-reversal-and-relinking.md).

* `bitsandbytes/linked_list.py` — one `Node` chain with a cached tail and a cached length. `append`, `prepend`, and `len` are O(1). `node_at`, `insert`, and `insert_sorted` are O(n). `pop` of the tail is O(n) because the predecessor is not stored. `require_linear` and `refresh` are O(n) time; while they run they hold a `seen` set, so peak extra memory is O(n).

## Industry

A working engineer uses a singly linked list when a value must be added at
the head, or appended at a cached tail, without sliding every later element.
Python's time-complexity documentation charges `list.insert` and `list.pop`
at index 0 as O(n) for that slide. Popping this list's tail stays O(n),
because the predecessor is not stored; a queue that needs the front uses
`collections.deque` instead.
