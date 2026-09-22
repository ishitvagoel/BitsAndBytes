"""Shared linked list: construction, edits, and circular form."""

import pytest

from bitsandbytes import LinkedList


def test_build_append_and_string_form() -> None:
    lst = LinkedList([1, 2])
    lst.append(3)
    assert list(lst) == [1, 2, 3]
    assert len(lst) == 3
    assert str(lst) == "1 --> 2 --> 3"
    assert lst.tail is not None
    assert lst.tail.data == 3


def test_prepend_insert_and_node_at() -> None:
    lst: LinkedList[int] = LinkedList()
    lst.prepend(2)
    lst.insert(0, 1)
    lst.insert(len(lst), 4)
    lst.insert(2, 3)
    assert list(lst) == [1, 2, 3, 4]
    assert lst.node_at(2).data == 3
    assert lst.node_at(-1).data == 4


def test_pop_and_remove() -> None:
    lst = LinkedList([1, 2, 3, 2])
    assert lst.pop() == 2
    assert lst.pop(0) == 1
    lst.remove(2)
    assert list(lst) == [3]
    lst.remove(3)
    assert list(lst) == []
    with pytest.raises(IndexError):
        lst.pop()
    with pytest.raises(ValueError):
        LinkedList([1]).remove(9)


def test_insert_sorted_keeps_equals_in_arrival_order() -> None:
    lst: LinkedList[int] = LinkedList()
    for value in (0, -1, 1, 1, 0):
        lst.insert_sorted(value)
    assert list(lst) == [-1, 0, 0, 1, 1]


def test_invalid_indexes() -> None:
    lst = LinkedList([1])
    with pytest.raises(IndexError):
        lst.node_at(1)
    with pytest.raises(IndexError):
        lst.insert(2, 5)
    with pytest.raises(IndexError):
        lst.pop(3)


def test_circular_list_iterates_once_and_rejects_appends() -> None:
    lst = LinkedList([1, 2, 3])
    lst.make_circular()
    assert list(lst) == [1, 2, 3]
    assert str(lst) == "1 --> 2 --> 3"
    assert lst.tail is not None and lst.tail.next is lst.head
    with pytest.raises(ValueError):
        lst.append(4)
    with pytest.raises(ValueError):
        lst.pop()


def test_make_circular_rejects_an_empty_list() -> None:
    with pytest.raises(ValueError):
        LinkedList().make_circular()


def test_refresh_rejects_a_cycle_that_does_not_return_to_the_head() -> None:
    lst = LinkedList([1, 2, 3])
    lst.node_at(2).next = lst.node_at(1)
    with pytest.raises(ValueError, match="Cycle does not return to the head"):
        lst.refresh()
