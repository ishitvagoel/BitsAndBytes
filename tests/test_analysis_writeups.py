"""Literal results for the three recurrence shapes and three traced routines."""

from __future__ import annotations

from bitsandbytes.complexity import RecurrenceShape, classify_recurrence
from bitsandbytes.linked_list import LinkedList
from bitsandbytes.linked_lists.cycle import find_cycle_start
from bitsandbytes.stacks.infix_postfix import evaluate_infix, infix_to_postfix
from bitsandbytes.stacks.largest_rectangle import largest_rectangle


def test_classify_recurrence_bounds() -> None:
    assert classify_recurrence(RecurrenceShape.MERGE_DIVIDE) == "Θ(n log n)"
    assert classify_recurrence(RecurrenceShape.HALVING) == "Θ(log n)"
    assert classify_recurrence(RecurrenceShape.LINEAR_DECREMENT) == "Θ(n²)"


def test_cycle_histogram_and_infix_results() -> None:
    chain = LinkedList([1, 2, 3, 4, 5])
    chain.node_at(4).next = chain.node_at(2)
    index, node = find_cycle_start(chain)
    assert index == 3
    assert node is not None and node.data == 3
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert infix_to_postfix("1+2*3") == ["1", "2", "3", "*", "+"]
    assert evaluate_infix("1+2*3") == 7
