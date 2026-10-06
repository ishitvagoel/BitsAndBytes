---
title: Stacks
slug: stacks
order: 4
status: present
module: bitsandbytes.stacks.stack, bitsandbytes.stacks.algorithm_stack, bitsandbytes.stacks.symbol_balance, bitsandbytes.stacks.min_stack, bitsandbytes.stacks.next_greater, bitsandbytes.stacks.stock_span, bitsandbytes.stacks.largest_rectangle, bitsandbytes.stacks.infix_postfix, bitsandbytes.stacks.sort_stack
---

This legacy page is the implementation inventory. Start with [stack basics](./stack-basics.md), then choose [monotonic stack patterns](./monotonic-stack-patterns.md) or [stack parsing and expressions](./stack-parsing-and-expressions.md) for focused overviews.

* `stacks/stack.py` — bounded stack: capacity, decorator guards, amortized O(1) `push`, O(1) `pop` and `peek`.
* `stacks/algorithm_stack.py` — unbounded LIFO for algorithm lessons. Same amortized costs without a limit check.
* `stacks/symbol_balance.py` — one pass. O(n) time, O(n) worst extra memory for openers.
* `stacks/min_stack.py` — second stack of minima. `push`, `pop`, and `minimum` are O(1).
* `stacks/next_greater.py` — monotonic stack. O(n) time, O(n) extra memory.
* `stacks/stock_span.py` — same monotonic pattern. O(n) time.
* `stacks/largest_rectangle.py` — histogram rectangle. O(n) time.
* `stacks/infix_postfix.py` — shunting yard plus postfix evaluation. O(n) time.
* `stacks/sort_stack.py` — one extra `AlgorithmStack`. Worst case O(n²) time, O(n) extra memory.

## Industry

A working engineer uses a Python `list` as a stack. The language tutorial
says to add with `append` and to retrieve with `pop()` and no index, so the
last item added is the first retrieved. The time-complexity documentation
lists an end `append` and an end `pop` as amortized O(1).
