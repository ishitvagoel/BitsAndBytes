"""Sorting algorithms."""

from __future__ import annotations

import random

import pytest

from bitsandbytes.sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)

CASES = [
    [],
    [1],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [1, 5, 7, 2, 0, -1],
    [3, 1, 2],
    [5, 1, 5, 1, 5],
    [0, 0, 0],
]


@pytest.mark.parametrize("values", CASES)
@pytest.mark.parametrize(
    "algorithm",
    [bubble_sort, insertion_sort, selection_sort, quick_sort],
)
def test_in_place_sorts_match_sorted(algorithm, values: list[int]) -> None:
    original = list(values)
    result = algorithm(values)
    assert result is values
    assert values == sorted(original)


@pytest.mark.parametrize("values", CASES)
def test_merge_sort_returns_a_new_list(values: list[int]) -> None:
    original = list(values)
    result = merge_sort(values)
    assert result == sorted(original)
    assert values == original
    assert result is not values


def test_merge_sort_is_stable() -> None:
    class Item:
        def __init__(self, key: int, label: str) -> None:
            self.key = key
            self.label = label

        def __lt__(self, other: object) -> bool:
            assert isinstance(other, Item)
            return self.key < other.key

    items = [Item(1, "a"), Item(2, "b"), Item(1, "c")]
    result = merge_sort(items)
    assert [item.label for item in result] == ["a", "c", "b"]


def test_insertion_sort_is_stable() -> None:
    class Item:
        def __init__(self, key: int, label: str) -> None:
            self.key = key
            self.label = label

        def __lt__(self, other: object) -> bool:
            assert isinstance(other, Item)
            return self.key < other.key

    items = [Item(1, "a"), Item(2, "b"), Item(1, "c")]
    insertion_sort(items)
    assert [item.label for item in items] == ["a", "c", "b"]


def test_selection_sort_descending() -> None:
    values = [1, 5, 7, 2, 0, -1]
    assert selection_sort(values, reverse=True) == [7, 5, 2, 1, 0, -1]


def test_quick_sort_uses_the_supplied_generator() -> None:
    values = [9, 4, 7, 1, 3, 8, 2, 6, 5]
    assert quick_sort(values, rng=random.Random(0)) == list(range(1, 10))


def test_bubble_sort_stops_early_on_sorted_input() -> None:
    values = [1, 2, 3, 4]
    assert bubble_sort(values) == [1, 2, 3, 4]
