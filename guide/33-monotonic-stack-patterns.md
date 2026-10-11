---
title: Monotonic stack patterns
slug: monotonic-stack-patterns
order: 33
status: present
module: bitsandbytes.stacks.next_greater, bitsandbytes.stacks.stock_span, bitsandbytes.stacks.largest_rectangle
---

## The idea

A monotonic stack stores indexes that are still waiting for an answer. next_greater on 2, 1, 2, 4, 3 returns 4, 2, 4, None, and None. The stack holds indexes. When a larger value arrives, every index it beats is popped and that value is written as the answer. Indexes that remain at the end have no strictly greater value on their right. stock_spans uses the same waiting stack. On prices 100, 80, 60, 70, 60, 75, 85 the span at the 75 is 4, because the walk stops at a strictly higher price. largest_rectangle asks for the nearest shorter bar on each side. The area is height times the gap between those bars. On 2, 1, 5, 6, 2, 3 the largest area is 10. min_stack keeps the current minimum beside the values. After pushing 3, then 1, then 2, the minimum is 1, and it is still 1 after 2 is popped. sort_stack uses a second stack so each moved value lands in order. The shared rule is that a value leaves the stack only when a later value resolves it.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Answers | first = 4 | next_greater writes the first strictly larger value on the right. |
| Area | area = 10 | The largest rectangle in this histogram has area 10. |

## Why it is correct

The stack stays ordered by the values at the stored indexes. A new value pops while the top is strictly smaller, so the top is the nearest unresolved candidate. Each pop writes an answer that will not change, because a later value is even farther to the right. The final leftovers are the positions with no greater neighbor, which is why their answers stay empty. The histogram uses two boundaries. A bar's width runs from the previous shorter bar to the next shorter bar, excluding those bars. Multiplying by the bar's height counts the rectangle that bar can support. The total work stays linear because each index is pushed once and popped at most once. The inner loop does not restart from the left.

## What it costs

n indexes produce at most n pushes and n pops, so the time is linear and the stack uses linear extra memory. A fresh scan from each index would be quadratic. largest_rectangle is the same bound. One pass finds the next smaller bar and one pass finds the previous smaller bar. min_stack push, pop, and minimum are constant time because the minimum is stored, not searched. Use this pattern when every item waits for a later item and then never waits again.

## Run it

```python
from bitsandbytes.stacks.next_greater import next_greater
print(next_greater([2, 1, 2, 4, 3]))
# prints: [4, 2, 4, None, None]
```

## Practice and next step

Answer the checkpoints, then open Stack parsing and expressions. The checkpoint stays in this browser.
