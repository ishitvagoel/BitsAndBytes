"""Linked-list algorithms, including the original sample inputs."""

import random

import pytest

from bitsandbytes import LinkedList
from bitsandbytes.linked_lists import (
    ReviewersList,
    find_cycle_start,
    find_intersection,
    is_palindrome,
    merge_sorted,
    merge_sorted_into,
    modular_node_from_end,
    modular_node_from_start,
    reverse_in_blocks,
    reverse_in_pairs,
    reverse_iterative,
    reverse_recursive,
    split_circular,
)


def test_reverse_iterative_and_recursive_round_trip() -> None:
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lst = LinkedList(values)
    reverse_iterative(lst)
    assert list(lst) == list(reversed(values))
    reverse_recursive(lst)
    assert list(lst) == values


def test_reverse_handles_empty_and_single_node_lists() -> None:
    empty: LinkedList[int] = LinkedList()
    reverse_iterative(empty)
    reverse_recursive(empty)
    assert list(empty) == []

    single = LinkedList([4])
    reverse_iterative(single)
    assert list(single) == [4]
    reverse_recursive(single)
    assert list(single) == [4]


def test_reverse_rejects_a_circular_list() -> None:
    lst = LinkedList([1, 2, 3])
    lst.make_circular()
    with pytest.raises(ValueError):
        reverse_iterative(lst)


def test_reverse_in_pairs_sample() -> None:
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7])
    reverse_in_pairs(lst)
    assert list(lst) == [2, 1, 4, 3, 6, 5, 7]


@pytest.mark.parametrize(
    ("values", "block", "remainder", "expected"),
    [
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            4,
            True,
            [4, 3, 2, 1, 8, 7, 6, 5, 12, 11, 10, 9, 15, 14, 13],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            3,
            True,
            [3, 2, 1, 6, 5, 4, 9, 8, 7, 12, 11, 10, 15, 14, 13],
        ),
        ([1, 2, 3], 10, True, [3, 2, 1]),
        ([1, 2, 3, 4, 5], 2, False, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 2, True, [2, 1, 4, 3, 5]),
        ([1, 2, 3, 4, 5], 3, False, [3, 2, 1, 4, 5]),
        ([1, 2, 3], 10, False, [1, 2, 3]),
    ],
)
def test_reverse_in_blocks(values, block, remainder, expected) -> None:
    lst = LinkedList(values)
    reverse_in_blocks(lst, block, reverse_remainder=remainder)
    assert list(lst) == expected


def test_reverse_in_blocks_rejects_non_positive_k() -> None:
    with pytest.raises(ValueError):
        reverse_in_blocks(LinkedList([1]), 0)


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], True),
        ([1], True),
        ([1, 2, 1, 2, 1], True),
        ([1, 1], True),
        ([1, 2], False),
        ([1, 2, 2, 1], True),
        ([1, 2, 2, 2, 2], False),
        ([1, 2, 3], False),
    ],
)
def test_palindrome(values: list[int], expected: bool) -> None:
    lst = LinkedList(values)
    assert is_palindrome(lst) is expected
    # The check reverses the second half temporarily and must restore it.
    assert list(lst) == values


def test_cycle_sample_and_acyclic_lists() -> None:
    lst = LinkedList([1, 2, 3, 4, 5])
    lst.node_at(4).next = lst.node_at(2)
    found = find_cycle_start(lst)
    assert found is not None
    position, node = found
    assert position == 3
    assert node.data == 3

    assert find_cycle_start(LinkedList()) is None
    assert find_cycle_start(LinkedList([1, 2, 3])) is None

    loop = LinkedList([7])
    assert loop.head is not None
    loop.head.next = loop.head
    assert find_cycle_start(loop) == (1, loop.head)

    pair = LinkedList([1, 2])
    pair.node_at(1).next = pair.head
    assert find_cycle_start(pair) == (1, pair.head)


def test_intersection_sample_and_miss() -> None:
    first = LinkedList([1, 2, 3, 4, 5, 6])
    second = LinkedList([1, 2])
    # Join at the node whose value is 4, without refreshing the cached length.
    second.node_at(1).next = first.node_at(3)
    shared = find_intersection(first, second)
    assert shared is not None
    assert shared.data == 4
    # require_linear rebuilds the cache from the spliced chain.
    assert len(second) == 5

    assert find_intersection(LinkedList([1, 2]), LinkedList([3, 4])) is None
    assert find_intersection(LinkedList(), LinkedList([1])) is None

    # The shared node is the head of the second list, not a later splice.
    tail = LinkedList([2, 3])
    front = LinkedList([1])
    assert front.head is not None
    front.head.next = tail.head
    assert find_intersection(front, tail) is tail.head


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ([1, 3, 5, 7, 9, 11, 23], [4, 6, 8, 10, 11, 11, 13, 14, 15, 16, 17, 24]),
        ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]),
        ([6, 7, 8, 9, 10], [6, 7, 8, 9, 10]),
        ([6, 7, 8, 9, 10], [1, 2, 3, 4, 5]),
        ([6, 7, 8, 9, 10], [1]),
        ([6, 7, 8, 9, 10], [11]),
        ([], [1, 2]),
        ([1, 2], []),
        ([], []),
    ],
)
def test_merge_sorted_samples(left: list[int], right: list[int]) -> None:
    left_list = LinkedList(left)
    right_list = LinkedList(right)
    merged = merge_sorted(left_list, right_list)
    assert list(merged) == sorted(left + right)
    assert list(left_list) == []
    assert list(right_list) == []

    destination = LinkedList(left)
    source = LinkedList(right)
    merge_sorted_into(destination, source)
    assert list(destination) == sorted(left + right)
    assert list(source) == []


def test_merge_sorted_rejects_merging_a_list_with_itself() -> None:
    lst = LinkedList([1, 2])
    with pytest.raises(ValueError):
        merge_sorted(lst, lst)
    with pytest.raises(ValueError):
        merge_sorted_into(lst, lst)
    assert list(lst) == [1, 2]


def test_split_circular_odd_and_even() -> None:
    odd = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    odd.make_circular()
    first, second = split_circular(odd)
    assert list(first) == [1, 2, 3, 4, 5, 6]
    assert list(second) == [7, 8, 9, 10, 11]
    assert first.tail is not None and first.tail.next is None
    assert second.tail is not None and second.tail.next is None

    even = LinkedList([1, 2, 3, 4])
    even.make_circular()
    left, right = split_circular(even)
    assert list(left) == [1, 2]
    assert list(right) == [3, 4]

    single = LinkedList([9])
    single.make_circular()
    head, rest = split_circular(single)
    assert list(head) == [9]
    assert list(rest) == []


def test_split_circular_rejects_a_linear_list() -> None:
    with pytest.raises(ValueError):
        split_circular(LinkedList([1, 2, 3]))


def test_modular_nodes_from_the_sample() -> None:
    lst = LinkedList([1, 2, 5, 111, 234, 51, 1])
    from_start = modular_node_from_start(lst, 3)
    assert from_start is not None
    position, node = from_start
    assert position == 6
    assert node.data == 51

    from_end = modular_node_from_end(lst, 3)
    assert from_end is not None
    end_position, end_node = from_end
    assert end_position == 6
    assert end_node.data == 2

    exact = LinkedList([1, 2, 3, 4, 5, 6])
    from_end_exact = modular_node_from_end(exact, 3)
    assert from_end_exact is not None
    assert from_end_exact[0] == 6
    assert from_end_exact[1].data == 1

    assert modular_node_from_start(lst, 8) is None
    assert modular_node_from_end(lst, 8) is None
    with pytest.raises(ValueError):
        modular_node_from_start(lst, 0)


def test_reviewer_rotation_inserts_new_people_after_the_cursor() -> None:
    reviewers = ReviewersList()
    with pytest.raises(RuntimeError):
        reviewers.next_reviewer()

    reviewers.add_reviewer("Sachin Tendulkar")
    assert reviewers.current_name == "Sachin Tendulkar"
    reviewers.add_reviewer("Michael Schumacher")
    reviewers.add_reviewer("Nadia Comaneci")
    reviewers.add_reviewer("Sergei Bubka")

    # Each add inserts just after the cursor, so the last person added is next.
    assert reviewers.next_reviewer().name == "Sergei Bubka"
    assert [person.name for person in reviewers] == [
        "Sachin Tendulkar",
        "Sergei Bubka",
        "Nadia Comaneci",
        "Michael Schumacher",
    ]
    assert reviewers.next_reviewer().name == "Nadia Comaneci"
    assert reviewers.next_reviewer().name == "Michael Schumacher"
    assert reviewers.next_reviewer().name == "Sachin Tendulkar"
    assert reviewers.next_reviewer().name == "Sergei Bubka"


def test_reverse_iterative_matches_python_on_random_lists() -> None:
    rng = random.Random(0)
    for _ in range(20):
        length = rng.randint(0, 12)
        values = [rng.randint(-5, 5) for _ in range(length)]
        lst = LinkedList(values)
        reverse_iterative(lst)
        assert list(lst) == list(reversed(values))


def test_merge_sorted_matches_sorted_concatenation() -> None:
    rng = random.Random(1)
    for _ in range(15):
        left_values = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        right_values = sorted(rng.randint(0, 9) for _ in range(rng.randint(0, 6)))
        left = LinkedList(left_values)
        right = LinkedList(right_values)
        merged = merge_sorted(left, right)
        assert list(merged) == sorted(left_values + right_values)
        assert list(left) == []
        assert list(right) == []
