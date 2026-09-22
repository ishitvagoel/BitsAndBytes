"""Dynamic array and linked deque."""

from __future__ import annotations

import pytest

from bitsandbytes.deques import LinkedDeque
from bitsandbytes.linear import DynamicArray


def test_dynamic_array_empty_and_one() -> None:
    array: DynamicArray[int] = DynamicArray()
    with pytest.raises(IndexError):
        array.pop()
    array.append(7)
    assert len(array) == 1
    assert array[0] == 7
    assert array.pop() == 7


def test_dynamic_array_distinguishing_copy_bound() -> None:
    array = DynamicArray(initial_capacity=1)
    assert array.total_copy_cost_for_appends(8) == 7


def test_linked_deque_both_ends() -> None:
    deque: LinkedDeque[str] = LinkedDeque()
    deque.append_right("b")
    deque.append_left("a")
    assert deque.pop_left() == "a"
    assert deque.pop_right() == "b"


def test_linked_deque_middle_insert_is_linear() -> None:
    deque: LinkedDeque[int] = LinkedDeque()
    for value in range(4):
        deque.append_right(value)
    deque.insert_at(2, 99)
    assert list(deque) == [0, 1, 99, 2, 3]
