"""Linked-list algorithms built on :class:`bitsandbytes.linked_list.LinkedList`.

The modules below the original set (reverse, cycle, merge, and so on) are the
next ideas worth learning. Each file's docstring is the explanation: what the
pointer is doing, why that pointer is enough, and the cost.

* ``middle`` — one walk finds a midpoint, because a fast pointer covers two
  steps for every step the slow pointer takes.
* ``nth_from_end`` — two pointers a fixed gap apart reach the tail's neighbour
  without a separate length pass.
* ``duplicates``, ``rotate``, ``partition``, ``odd_even``, ``reorder`` —
  rearrangements that only rewrite ``next``.
* ``delete_node`` — why a predecessor is normally required, and the one trick
  that avoids it.
* ``remove_cycle`` — open the loop Floyd's algorithm found.
* ``add_numbers`` — digits stored least-significant-first, so addition starts
  at the head.
* ``sort_list`` — bottom-up merge sort, the sort that does not need indexes.
* ``random_pointer`` — clone a node that also points somewhere arbitrary.
* ``lru_cache`` — a doubly linked list plus a dictionary.
"""

from bitsandbytes.linked_lists.add_numbers import add_numbers
from bitsandbytes.linked_lists.cycle import find_cycle_start
from bitsandbytes.linked_lists.delete_node import delete_without_predecessor
from bitsandbytes.linked_lists.duplicates import (
    remove_sorted_duplicates,
    remove_unsorted_duplicates,
)
from bitsandbytes.linked_lists.intersection import find_intersection
from bitsandbytes.linked_lists.lru_cache import LRUCache
from bitsandbytes.linked_lists.merge_sorted import merge_sorted, merge_sorted_into
from bitsandbytes.linked_lists.middle import end_of_first_half, middle_node
from bitsandbytes.linked_lists.modular_nodes import (
    modular_node_from_end,
    modular_node_from_start,
)
from bitsandbytes.linked_lists.nth_from_end import nth_from_end, remove_nth_from_end
from bitsandbytes.linked_lists.odd_even import group_by_position_parity
from bitsandbytes.linked_lists.palindrome import is_palindrome
from bitsandbytes.linked_lists.partition import partition
from bitsandbytes.linked_lists.random_pointer import (
    RandomNode,
    clone_interleaved,
    clone_with_map,
)
from bitsandbytes.linked_lists.remove_cycle import remove_cycle
from bitsandbytes.linked_lists.reorder import reorder
from bitsandbytes.linked_lists.reverse import reverse_iterative, reverse_recursive
from bitsandbytes.linked_lists.reverse_in_blocks import reverse_in_blocks
from bitsandbytes.linked_lists.reverse_in_pairs import reverse_in_pairs
from bitsandbytes.linked_lists.reviewers import Reviewer, ReviewersList
from bitsandbytes.linked_lists.rotate import rotate_right
from bitsandbytes.linked_lists.sort_list import sort_list
from bitsandbytes.linked_lists.split_circular import split_circular

__all__ = [
    "LRUCache",
    "RandomNode",
    "Reviewer",
    "ReviewersList",
    "add_numbers",
    "clone_interleaved",
    "clone_with_map",
    "delete_without_predecessor",
    "end_of_first_half",
    "find_cycle_start",
    "find_intersection",
    "group_by_position_parity",
    "is_palindrome",
    "merge_sorted",
    "merge_sorted_into",
    "middle_node",
    "modular_node_from_end",
    "modular_node_from_start",
    "nth_from_end",
    "partition",
    "remove_cycle",
    "remove_nth_from_end",
    "remove_sorted_duplicates",
    "remove_unsorted_duplicates",
    "reorder",
    "reverse_in_blocks",
    "reverse_in_pairs",
    "reverse_iterative",
    "reverse_recursive",
    "rotate_right",
    "sort_list",
    "split_circular",
]
