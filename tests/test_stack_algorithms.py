"""Min stack, monotonic-stack scans, infix evaluation, and stack sorting."""

import pytest

from bitsandbytes.stacks import (
    MinStack,
    Stack,
    StackEmptyError,
    evaluate_infix,
    evaluate_postfix,
    infix_to_postfix,
    largest_rectangle,
    next_greater,
    sort_stack,
    stock_spans,
)


def test_min_stack_tracks_the_minimum_through_pushes_and_pops() -> None:
    stack = MinStack()
    stack.push(3)
    stack.push(1)
    stack.push(2)
    assert stack.minimum() == 1
    assert stack.peek() == 2
    assert stack.pop() == 2
    assert stack.minimum() == 1
    assert stack.pop() == 1
    assert stack.minimum() == 3
    assert len(stack) == 1


def test_min_stack_keeps_an_earlier_copy_of_a_duplicate_minimum() -> None:
    stack = MinStack()
    stack.push(2)
    stack.push(1)
    stack.push(1)
    assert stack.minimum() == 1
    stack.pop()
    assert stack.minimum() == 1
    stack.pop()
    assert stack.minimum() == 2


def test_min_stack_rejects_reads_when_empty() -> None:
    stack = MinStack()
    with pytest.raises(StackEmptyError):
        stack.pop()
    with pytest.raises(StackEmptyError):
        stack.peek()
    with pytest.raises(StackEmptyError):
        stack.minimum()


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], []),
        ([1], [None]),
        ([2, 1, 2, 4, 3], [4, 2, 4, None, None]),
        ([1, 1, 1], [None, None, None]),
        ([1, 3, 2], [3, None, None]),
        ([5, 4, 3], [None, None, None]),
    ],
)
def test_next_greater(values: list[int], expected: list[int | None]) -> None:
    assert next_greater(values) == expected


@pytest.mark.parametrize(
    ("prices", "expected"),
    [
        ([], []),
        ([10], [1]),
        ([100, 80, 60, 70, 60, 75, 85], [1, 1, 1, 2, 1, 4, 6]),
        ([5, 4, 3], [1, 1, 1]),
        ([1, 2, 3], [1, 2, 3]),
        ([2, 2, 2], [1, 2, 3]),
    ],
)
def test_stock_spans(prices: list[int], expected: list[int]) -> None:
    assert stock_spans(prices) == expected


@pytest.mark.parametrize(
    ("heights", "area"),
    [
        ([], 0),
        ([2], 2),
        ([0, 0], 0),
        ([1, 1, 1], 3),
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 0, 2], 2),
        ([6, 2, 5, 4, 5, 1, 6], 12),
        ([1, 2, 3, 4], 6),
    ],
)
def test_largest_rectangle(heights: list[int], area: int) -> None:
    assert largest_rectangle(heights) == area


def test_infix_to_postfix_respects_precedence_and_parentheses() -> None:
    assert infix_to_postfix("2+3*4") == ["2", "3", "4", "*", "+"]
    assert infix_to_postfix("(2+3)*4") == ["2", "3", "+", "4", "*"]
    assert infix_to_postfix("8/2/2") == ["8", "2", "/", "2", "/"]
    assert infix_to_postfix("2 - 3 + 4") == ["2", "3", "-", "4", "+"]


def test_evaluate_infix_and_postfix() -> None:
    assert evaluate_infix("2+3*4") == 14
    assert evaluate_infix("(2+3)*4") == 20
    assert evaluate_infix("8/2/2") == 2
    assert evaluate_infix("2 - 3 + 4") == 3
    assert evaluate_postfix(["2", "3", "4", "*", "+"]) == 14


def test_infix_rejects_bad_tokens_and_parentheses() -> None:
    with pytest.raises(ValueError):
        infix_to_postfix("2 + a")
    with pytest.raises(ValueError):
        infix_to_postfix("(2+3")
    with pytest.raises(ValueError):
        infix_to_postfix("2+3)")
    with pytest.raises(ValueError):
        evaluate_postfix(["+", "1"])
    with pytest.raises(ZeroDivisionError):
        evaluate_infix("1/0")


def test_sort_stack_leaves_the_smallest_on_top() -> None:
    stack: Stack[int] = Stack(limit=5)
    for item in (3, 1, 4, 1, 2):
        stack.push(item)
    assert sort_stack(stack) is stack
    assert [stack.pop() for _ in range(len(stack))] == [1, 1, 2, 3, 4]


def test_sort_stack_handles_empty_and_single_item() -> None:
    empty: Stack[int] = Stack()
    sort_stack(empty)
    assert empty.is_empty

    single: Stack[str] = Stack(limit=1)
    single.push("only")
    sort_stack(single)
    assert single.pop() == "only"


def test_sort_stack_already_sorted_and_reversed() -> None:
    ascending: Stack[int] = Stack(limit=4)
    for item in (4, 3, 2, 1):
        ascending.push(item)
    sort_stack(ascending)
    assert [ascending.pop() for _ in range(4)] == [1, 2, 3, 4]

    descending: Stack[int] = Stack(limit=4)
    for item in (1, 2, 3, 4):
        descending.push(item)
    sort_stack(descending)
    assert [descending.pop() for _ in range(4)] == [1, 2, 3, 4]
