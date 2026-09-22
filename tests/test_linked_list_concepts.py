"""The linked-list ideas that sit on top of reversal, cycles, and merges."""

import random

import pytest

from bitsandbytes import DoublyLinkedList, LinkedList
from bitsandbytes.linked_lists import (
    LRUCache,
    RandomNode,
    add_numbers,
    clone_interleaved,
    clone_with_map,
    delete_without_predecessor,
    group_by_position_parity,
    middle_node,
    nth_from_end,
    partition,
    remove_cycle,
    remove_nth_from_end,
    remove_sorted_duplicates,
    remove_unsorted_duplicates,
    reorder,
    rotate_right,
    sort_list,
)
from bitsandbytes.linked_lists.middle import end_of_first_half


def test_middle_nodes() -> None:
    assert middle_node(LinkedList()) is None

    single = middle_node(LinkedList([7]))
    assert single is not None and single.data == 7

    odd = LinkedList([1, 2, 3, 4, 5])
    odd_middle = middle_node(odd)
    assert odd.head is not None and odd_middle is not None
    assert odd_middle.data == 3
    assert end_of_first_half(odd.head).data == 3

    even = LinkedList([1, 2, 3, 4])
    even_middle = middle_node(even)
    assert even.head is not None and even_middle is not None
    # Second middle, versus the end of the left half.
    assert even_middle.data == 3
    assert end_of_first_half(even.head).data == 2


def test_nth_from_end_and_removal() -> None:
    lst = LinkedList([1, 2, 3, 4, 5])
    assert nth_from_end(lst, 1).data == 5
    assert nth_from_end(lst, 2).data == 4
    assert nth_from_end(lst, 5).data == 1

    assert remove_nth_from_end(lst, 2) == 4
    assert list(lst) == [1, 2, 3, 5]
    assert lst.tail is not None and lst.tail.data == 5

    assert remove_nth_from_end(lst, len(lst)) == 1
    assert list(lst) == [2, 3, 5]
    assert remove_nth_from_end(lst, 1) == 5
    assert list(lst) == [2, 3]

    with pytest.raises(ValueError):
        nth_from_end(LinkedList([1]), 2)
    with pytest.raises(ValueError):
        remove_nth_from_end(LinkedList(), 1)


def test_duplicates() -> None:
    sorted_values = LinkedList([1, 1, 2, 3, 3, 3])
    remove_sorted_duplicates(sorted_values)
    assert list(sorted_values) == [1, 2, 3]
    assert len(sorted_values) == 3

    unsorted = LinkedList([3, 1, 3, 2, 1, 2])
    remove_unsorted_duplicates(unsorted)
    assert list(unsorted) == [3, 1, 2]


def test_rotate_right() -> None:
    lst = LinkedList([1, 2, 3, 4, 5])
    rotate_right(lst, 2)
    assert list(lst) == [4, 5, 1, 2, 3]
    assert lst.tail is not None and lst.tail.data == 3

    rotate_right(lst, 5)
    assert list(lst) == [4, 5, 1, 2, 3]

    rotate_right(lst, -1)
    assert list(lst) == [5, 1, 2, 3, 4]

    single = LinkedList([1])
    rotate_right(single, 4)
    assert list(single) == [1]


def test_partition_preserves_group_order() -> None:
    lst = LinkedList([1, 4, 3, 2, 5, 2])
    partition(lst, 3)
    assert list(lst) == [1, 2, 2, 4, 3, 5]

    equals = LinkedList([3, 1, 3])
    partition(equals, 3)
    assert list(equals) == [1, 3, 3]


def test_group_odd_and_even_positions() -> None:
    lst = LinkedList([1, 2, 3, 4, 5])
    group_by_position_parity(lst)
    assert list(lst) == [1, 3, 5, 2, 4]

    even = LinkedList([1, 2, 3, 4])
    group_by_position_parity(even)
    assert list(even) == [1, 3, 2, 4]


def test_reorder_folds_the_ends_inward() -> None:
    odd = LinkedList([1, 2, 3, 4, 5])
    reorder(odd)
    assert list(odd) == [1, 5, 2, 4, 3]

    even = LinkedList([1, 2, 3, 4])
    reorder(even)
    assert list(even) == [1, 4, 2, 3]

    pair = LinkedList([1, 2])
    reorder(pair)
    assert list(pair) == [1, 2]


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
        ([5], [5], [0, 1]),
        ([9, 9], [1], [0, 0, 1]),
        ([], [], [0]),
        ([0], [], [0]),
    ],
)
def test_add_numbers(left: list[int], right: list[int], expected: list[int]) -> None:
    assert list(add_numbers(LinkedList(left), LinkedList(right))) == expected


def test_sort_list_is_stable_and_covers_short_runs() -> None:
    class Item:
        def __init__(self, key: int, label: str) -> None:
            self.key = key
            self.label = label

        def __lt__(self, other: object) -> bool:
            assert isinstance(other, Item)
            return self.key < other.key

    items = LinkedList([Item(1, "a"), Item(2, "b"), Item(1, "c")])
    sort_list(items)
    assert [item.label for item in items] == ["a", "c", "b"]

    for values in ([3, 1, 2], [5, 4, 3, 2, 1], [1], [], [2, 2, 1]):
        lst = LinkedList(values)
        sort_list(lst)
        assert list(lst) == sorted(values)

    rng = random.Random(0)
    mixed = list(range(20))
    rng.shuffle(mixed)
    lst = LinkedList(mixed)
    sort_list(lst)
    assert list(lst) == list(range(20))
    assert lst.tail is not None and lst.tail.data == 19


def test_remove_cycle_opens_the_loop() -> None:
    lst = LinkedList([1, 2, 3, 4, 5])
    lst.node_at(4).next = lst.node_at(2)
    assert remove_cycle(lst) is True
    assert list(lst) == [1, 2, 3, 4, 5]
    assert lst.tail is not None and lst.tail.next is None

    loop = LinkedList([7])
    assert loop.head is not None
    loop.head.next = loop.head
    assert remove_cycle(loop) is True
    assert list(loop) == [7]

    circle = LinkedList([1, 2, 3])
    circle.make_circular()
    assert remove_cycle(circle) is True
    assert list(circle) == [1, 2, 3]

    plain = LinkedList([1, 2])
    assert remove_cycle(plain) is False
    assert list(plain) == [1, 2]


def test_delete_without_predecessor_slides_the_successor_back() -> None:
    lst = LinkedList([1, 2, 3])
    assert lst.head is not None and lst.head.next is not None
    delete_without_predecessor(lst.head.next)
    lst.refresh()
    assert list(lst) == [1, 3]

    with pytest.raises(ValueError):
        assert lst.tail is not None
        delete_without_predecessor(lst.tail)


def test_doubly_linked_list_edits_and_reversal() -> None:
    lst = DoublyLinkedList([1, 3])
    assert lst.head is not None
    middle = lst.insert_after(lst.head, 2)
    lst.prepend(0)
    assert list(lst) == [0, 1, 2, 3]
    assert [node.data for node in _backward(lst)] == [3, 2, 1, 0]

    assert lst.remove_node(middle) == 2
    assert list(lst) == [0, 1, 3]
    assert lst.pop_tail() == 3
    lst.reverse()
    assert list(lst) == [1, 0]
    assert lst.tail is not None and lst.tail.data == 0

    assert lst.head is not None and lst.tail is not None
    lst.move_to_front(lst.tail)
    assert list(lst) == [0, 1]

    with pytest.raises(IndexError):
        DoublyLinkedList().pop_tail()


def test_lru_cache_evicts_the_least_recently_used_key() -> None:
    cache: LRUCache[int, str] = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    assert cache.get(1) == "a"
    cache.put(3, "c")
    assert cache.get(2) is None
    assert cache.get(1) == "a"
    assert cache.get(3) == "c"

    cache.put(1, "a2")
    assert cache.get(1) == "a2"
    cache.put(4, "d")
    assert cache.get(3) is None
    assert cache.get(1) == "a2"
    assert len(cache) == 2

    tiny: LRUCache[str, int] = LRUCache(1)
    tiny.put("a", 1)
    tiny.put("b", 2)
    assert tiny.get("a") is None
    assert tiny.get("b") == 2

    with pytest.raises(ValueError):
        LRUCache(0)


def test_random_pointer_clones_match_and_leave_the_original_intact() -> None:
    original = _random_chain([1, 2, 3], [2, 0, 1])
    # The middle node also points at itself, through the index above? index 1 -> 0.
    # Point the head at itself as well by editing after construction.
    assert original is not None
    original.random = original
    before = _snapshot(original)

    for clone in (clone_with_map(original), clone_interleaved(original)):
        assert clone is not original
        assert _snapshot(original) == before
        assert _snapshot(clone) == before
        assert _nodes(clone).isdisjoint(_nodes(original))

    assert clone_with_map(None) is None
    assert clone_interleaved(None) is None


def _backward(lst: DoublyLinkedList[int]) -> list:
    node = lst.tail
    values = []
    while node is not None:
        values.append(node)
        node = node.prev
    return values


def _random_chain(values: list[int], random_indexes: list[int | None]) -> RandomNode[int]:
    nodes = [RandomNode(value) for value in values]
    for index, node in enumerate(nodes[:-1]):
        node.next = nodes[index + 1]
    for index, target in enumerate(random_indexes):
        if target is not None:
            nodes[index].random = nodes[target]
    return nodes[0]


def _nodes(head: RandomNode[int] | None) -> set[int]:
    found: set[int] = set()
    current = head
    while current is not None and id(current) not in found:
        found.add(id(current))
        current = current.next
    return found


def _snapshot(head: RandomNode[int] | None) -> list[tuple[int, int | None]]:
    nodes: list[RandomNode[int]] = []
    current = head
    while current is not None:
        nodes.append(current)
        current = current.next
    index = {id(node): position for position, node in enumerate(nodes)}
    return [
        (node.data, None if node.random is None else index[id(node.random)])
        for node in nodes
    ]
