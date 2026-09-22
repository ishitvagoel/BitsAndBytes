"""Linear probing and sorting extras."""

from bitsandbytes.hash_tables.linear_probing import (
    LinearProbingHashTable,
    degenerate_chain_length,
)
from bitsandbytes.sorting.selection_and_radix import (
    binary_search_on_answer,
    comparison_sort_lower_bound,
    counting_sort,
    inversion_count,
    lsd_radix_sort,
    lsd_radix_sort_strings,
    quickselect,
)


def test_linear_probing_roundtrip() -> None:
    table: LinearProbingHashTable[str, int] = LinearProbingHashTable(capacity=4)
    table["a"] = 1
    table["b"] = 2
    del table["a"]
    table["c"] = 3
    assert table["b"] == 2
    assert table["c"] == 3


def test_degenerate_chain_length() -> None:
    assert degenerate_chain_length(10, 1) == 10


def test_counting_and_radix_sort() -> None:
    assert counting_sort([2, 0, 2, 1], maximum=2) == [0, 1, 2, 2]
    assert lsd_radix_sort([170, 45, 75, 90, 802]) == [45, 75, 90, 170, 802]
    assert lsd_radix_sort_strings(["cab", "car", "cat"], width=3) == [
        "cab",
        "car",
        "cat",
    ]


def test_quickselect_and_inversions() -> None:
    values = [3, 1, 4, 1, 5]
    assert quickselect(values, 2) == 3
    assert inversion_count([2, 3, 8, 6, 1]) == 5


def test_binary_search_on_answer() -> None:
    assert binary_search_on_answer(0, 10, lambda value: value * value >= 20) == 5


def test_comparison_lower_bound_small() -> None:
    assert comparison_sort_lower_bound(4) >= 4
