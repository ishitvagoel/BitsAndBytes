---
title: Heap operations
slug: heap-operations
order: 49
status: present
module: bitsandbytes.heaps.heapsort
---

## The idea

A binary heap stores a complete tree in an array. For a max-heap, every parent is ≥ its children, so the largest key is at index 0. The children of index i are 2i + 1 and 2i + 2. heapify starts at the last parent and sifts that item down until the invariant holds. On [3, 1, 4, 2] the last parent is index 1. Sifting swaps 1 with 2, leaving [3, 2, 4, 1]. Sifting the root then swaps 3 with 4, leaving [4, 2, 3, 1]. heapsort extracts the root until the array is sorted. The library returns [1, 2, 3, 4].

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Before | root = 3 | The array is not a heap. Index 1 holds 1, and its child at index 3 holds 2. |
| Sift index 1 | array = [3, 2, 4, 1] | 1 is smaller than its child 2, so those values swap. |
| Sift index 0 | root = 4 | 3 is smaller than its child 4, so 4 becomes the root and the array is [4, 2, 3, 1]. |
| After heapsort | order = ascending | Repeated extraction leaves the array sorted. The library returns [1, 2, 3, 4]. |

## Why it is correct

Sift-down restores the invariant in one subtree when both children are already heaps. It swaps the parent with the larger child when the parent is smaller, then repeats. Each swap moves the violation down, and a leaf has no child to violate. heapify can start at the last parent because every index after that is a leaf, and a leaf is already a heap. The extraction loop removes the current maximum and sifts the item that was moved into the root, so the next maximum surfaces. Writing extracted maxima from the end of the array backward produces ascending order.

## What it costs

heapify is Θ(n). The sift at a node is proportional to its height, and the sum of heights in a complete tree is less than 2n. Each of the n extractions then sifts a prefix of height Θ(log n), so heapsort is Θ(n log n) time. The heap reuses the input array, so extra memory is O(1). The sort is not stable. A priority queue uses the same sift for insert and extract-min, each Θ(log n), which is the right cost when you need the next extreme key and not the full sorted order.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
