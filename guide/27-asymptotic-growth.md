---
title: Asymptotic growth
slug: asymptotic-growth
order: 27
status: present
module: bitsandbytes.complexity
---

## Compare how work grows

Asymptotic notation describes how cost changes as an input grows, ignoring fixed constants and lower-order terms. It is a model for comparison, not a stopwatch prediction.

**By the end of this overview, you can** distinguish upper, tight and lower bounds, and compare constant, logarithmic, linear, linearithmic and quadratic growth.

## Read the bounds precisely

`O(g(n))` is an upper bound up to a constant factor. `Ω(g(n))` is a lower bound. `Θ(g(n))` means both bounds hold, so the growth is tight. For `3n² + 10n + 8`, the quadratic term eventually dominates: the function is Θ(n²), and therefore also O(n²), O(n³), and so on. Saying O(n²) does not by itself prove tightness.

When input size doubles, a linear cost roughly doubles, a quadratic cost roughly quadruples, and a logarithmic cost increases by about one unit for base 2. These comparisons assume the same cost model and operation costs.

## Practice and next step

Classify `5n + 12` tightly and give one valid but loose upper bound. Then compare `n log₂ n` with `n²` for large `n`. Continue to [cost models and assumptions](./cost-models.md) before applying a bound to Python code.
