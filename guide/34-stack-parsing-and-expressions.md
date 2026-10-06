---
title: Stack parsing and expressions
slug: stack-parsing-and-expressions
order: 34
status: present
module: bitsandbytes.stacks.symbol_balance, bitsandbytes.stacks.min_stack, bitsandbytes.stacks.infix_postfix, bitsandbytes.stacks.sort_stack
---

## Match nested structure with a stack

When a later symbol must match the most recent unmatched opener, last-in, first-out order fits naturally. Push open brackets; when a closer arrives, compare it with the top and remove the match. A mismatch or leftover opener means the expression is unbalanced.

**By the end of this overview, you can** connect nested parsing to stack order and trace how a precedence-aware conversion delays operators.

## A small expression trace

For `2 + 3 × 4`, multiplication has higher precedence, so a conversion to postfix emits `2 3 4 × +`. The operator stack temporarily holds `+` while reading the multiplication, then emits `×` before `+`. Parentheses act as explicit boundaries for when operators leave the stack.

A one-pass parser takes O(n) time in the input length and can store O(n) openers or operators. A minimum-stack variant keeps a second stack of candidate minima so each minimum query is O(1), at the cost of additional O(n) storage in the worst case. Always define behavior for empty input, unmatched delimiters and unsupported tokens.

## Practice and next step

Trace the opener stack for `([{}])` and for `([)]`. Then write the operator stack at each symbol in `2 + 3 × 4`. Compare with [the repository stack tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_stacks.py).
