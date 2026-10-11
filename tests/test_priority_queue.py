"""Priority queue with decrease-key."""

from bitsandbytes.heaps.priority_queue import PriorityQueue


def test_priority_queue_empty() -> None:
    queue: PriorityQueue[str] = PriorityQueue()
    token = queue.push(5, "a")
    assert queue.peek() == (5, "a")
    queue.decrease_key(token, 1)
    assert queue.pop() == (1, "a")


def test_decrease_key_rejects_an_equal_priority() -> None:
    queue: PriorityQueue[str] = PriorityQueue()
    token = queue.push(5, "a")
    try:
        queue.decrease_key(token, 5)
    except ValueError as error:
        assert "strictly smaller" in str(error)
    else:
        raise AssertionError("equal priority must be rejected")
    assert queue.pop() == (5, "a")


def test_priority_queue_order() -> None:
    queue: PriorityQueue[int] = PriorityQueue()
    queue.push(10, 1)
    queue.push(3, 2)
    queue.push(7, 3)
    assert queue.pop()[0] == 3
    assert queue.pop()[0] == 7
