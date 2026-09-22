"""Binary search, bounds, and quick-sort variants."""

from __future__ import annotations

import random

import pytest

from bitsandbytes.search import binary_search, lower_bound, upper_bound
from bitsandbytes.sorting import bubble_sort, quick_sort, quick_sort_three_way, selection_sort


def test_binary_search_and_bounds_on_duplicates() -> None:
    values = [1, 2, 2, 2, 5, 7]
    assert binary_search(values, 5) == 4
    assert binary_search(values, 4) == -1
    assert lower_bound(values, 2) == 1
    assert upper_bound(values, 2) == 4


@pytest.mark.parametrize(
    ("values", "target", "index"),
    [
        ([], 1, -1),
        ([3], 3, 0),
        ([1, 3, 5], 1, 0),
        ([1, 3, 5], 5, 2),
    ],
)
def test_binary_search_samples(values: list[int], target: int, index: int) -> None:
    assert binary_search(values, target) == index


def test_bubble_sort_is_stable() -> None:
    class Item:
        def __init__(self, key: int, label: str) -> None:
            self.key = key
            self.label = label

        def __lt__(self, other: object) -> bool:
            assert isinstance(other, Item)
            return self.key < other.key

    items = [Item(1, "a"), Item(2, "b"), Item(1, "c")]
    bubble_sort(items)
    assert [item.label for item in items] == ["a", "c", "b"]


def test_selection_sort_is_not_stable_on_equal_keys() -> None:
    class Item:
        def __init__(self, key: int, label: str) -> None:
            self.key = key
            self.label = label

        def __lt__(self, other: object) -> bool:
            assert isinstance(other, Item)
            return self.key < other.key

    items = [Item(2, "b"), Item(1, "a"), Item(1, "c")]
    selection_sort(items)
    assert [item.label for item in items] == ["a", "c", "b"]


def test_lomuto_quick_sort_sorts_duplicate_integers() -> None:
    values = [2, 1, 1, 0, 2]
    quick_sort(values, rng=random.Random(0))
    assert values == [0, 1, 1, 2, 2]

    values = [0, 0, 0, 0, 0, 0, 0]
    quick_sort_three_way(values)
    assert values == [0, 0, 0, 0, 0, 0, 0]
