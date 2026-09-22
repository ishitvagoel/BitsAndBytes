"""Infix to postfix, then evaluate the postfix.

The shunting-yard scan writes numbers straight to the output and holds
operators on a stack until a later operator of lower or equal precedence
forces them out. Parentheses are a sub-expression: ``(`` is stacked, and
``)`` pops down to the matching ``(``. Left associativity is the ``>=`` test:
``8/2/2`` becomes ``8 2 / 2 /``, not ``8 2 2 / /``.

Numbers are non-negative integers. ``+``, ``-``, ``*``, and ``/`` are binary.
``/`` is floor division. A unary minus is not an operator here; write
subtraction as a binary ``-``.
"""

from __future__ import annotations

from collections.abc import Sequence

_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}
_OPERATORS = set(_PRECEDENCE)


def infix_to_postfix(expression: str) -> list[str]:
    """Return the postfix tokens for an infix ``expression``.

    Cost
    ----
    Let n be the number of characters. Tokenizing visits each character
    once, so that pass is O(n) and produces t tokens with t <= n. The
    shunting-yard loop runs t times. Each token is pushed on the operator
    stack at most once and popped at most once, so the inner ``while``
    loops together run at most t times, not t times per token. Each step
    is O(1). Time is O(n). The operator stack and the output hold at most
    t tokens: O(n) extra memory.
    """

    output: list[str] = []
    operators: list[str] = []
    for token in _tokenize(expression):
        if token.isdigit():
            output.append(token)
            continue
        if token == "(":
            operators.append(token)
            continue
        if token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators:
                raise ValueError("Mismatched parentheses.")
            operators.pop()
            continue
        while (
            operators
            and operators[-1] != "("
            and _PRECEDENCE[operators[-1]] >= _PRECEDENCE[token]
        ):
            output.append(operators.pop())
        operators.append(token)
    while operators:
        operator = operators.pop()
        if operator == "(":
            raise ValueError("Mismatched parentheses.")
        output.append(operator)
    return output


def evaluate_postfix(tokens: Sequence[str]) -> int:
    """Evaluate postfix ``tokens`` and return the integer result.

    ``/`` uses floor division. Division by zero raises ``ZeroDivisionError``.
    A stack that does not end with exactly one value raises ``ValueError``.

    Cost
    ----
    Let t be ``len(tokens)``. The loop runs t times. A number is one
    ``int()`` and one append, both O(1) for the integers this parser emits
    (their digit count was already paid during tokenization). An operator
    pops two values, applies one arithmetic operation, and pushes the
    result: O(1). Time is O(t). The value stack holds at most t integers,
    so extra memory is O(t).
    """

    values: list[int] = []
    for token in tokens:
        if token in _OPERATORS:
            if len(values) < 2:
                raise ValueError(f"Operator {token!r} is missing an operand.")
            right = values.pop()
            left = values.pop()
            values.append(_apply(token, left, right))
        else:
            values.append(int(token))
    if len(values) != 1:
        raise ValueError("Expression does not leave a single result.")
    return values[0]


def evaluate_infix(expression: str) -> int:
    """Convert ``expression`` to postfix and evaluate it.

    Cost
    ----
    Let n be the number of characters. ``infix_to_postfix`` is O(n) and
    ``evaluate_postfix`` is O(t) for t <= n tokens. The sum is O(n). The
    postfix list and the value stack are O(n) extra memory.
    """

    return evaluate_postfix(infix_to_postfix(expression))


def _tokenize(expression: str) -> list[str]:
    """Split ``expression`` into numbers, operators, and parentheses.

    Cost
    ----
    Let n be ``len(expression)``. The index advances on every iteration,
    including through each digit of a number, so the loop runs n times.
    Each step inspects one character in O(1). Time is O(n). The token list
    holds at most n tokens: O(n) extra memory.
    """

    tokens: list[str] = []
    index = 0
    length = len(expression)
    while index < length:
        character = expression[index]
        if character.isspace():
            index += 1
            continue
        if character.isdigit():
            start = index
            index += 1
            while index < length and expression[index].isdigit():
                index += 1
            tokens.append(expression[start:index])
            continue
        if character in "()+-*/":
            tokens.append(character)
            index += 1
            continue
        raise ValueError(f"Unexpected character {character!r}.")
    return tokens


def _apply(operator: str, left: int, right: int) -> int:
    """Apply one binary operator.

    Cost
    ----
    One arithmetic operation. O(1) time and O(1) extra memory.
    """

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    return left // right
