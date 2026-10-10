---
title: Singly linked list
slug: singly-linked-list
order: 1
status: present
module: bitsandbytes.linked_list
---

## The idea

A singly linked list stores each value in a node whose next reference points at the following node. The list keeps a head, a cached tail, and a size. The invariant is that following next from the head visits exactly size nodes and ends at the cached tail, whose next is empty. Prepending changes the head in Θ(1) time. Appending with a cached tail changes the old tail's next and moves the tail pointer in Θ(1) time. Reading an index walks from the head, so it is Θ(n). Removing the tail is also Θ(n), because the predecessor is not stored.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Empty | size = 0 | Head and tail are empty. Size is 0. |
| Append a | size = 1, tail = a | The only node is both head and tail. |
| Append b | size = 2, tail = b | The old tail's next becomes b, and the tail pointer moves. Head stays a. |
| Find index 1 | steps = 1 | The search starts at the head and follows one link. |

## Why it is correct

The invariant is preserved by each edit that updates the cached fields together with the links. Append writes the new node, points the old tail at it, and then moves the tail cache. If it moved the cache first, the old tail would be unreachable and the invariant would fail. A search that starts at the head and follows next i times lands on index i because the nodes are in a single chain with no extra forward jumps. There is no predecessor pointer, so the only way to find the node before the tail is to walk until next is the tail.

## What it costs

Append and prepend are Θ(1). Index lookup and tail removal are Θ(n). len is Θ(1) because size is cached. Extra memory is one node per item plus the three list fields. A Python list is the better default when you need list[i]. The linked list earns its place when you already hold the node you want to relink.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
