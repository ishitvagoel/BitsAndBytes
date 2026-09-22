"""Check that brackets in an expression are balanced.

The opening bracket of each pair is pushed. A closing bracket pops the stack
and must match that opening bracket. Any other character is ignored, so
``(a + [b])`` is checked the same way as ``([] )``.

The original map defined ``}`` twice, so ``'}': '('`` was overwritten by
``'}': '{'``, and ``>`` was used where ``)`` belongs. ``()``, ``[]``, ``{}``,
and ``<>`` are all recognized now.

An empty expression is balanced. A leftover opening bracket is not.
"""

from __future__ import annotations

# Closing bracket -> the opening bracket it must match.
CLOSING_TO_OPENING = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
OPENING = set(CLOSING_TO_OPENING.values())


def symbols_are_balanced(expression: str) -> bool:
    """Return whether every bracket in ``expression`` is correctly paired."""

    opening_stack: list[str] = []
    for character in expression:
        if character in OPENING:
            opening_stack.append(character)
            continue
        expected_opening = CLOSING_TO_OPENING.get(character)
        if expected_opening is None:
            continue
        # A closer with nothing open, or the wrong opener, fails immediately.
        if not opening_stack or opening_stack.pop() != expected_opening:
            return False
    return not opening_stack
