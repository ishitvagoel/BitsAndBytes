"""Expectation argument and the all-equal Lomuto bound."""

from __future__ import annotations

import random
from importlib import import_module

from bitsandbytes.sorting import quick_sort

quick_sort_module = import_module("bitsandbytes.sorting.quick_sort")

_DISTINCT_KEYS = (
    "A random pivot on distinct keys is expected O(n log n) because the "
    "i-th and j-th order statistics are compared only when one of them is "
    "the first pivot chosen from the ``j - i + 1`` keys in that range, "
    "which has probability ``2 / (j - i + 1)``, and the sum of those "
    "probabilities over pairs is at most ``2 n H_n`` for the n-th harmonic "
    "number ``H_n``, which is O(n log n)."
)
_ALL_EQUAL_LOMUTO = (
    "All-equal Lomuto stays the linear-decrement recurrence "
    "``T(n) = T(n - 1) + O(n)`` because every key compares less than or "
    "equal to the pivot, the boundary advances to the last index, and the "
    "right side is empty."
)


def _compact(text: str | None) -> str:
    return " ".join((text or "").split())


def test_expectation_sentences() -> None:
    module_doc = _compact(quick_sort_module.__doc__)
    assert _DISTINCT_KEYS in module_doc
    assert _ALL_EQUAL_LOMUTO in module_doc


def test_sorts_duplicate_sample() -> None:
    values = [3, 1, 2, 2]
    assert quick_sort(values, rng=random.Random(0)) == [1, 2, 2, 3]
