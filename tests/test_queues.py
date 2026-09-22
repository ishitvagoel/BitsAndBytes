"""Queue implementations."""

import pytest

from bitsandbytes.queues import CircularQueue, LinkedQueue


def test_linked_queue_fifo_order() -> None:
    queue: LinkedQueue[str] = LinkedQueue()
    queue.enqueue("a")
    queue.enqueue("b")
    assert queue.peek() == "a"
    assert queue.dequeue() == "a"
    assert queue.dequeue() == "b"
    assert queue.is_empty


def test_linked_queue_empty_errors() -> None:
    queue: LinkedQueue[int] = LinkedQueue()
    with pytest.raises(IndexError):
        queue.dequeue()
    with pytest.raises(IndexError):
        queue.peek()


def test_circular_queue_wraps_and_rejects_overflow() -> None:
    queue: CircularQueue[int] = CircularQueue(capacity=2)
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.is_full
    with pytest.raises(IndexError):
        queue.enqueue(3)
    assert queue.dequeue() == 1
    queue.enqueue(3)
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3
