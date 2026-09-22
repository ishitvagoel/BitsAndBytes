"""Tests for analysis and library cost modules."""

from __future__ import annotations

import pytest

from bitsandbytes.complexity import (
    RecurrenceShape,
    bound_vocabulary,
    classify_recurrence,
    recursion_limit,
)
from bitsandbytes.library_costs import (
    bfs_layer_sizes,
    insert_into_sorted,
    list_pop_front_cost_demo,
    timsort_sorted,
    top_k_smallest,
)


def test_bound_vocabulary_and_recurrences() -> None:
    vocab = bound_vocabulary()
    assert "O" in vocab and "Theta" in vocab
    assert classify_recurrence(RecurrenceShape.MERGE_DIVIDE) == "Θ(n log n)"
    assert classify_recurrence(RecurrenceShape.HALVING) == "Θ(log n)"
    assert recursion_limit() >= 100


def test_bfs_layer_sizes_empty_start() -> None:
    assert bfs_layer_sizes({}, "missing") == []


def test_bfs_layer_sizes_sample() -> None:
    adjacency = {
        0: [1, 2],
        1: [3],
        2: [],
        3: [],
    }
    assert bfs_layer_sizes(adjacency, 0) == [1, 2, 1]


def test_library_helpers() -> None:
    assert top_k_smallest([5, 1, 4, 2], 2) == [1, 2]
    values = [1, 3, 5]
    insert_into_sorted(values, 2)
    assert values == [1, 2, 3, 5]
    assert timsort_sorted([3, 1, 2]) == [1, 2, 3]
    assert list_pop_front_cost_demo(5) == 4


def test_top_k_invalid() -> None:
    with pytest.raises(ValueError):
        top_k_smallest([1], -1)
