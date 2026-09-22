# Bits and Bytes

A study path for the data structures in this repository. Read the sections in order. Every function and method has a `Cost` section in its docstring that names the input size, counts the loops, and separates extra memory from the input. The notes below record only the result of that derivation. Worked traces for the trickiest pointer and stack walks live in those module docstrings.

```mermaid
flowchart TD
  lists[SinglyLinkedList]
  listAlgos[ListAlgorithms]
  doubly[DoublyListAndLRU]
  stacks[Stacks]
  sorts[Sorting]
  search[BinarySearch]
  queue[Queues]
  heap[Heaps]
  hash[HashTable]
  tree[BST]
  graph[Graphs]
  lists --> listAlgos --> doubly --> stacks --> sorts --> search --> queue --> heap --> hash --> tree --> graph
```

## 1. Singly linked list

* `bitsandbytes/linked_list.py` — one `Node` chain with a cached tail and a cached length. `append`, `prepend`, and `len` are O(1). `node_at`, `insert`, and `insert_sorted` are O(n). `pop` of the tail is O(n) because the predecessor is not stored. `require_linear` and `refresh` are O(n) time; while they run they hold a `seen` set, so peak extra memory is O(n).

## 2. List algorithms

These modules only rewrite `next` on that shared list. Any call that starts with `require_linear` inherits that O(n) peak before the main loop.

* `linked_lists/reverse.py` — iterative reversal is O(n) time and O(1) extra memory for the three pointers. The recursive form adds O(n) call-stack memory.
* `linked_lists/reverse_in_pairs.py` — swap neighbours. O(n) time, O(1) extra memory for the loop.
* `linked_lists/reverse_in_blocks.py` — reverse every block of `k`. Each node is touched a constant number of times, so time is O(n), not O(n·k).
* `linked_lists/middle.py` — fast and slow pointers; two different “middles” on even length. O(n) time. See the worked trace in the module docstring.
* `linked_lists/cycle.py` — Floyd’s algorithm finds a cycle entrance. O(n) time, O(1) extra memory for the walk itself.
* `linked_lists/remove_cycle.py` — clear the link that points back at the entrance. O(n) time, O(1) extra memory.
* `linked_lists/nth_from_end.py` — a fixed gap of `n` nodes, then one walk together. O(length) time, O(1) extra memory for the two pointers.
* `linked_lists/duplicates.py` — sorted duplicates are O(n) time and O(1) extra memory. Unsorted duplicates use a set: expected O(n) time and O(n) extra memory.
* `linked_lists/rotate.py`, `partition.py`, `odd_even.py`, `reorder.py` — relinking only. O(n) time, O(1) extra memory for each loop.
* `linked_lists/palindrome.py` — split at the left middle, reverse the second half, compare, restore. O(n) time, O(1) extra memory for the loop.
* `linked_lists/delete_node.py` — copy the successor forward. O(1). Cannot delete the tail.
* `linked_lists/add_numbers.py` — least-significant digit at the head. O(n + m) time, O(1) scratch besides the result nodes.
* `linked_lists/merge_sorted.py` — merge two sorted chains by relinking. O(n + m) time, O(1) extra memory.
* `linked_lists/intersection.py` — `require_linear` on both lists, then equalize with cached lengths and walk in step. O(n + m) time; O(1) extra memory for the walk besides the guard peak.
* `linked_lists/sort_list.py` — bottom-up merge sort. O(n log n) time, O(1) extra memory besides nodes. Stable.
* `linked_lists/split_circular.py`, `modular_nodes.py`, `reviewers.py` — see each module’s `Cost` section. `modular_node_from_end` uses `nth_from_end`, so it is O(n) time and O(1) extra memory for the gap walk.

## 3. Doubly linked list and the LRU cache

* `bitsandbytes/doubly_linked_list.py` — `prev` makes unlink and insert-beside-a-node O(1). Reversal is O(n) time and O(1) extra memory.
* `linked_lists/random_pointer.py` — dictionary clone expected O(n) time and O(n) extra memory; interleaved clone O(n) time and O(1) scratch besides the copy.
* `linked_lists/lru_cache.py` — dictionary plus doubly linked list. `get` and `put` are expected O(1). Resident memory is O(capacity). The hash table chapter explains why the dictionary lookup is expected O(1).

## 4. Stacks

* `stacks/stack.py` — bounded stack: capacity, decorator guards, amortized O(1) `push`, O(1) `pop` and `peek`.
* `stacks/algorithm_stack.py` — unbounded LIFO for algorithm lessons. Same amortized costs without a limit check.
* `stacks/symbol_balance.py` — one pass. O(n) time, O(n) worst extra memory for openers.
* `stacks/min_stack.py` — second stack of minima. `push`, `pop`, and `minimum` are O(1).
* `stacks/next_greater.py` — monotonic stack. O(n) time, O(n) extra memory.
* `stacks/stock_span.py` — same monotonic pattern. O(n) time.
* `stacks/largest_rectangle.py` — histogram rectangle. O(n) time.
* `stacks/infix_postfix.py` — shunting yard plus postfix evaluation. O(n) time.
* `stacks/sort_stack.py` — one extra `AlgorithmStack`. Worst case O(n²) time, O(n) extra memory.

## 5. Sorting

* `sorting/bubble_sort.py` — O(n²) worst and average, O(n) best on sorted input, O(1) extra memory. Stable.
* `sorting/selection_sort.py` — O(n²) for every input order. Not stable.
* `sorting/insertion_sort.py` — O(n²) worst and average, O(n) best. Stable.
* `sorting/merge_sort.py` — O(n log n) time, O(n) extra memory. Stable.
* `sorting/quick_sort.py` — Lomuto partition: expected O(n log n), worst O(n²), including an all-equal list. `quick_sort_three_way` handles duplicates in O(n) when every key matches. Not stable.

## 6. Binary search

* `search/binary_search.py` — `binary_search`, `lower_bound`, and `upper_bound` on a sorted sequence. O(log n) time, O(1) extra memory each.

## 7. Queues

* `queues/linked_queue.py` — FIFO with a doubly linked list. Enqueue and dequeue are O(1).
* `queues/circular_queue.py` — fixed-capacity ring buffer with an explicit size counter. Enqueue and dequeue are O(1).

## 8. Heaps

* `heaps/heapsort.py` — `heapify` is O(n); `heapsort` is O(n log n) time and O(1) extra memory. Not stable.

## 9. Hash table

* `hash_tables/chaining.py` — separate chaining. Expected O(1) lookup and insert; rehash is O(n) but amortized.

## 10. Binary search tree

* `trees/bst.py` — insert and search are O(h) for height h; in-order walk is O(n) with O(h) stack memory.

## 11. Graphs

* `graphs/adjacency_list.py` — adjacency lists. DFS and BFS are O(V + E). The teaching `dijkstra_distances` scans all unsettled vertices each step, so O(V²) time on dense graphs; a heap would be O((V + E) log V).

## Appendix: Python tools

These are not the next data-structure lesson after graphs. They stay in the repo as small Python examples.

* `decorators/permission.py` — wrapper is O(1) plus the wrapped call.
* `decorators/access_control.py` — expected O(1) permission lookup, then the action.
* `tools/print_directory.py` — `os.walk` is O(entries).

`print_directory_paths.py` still runs the directory walk.

## Try it

```bash
python3 -m bitsandbytes.tools.print_directory topdown
python3 -m bitsandbytes.decorators.permission
python3 -m bitsandbytes.decorators.access_control developer testdb
```

## Tests

```bash
python3 -m pip install pytest
python3 -m pytest
```
