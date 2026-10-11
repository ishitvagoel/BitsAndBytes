"""Every teaching container supports len, iteration, membership, and repr."""

from __future__ import annotations

import pytest

from bitsandbytes.deques.linked_deque import LinkedDeque
from bitsandbytes.doubly_linked_list import DoublyLinkedList
from bitsandbytes.heaps.priority_queue import PriorityQueue
from bitsandbytes.linear.dynamic_array import DynamicArray
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.reviewers import ReviewersList
from bitsandbytes.queues.circular_queue import CircularQueue
from bitsandbytes.queues.linked_queue import LinkedQueue
from bitsandbytes.stacks.min_stack import MinStack
from bitsandbytes.stacks.stack import Stack
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree


def _stack() -> tuple[object, list[object], object, object, str]:
    container = Stack(limit=4)
    container.push(1)
    container.push(2)
    return container, [1, 2], 1, 9, "Stack([1, 2])"


def _min_stack() -> tuple[object, list[object], object, object, str]:
    container = MinStack()
    container.push(1)
    container.push(2)
    return container, [1, 2], 2, 9, "MinStack([1, 2])"


def _unbounded_stack() -> tuple[object, list[object], object, object, str]:
    container = Stack(limit=None)
    container.push(1)
    container.push(2)
    return container, [1, 2], 1, 9, "Stack([1, 2])"


def _linked_queue() -> tuple[object, list[object], object, object, str]:
    container = LinkedQueue()
    container.enqueue("a")
    container.enqueue("b")
    return container, ["a", "b"], "a", "z", "LinkedQueue(['a', 'b'])"


def _circular_queue() -> tuple[object, list[object], object, object, str]:
    container = CircularQueue(4)
    container.enqueue("a")
    container.enqueue("b")
    return container, ["a", "b"], "b", "z", "CircularQueue(['a', 'b'])"


def _deque() -> tuple[object, list[object], object, object, str]:
    container = LinkedDeque()
    container.append_right(1)
    container.append_right(2)
    return container, [1, 2], 1, 9, "LinkedDeque([1, 2])"


def _dynamic_array() -> tuple[object, list[object], object, object, str]:
    container = DynamicArray()
    container.append("a")
    container.append("b")
    return container, ["a", "b"], "a", "z", "DynamicArray(['a', 'b'])"


def _linked_list() -> tuple[object, list[object], object, object, str]:
    container = LinkedList()
    container.append(1)
    container.append(2)
    return container, [1, 2], 2, 9, "LinkedList([1, 2])"


def _doubly() -> tuple[object, list[object], object, object, str]:
    container = DoublyLinkedList()
    container.append(1)
    container.append(2)
    return container, [1, 2], 1, 9, "DoublyLinkedList([1, 2])"


def _priority() -> tuple[object, list[object], object, object, str]:
    container = PriorityQueue()
    container.push(1, "a")
    return container, ["a"], "a", "z", "PriorityQueue(['a'])"


def _reviewers() -> tuple[object, list[object], object, object, str]:
    container = ReviewersList()
    container.add_reviewer("Ada")
    return container, ["Ada"], "Ada", "Grace", "ReviewersList(['Ada'])"


def _tree() -> tuple[object, list[object], object, object, str]:
    container = LeftLeaningRedBlackTree()
    container.insert(2)
    container.insert(1)
    return container, [1, 2], 1, 9, "LeftLeaningRedBlackTree([1, 2])"


CASES = [
    ("stack", _stack, lambda: Stack(limit=2).pop()),
    ("min-stack", _min_stack, lambda: MinStack().pop()),
    ("unbounded-stack", _unbounded_stack, lambda: Stack(limit=None).pop()),
    ("linked-queue", _linked_queue, lambda: LinkedQueue().dequeue()),
    ("circular-queue", _circular_queue, lambda: CircularQueue(2).dequeue()),
    ("deque", _deque, lambda: LinkedDeque().pop_left()),
    ("dynamic-array", _dynamic_array, lambda: DynamicArray().pop()),
    ("linked-list", _linked_list, lambda: LinkedList().pop()),
    ("doubly-linked-list", _doubly, lambda: DoublyLinkedList().pop_tail()),
    ("priority-queue", _priority, lambda: PriorityQueue().pop()),
    ("reviewers", _reviewers, lambda: ReviewersList().current),
    ("red-black-tree", _tree, lambda: LeftLeaningRedBlackTree().select(0)),
]


@pytest.mark.parametrize(("name", "build", "empty_removal"), CASES, ids=[case[0] for case in CASES])
def test_container_protocol(name: str, build, empty_removal) -> None:
    container, items, present, absent, text = build()
    assert len(container) == len(items)
    observed = [getattr(item, "name", item) for item in container]
    assert observed == items
    assert present in container
    assert absent not in container
    assert repr(container) == text
    with pytest.raises(IndexError):
        empty_removal()
