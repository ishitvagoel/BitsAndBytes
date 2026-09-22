# Bits and Bytes

Data structures and algorithms in Python 3.12+.

The implementations share one linked list and one stack instead of copying a
`Node` class into every file. Each algorithm module documents the approach,
the complexity, and the steps that are easy to misread.

## Layout

| Path | What it is |
| --- | --- |
| `bitsandbytes/linked_list.py` | Singly linked list used by every list algorithm |
| `bitsandbytes/doubly_linked_list.py` | Doubly linked list: O(1) delete when you already hold the node |
| `bitsandbytes/sorting/` | Bubble, selection, insertion, merge, and quick sort |
| `bitsandbytes/stacks/` | Bounded stack, and bracket matching |
| `bitsandbytes/linked_lists/` | List algorithms, including the concepts below |
| `bitsandbytes/decorators/` | Confirmation prompt, and permission checks |
| `bitsandbytes/tools/print_directory.py` | Top-down or bottom-up directory walk |

`print_directory_paths.py` still runs the directory walk.

## Linked list concepts

Read these after reversal, cycle detection, and merging two sorted lists. The
module docstring is the full explanation. This is the idea each one is teaching.

**Two pointers at different speeds** (`middle.py`). One pointer moves two
steps while the other moves one. When the fast pointer reaches the end, the
slow pointer is halfway. On an even-length list there are two middles.
`middle_node` returns the later one. `end_of_first_half` returns the earlier
one, which is where a palindrome check and a reorder split the list. Getting
those two conventions mixed up is the usual bug.

**A fixed gap instead of a length** (`nth_from_end.py`). Park one pointer `n`
nodes ahead of the other and walk them together. When the leader falls off,
the trailer is `n` from the tail. Removal uses an anchor in front of the head
so deleting the first node is the same code as deleting any other node.

**Rewriting `next`, not allocating a new chain.**

* `duplicates.py` — a sorted list only compares a node with its successor. An
  unsorted list remembers values it has already kept. The first occurrence
  stays, so order of first appearance survives.
* `rotate.py` — close the list into a circle, cut it at the new tail, and
  open it again. `k` larger than the length, and negative `k`, both reduce
  with `%`.
* `partition.py` — values less than the pivot form one chain, the rest form
  another, then the second chain hangs off the first. Order inside each group
  stays put.
* `odd_even.py` — odd *positions* (1-based) are gathered in front of even
  positions. The values are not tested for parity.
* `reorder.py` — fold the list in half. Find the end of the left half, reverse
  the right half, and zip them. `[1, 2, 3, 4, 5]` becomes `[1, 5, 2, 4, 3]`.

**You usually need the predecessor** (`delete_node.py`). The predecessor's
`next` is what skips a node. If you only hold the node, copy the successor
into it and delete the successor instead. That cannot delete the tail.

**A cycle is a loop you can open** (`remove_cycle.py`). Floyd's algorithm
finds the entrance. The node that points back at the entrance is the end of
the loop. Clear that one link and every node remains, once.

**Digits grow from the head** (`add_numbers.py`). Put the least significant
digit first. Addition, carry and all, then starts at the only end you can
reach in constant time. A final carry is a new node.

**Sort without indexes** (`sort_list.py`). Merge sort only rewrites `next`.
The bottom-up form merges runs of length 1, then 2, then 4, so it never
searches for a midpoint and never recurses. It is stable and uses a constant
amount of extra memory.

**A second pointer changes the cost** (`doubly_linked_list.py`). `prev` makes
delete-this-node and insert-beside-this-node O(1). Reversal swaps the two
links on each node, then swaps the head with the tail.

**The cache that list is for** (`lru_cache.py`). A dictionary finds the key's
node. The doubly linked list orders nodes by use: head is newest, tail is the
one to evict. Both `get` and `put` are O(1). A singly linked list would make
eviction O(capacity).

**A pointer that is not `next`** (`random_pointer.py`). `random` may aim at
any node. A dictionary from original to copy is the clear clone. Weaving each
copy in front of the next original lets `copy.random` be `original.random.next`,
then the two lists are split apart. That clone needs no dictionary.

## Try it

```bash
python -m bitsandbytes.tools.print_directory topdown
python -m bitsandbytes.decorators.permission
python -m bitsandbytes.decorators.access_control developer testdb
```

## Tests

```bash
python -m pip install pytest
pytest
```
