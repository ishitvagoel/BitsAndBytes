"""Push and pop return the stored item."""

from __future__ import annotations

from bitsandbytes.stacks import Stack


def test_push_then_pop_one_value() -> None:
    stack: Stack[int] = Stack()
    assert stack.push(1) == 1
    assert stack.pop() == 1
