"""Heap algorithms."""

from bitsandbytes.heaps import heapify, heapsort


def test_heapify_builds_a_max_heap() -> None:
    values = [3, 1, 4, 1, 5]
    heapify(values)
    assert values[0] == max(values)


def test_heapsort_matches_sorted() -> None:
    values = [4, 1, 3, 2, 5, 0]
    assert heapsort(values) == [0, 1, 2, 3, 4, 5]
    assert values == [0, 1, 2, 3, 4, 5]
