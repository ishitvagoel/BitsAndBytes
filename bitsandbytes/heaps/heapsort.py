"""Binary max-heap and in-place heapsort.

A max-heap stores the largest key at index 0. Each parent is at least as
large as its two children. ``sift_down`` restores that order after the root
changes. ``heapify`` runs ``sift_down`` from the last parent up to the root.
The sum of subtree heights is linear, so ``heapify`` is O(n), not O(n log n).

Heapsort repeatedly swaps the root with the last heap element, shrinks the
heap by one, and sifts down. It is O(n log n) time and O(1) extra memory,
but it is not stable.
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def heapify(values: list[T]) -> None:
    """Turn ``values`` into a max-heap in place.

    Cost
    ----
    Let n be ``len(values)``. ``sift_down`` at index ``i`` walks at most
    the height of that subtree, ``floor(log2(n)) - floor(log2(i+1))``.
    Summing those heights over all parents is less than 2n, so the total
    is O(n) time. No extra list is allocated: O(1) extra memory.
    """

    last_parent = (len(values) // 2) - 1
    for index in range(last_parent, -1, -1):
        _sift_down(values, index, len(values))


def heapsort(values: list[T]) -> list[T]:
    """Sort ``values`` in ascending order in place with a max-heap.

    Cost
    ----
    ``heapify`` is O(n). The extraction loop runs ``n - 1`` times and each
    ``sift_down`` on the shrinking prefix is O(log n). Total time
    O(n) + O(n log n) = O(n log n). The heap reuses the input list: O(1)
    extra memory besides the array being sorted. Not stable.
    """

    heapify(values)
    end = len(values) - 1
    while end > 0:
        values[0], values[end] = values[end], values[0]
        end -= 1
        _sift_down(values, 0, end + 1)
    return values


def _sift_down(values: list[T], index: int, heap_size: int) -> None:
    """Move ``values[index]`` down until it is not smaller than either child.

    Cost
    ----
    Each step follows the larger child. At most ``floor(log2(heap_size))``
    steps, each O(1). Time O(log heap_size), extra memory O(1).
    """

    while True:
        left = 2 * index + 1
        right = left + 1
        largest = index
        if left < heap_size and values[left] > values[largest]:
            largest = left
        if right < heap_size and values[right] > values[largest]:
            largest = right
        if largest == index:
            return
        values[index], values[largest] = values[largest], values[index]
        index = largest
