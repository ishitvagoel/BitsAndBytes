"""Non-comparison sorts and selection."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def comparison_sort_lower_bound(n: int) -> int:
    """Return ``floor(log2(n!))``, the decision-tree height for sorting n keys.

    Stirling's approximation gives ``log2(n!) = Θ(n log n)``, which is why
    comparison sorts cannot beat O(n log n) in the worst case.

    Cost
    ----
    O(n) multiplications on integers that grow with n; this is a teaching
    count, not a word-RAM step bound for huge n.
    """

    if n < 0:
        raise ValueError("n cannot be negative.")
    if n <= 1:
        return 0
    factorial = 1
    for value in range(2, n + 1):
        factorial *= value
    return factorial.bit_length() - 1


def counting_sort(values: list[int], *, maximum: int) -> list[int]:
    """Sort non-negative integers in ``[0, maximum]`` stably.

    Cost
    ----
    O(n + maximum) time for n = ``len(values)``. Count array length
    ``maximum + 1``: O(maximum) extra memory.
    """

    counts = [0] * (maximum + 1)
    for value in values:
        if value < 0 or value > maximum:
            raise ValueError("value out of range for counting sort")
        counts[value] += 1
    output: list[int] = []
    for digit, count in enumerate(counts):
        output.extend([digit] * count)
    return output


def lsd_radix_sort(values: list[int], *, base: int = 10) -> list[int]:
    """Sort non-negative integers with least-significant-digit radix passes.

    Cost
    ----
    Let d be the number of digits in the largest value. Each pass is O(n + base).
    Total O(d · (n + base)) time and O(n + base) extra memory per pass.
    """

    if base < 2:
        raise ValueError("base must be at least 2.")
    if not values:
        return []
    maximum = max(values)
    exp = 1
    working = list(values)
    while exp <= maximum:
        buckets: list[list[int]] = [[] for _ in range(base)]
        for value in working:
            if value < 0:
                raise ValueError("LSD radix sort requires non-negative integers")
            digit = (value // exp) % base
            buckets[digit].append(value)
        working = [item for bucket in buckets for item in bucket]
        exp *= base
    return working


def lsd_radix_sort_strings(values: list[str], *, width: int) -> list[str]:
    """Sort fixed-width strings by character from right to left.

    Cost
    ----
    d passes for width d, each O(n + alphabet) with alphabet 256 here.
    Total O(d · (n + 256)) time.
    """

    alphabet = 256
    working = list(values)
    for position in range(width - 1, -1, -1):
        buckets: list[list[str]] = [[] for _ in range(alphabet)]
        for text in working:
            if len(text) != width:
                raise ValueError("every string must have the fixed width")
            code = ord(text[position])
            buckets[code].append(text)
        working = [item for bucket in buckets for item in bucket]
    return working


def quickselect(values: list[int], k: int) -> int:
    """Return the k-th smallest element (0-based) in expected O(n) time.

    Cost
    ----
    Expected O(n) from random pivot splits. Worst O(n²) if every pivot is
    extreme. O(1) extra memory besides the input list indices.
    """

    if k < 0 or k >= len(values):
        raise IndexError("k out of range")
    left = 0
    right = len(values) - 1
    while left <= right:
        pivot_index = _partition(values, left, right)
        if pivot_index == k:
            return values[k]
        if k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
    raise RuntimeError("quickselect failed")


def _partition(values: list[int], left: int, right: int) -> int:
    pivot = values[right]
    store = left
    for index in range(left, right):
        if values[index] <= pivot:
            values[store], values[index] = values[index], values[store]
            store += 1
    values[store], values[right] = values[right], values[store]
    return store


def binary_search_on_answer(
    low: int,
    high: int,
    feasible: Callable[[int], bool],
) -> int:
    """Return the smallest integer in ``[low, high]`` where ``feasible`` is true.

    ``feasible`` must be monotonic: false…false, true…true as values increase.

    Cost
    ----
    O(log(high - low)) calls to ``feasible``, each charged separately.
    """

    if low > high:
        raise ValueError("empty search range")
    answer: int | None = None
    while low <= high:
        middle = low + (high - low) // 2
        if feasible(middle):
            answer = middle
            high = middle - 1
        else:
            low = middle + 1
    if answer is None:
        raise ValueError("no feasible answer in range")
    return answer


def inversion_count(values: list[int]) -> int:
    """Count pairs ``i < j`` with ``values[i] > values[j]`` using merge sort.

    Cost
    ----
    O(n log n) time, O(n) extra memory for the merge buffer.
    """

    copy = values.copy()
    buffer = [0] * len(copy)
    return _inversion_merge(copy, buffer, 0, len(copy) - 1)


def _inversion_merge(
    values: list[int],
    buffer: list[int],
    left: int,
    right: int,
) -> int:
    if left >= right:
        return 0
    middle = left + (right - left) // 2
    count = _inversion_merge(values, buffer, left, middle)
    count += _inversion_merge(values, buffer, middle + 1, right)
    index = left
    left_index = left
    right_index = middle + 1
    while left_index <= middle and right_index <= right:
        if values[left_index] <= values[right_index]:
            buffer[index] = values[left_index]
            left_index += 1
        else:
            buffer[index] = values[right_index]
            count += middle - left_index + 1
            right_index += 1
        index += 1
    while left_index <= middle:
        buffer[index] = values[left_index]
        left_index += 1
        index += 1
    while right_index <= right:
        buffer[index] = values[right_index]
        right_index += 1
        index += 1
    for pos in range(left, right + 1):
        values[pos] = buffer[pos]
    return count
