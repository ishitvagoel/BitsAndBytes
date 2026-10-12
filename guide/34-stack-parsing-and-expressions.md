---
title: Stack parsing and expressions
slug: stack-parsing-and-expressions
order: 34
status: present
module: bitsandbytes.stacks.symbol_balance, bitsandbytes.stacks.min_stack, bitsandbytes.stacks.infix_postfix, bitsandbytes.stacks.sort_stack
---

## The idea

The string ([]) matches. The string ([)] does not. 2+3*4 is 14.

A bracket stack stores unmatched opening marks. symbols_are_balanced pushes each opener and pops when a closer arrives. The closer must match the current top. Other characters are ignored, so a formula and a bare bracket string share one checker. ([]) is balanced. ([)] is not, because the closer for the square bracket arrives while the parenthesis is still on top. An empty string is balanced. A leftover opener is not. Operator precedence uses a second stack. infix_to_postfix turns 2+3*4 into the tokens 2, 3, 4, *, +. Multiplication leaves the operator stack before addition because it binds more tightly. evaluate_infix of that expression returns 14. The value stack applies an operator only when both of its operands are already values. That is why postfix does not need parentheses.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Match | ok = true | ([]) is balanced. Each closer matches the top opener. |
| Cross | ok = false | ([)] is not balanced. The closer does not match the top. |
| Value | value = 14 | 2+3*4 evaluates to 14. Multiplication runs first. |

## Why it is correct

The bracket invariant is that the stack, from bottom to top, is the unmatched openers in the order they appeared. A matching closer restores the invariant by removing the top. A crossing closer breaks it, and the function returns false immediately. Termination with an empty stack means every opener found its closer. The operator invariant is that the operator stack is ordered by precedence, tightest at the top. Seeing a looser operator pops the tighter ones into the output first. The final pops drain the remaining operators. 3 * 4 happens before the addition with 2, so the value is 14.

## A common mistake

A later partner is not a match while another opener is still on top.

## What it costs

Each character is pushed or popped at most once, so both scans are linear in the length of the expression. Extra memory is the unmatched openers or the pending operators, which is linear in the worst case and small when the expression stays nested cleanly. A wrong match is a constant-time rejection. Do not scan backward for the opener. The stack already has it. Both scans are Θ(n) time and O(n) extra memory in the worst case.

## Run it

```python
from bitsandbytes.stacks.infix_postfix import evaluate_infix
print(evaluate_infix('2+3*4'))
# prints: 14
```

## Practice and next step

Open Queue and deque operations next. A queue removes the earliest item, which is the order a stack does not give you.
