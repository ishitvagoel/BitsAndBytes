"""Add two non-negative integers stored as linked lists of digits.

Store the least significant digit at the head. Addition then starts at the
front of both lists, which is the only end a singly linked list can reach in
O(1). ``342 + 465`` is ``2 → 4 → 3`` plus ``5 → 6 → 4``, and the sum ``807``
is ``7 → 0 → 8``.

Each step adds the two digits and the carry, writes ``total % 10``, and keeps
``total // 10`` for the next step. The lists may differ in length. A final
carry becomes a new digit, so ``5 + 5`` is ``0 → 1``.

An empty list means zero. The sum of two zeros is a single node holding ``0``,
so the result always represents a number.

The inputs are not modified. Time O(n + m), extra memory O(n + m) for the sum.
"""

from __future__ import annotations

from bitsandbytes.linked_list import LinkedList, Node


def add_numbers(left: LinkedList[int], right: LinkedList[int]) -> LinkedList[int]:
    """Return the digit-wise sum of ``left`` and ``right``.

    Digits are non-negative integers. The usual representation uses ``0``
    through ``9``, but any non-negative digit works: the base is still 10.

    Cost
    ----
    Let n and m be the lengths. The loop runs once per digit of the longer
    number, plus one extra step when a final carry remains:
    max(n, m) + 1 iterations. Each iteration adds two digits and appends one
    result digit. Append is O(1). Time is O(n + m). The result list holds
    O(n + m) new nodes, which is the output, not scratch space. A few
    references and the carry are O(1) scratch memory.
    """

    left.require_linear()
    right.require_linear()
    result: LinkedList[int] = LinkedList()
    carry = 0
    left_node: Node[int] | None = left.head
    right_node: Node[int] | None = right.head
    while left_node is not None or right_node is not None or carry:
        total = carry
        if left_node is not None:
            total += left_node.data
            left_node = left_node.next
        if right_node is not None:
            total += right_node.data
            right_node = right_node.next
        if total < 0:
            raise ValueError("Digits must be non-negative.")
        result.append(total % 10)
        carry = total // 10
    if result.head is None:
        result.append(0)
    return result
