"""Bounded stack and bracket matching."""

import pytest

from bitsandbytes.stacks import (
    Stack,
    StackEmptyError,
    StackFullError,
    symbols_are_balanced,
)


def test_push_pop_and_peek_are_lifo() -> None:
    stack: Stack[str] = Stack(limit=3)
    assert stack.is_empty
    assert stack.push("a") == "a"
    stack.push("b")
    assert stack.peek() == "b"
    assert len(stack) == 2
    assert stack.pop() == "b"
    assert stack.pop() == "a"
    assert stack.is_empty


def test_full_stack_rejects_push() -> None:
    stack: Stack[int] = Stack(limit=1)
    stack.push(1)
    assert stack.is_full
    with pytest.raises(StackFullError):
        stack.push(2)
    assert stack.peek() == 1


def test_empty_stack_rejects_pop_and_peek() -> None:
    stack: Stack[int] = Stack()
    with pytest.raises(StackEmptyError):
        stack.pop()
    with pytest.raises(StackEmptyError):
        stack.peek()


def test_negative_limit_is_rejected() -> None:
    with pytest.raises(ValueError):
        Stack(limit=-1)


def test_decorators_keep_the_method_name() -> None:
    assert Stack.push.__name__ == "push"
    assert Stack.pop.__name__ == "pop"
    assert Stack.peek.__name__ == "peek"


@pytest.mark.parametrize(
    ("expression", "balanced"),
    [
        ("", True),
        ("()", True),
        ("([])", True),
        ("([{}])", True),
        ("<>", True),
        ("(a + [b])", True),
        ("{()}", True),
        (")(", False),
        ("(]", False),
        ("([)]", False),
        ("((", False),
        ("())", False),
        ("{)}", False),
        ("<", False),
    ],
)
def test_symbol_balance(expression: str, balanced: bool) -> None:
    assert symbols_are_balanced(expression) is balanced
