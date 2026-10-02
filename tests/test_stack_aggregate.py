"""Aggregate series for geometric growth inside ``Stack.push``."""

from __future__ import annotations

from bitsandbytes.stacks import Stack

_AGGREGATE_SERIES = (
    "the sizes 1, 2, 4, … sum to less than 2n and are bounded by twice the "
    "number of pushes"
)


def _compact(text: str | None) -> str:
    return " ".join((text or "").split())


def test_push_docstring_states_the_aggregate_series() -> None:
    assert _AGGREGATE_SERIES in _compact(Stack.push.__doc__)


def test_push_then_pop_one_value() -> None:
    stack: Stack[int] = Stack()
    assert stack.push(1) == 1
    assert stack.pop() == 1
