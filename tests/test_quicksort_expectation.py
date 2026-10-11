"""Literal quicksort results for a seeded run and a duplicate sample."""

from __future__ import annotations

import random

from bitsandbytes.sorting import quick_sort


def test_seeded_sort_is_fully_ordered() -> None:
    assert quick_sort([3, 1, 4, 2], rng=random.Random(0)) == [1, 2, 3, 4]


def test_sorts_duplicate_sample() -> None:
    values = [3, 1, 2, 2]
    assert quick_sort(values, rng=random.Random(0)) == [1, 2, 2, 3]
