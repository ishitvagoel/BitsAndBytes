"""Asymptotic analysis for this course.

Worked trace (classify ``MERGE_DIVIDE`` for n = 8):

* Level 0: one problem of size 8 costs O(8) to combine.
* Level 1: two problems of size 4, each with O(4) combine work.
* Level 2: four problems of size 2.
* Level 3: eight base cases of size 1.
* There are log2(8) + 1 = 4 levels. The combine work at level i is 2**i *
  O(8 / 2**i) = O(8). Summing over levels gives O(n log n).

Cost model
----------
The **word RAM** counts one step for a pointer write, a comparison, a hash of
a fixed-size key, or an arithmetic operation on a machine word. That model is
an assumption, not a law of physics.

CPython ``int`` values grow with the number of bits. Adding two integers with
Θ(n) bits is not O(1) in n. Core modules that need fixed-width arithmetic say
so explicitly (for example Fibonacci modulo a word in the dynamic-programming
chapter).

CPython does not eliminate tail calls. The default recursion limit is 1000
(see ``recursion_limit``). Recursive algorithms in this repository state
call-stack memory separately from loop-only memory.
"""

from __future__ import annotations

import sys
from enum import Enum


class RecurrenceShape(Enum):
    """The three recurrence shapes used throughout the repository."""

    MERGE_DIVIDE = "2T(n/2) + O(n)"
    HALVING = "T(n/2) + O(1)"
    LINEAR_DECREMENT = "T(n-1) + O(n)"


_BOUND_VOCABULARY: dict[str, str] = {
    "O": "Upper bound: f(n) is O(g(n)) when f grows no faster than g up to a constant factor.",
    "Theta": "Tight bound: f(n) is Θ(g(n)) when f is sandwiched between constant multiples of g.",
    "Omega": "Lower bound: f(n) is Ω(g(n)) when f grows at least as fast as g up to a constant factor.",
}


def bound_vocabulary() -> dict[str, str]:
    """Return short definitions of O, Θ, and Ω.

    Cost
    ----
    The dictionary is fixed size: O(1) time and O(1) extra memory.
    """

    return dict(_BOUND_VOCABULARY)


def recursion_limit() -> int:
    """Return CPython's current recursion depth limit.

    Cost
    ----
    One interpreter attribute read: O(1).
    """

    return sys.getrecursionlimit()


def classify_recurrence(shape: RecurrenceShape) -> str:
    """Return the Θ bound taught for ``shape``.

    Only the three shapes in ``RecurrenceShape`` are classified. This helper
    is not a general recurrence solver (Akra–Bazzi is out of scope).

    Cost
    ----
    A constant-size table lookup: O(1) time and O(1) extra memory.
    """

    table = {
        RecurrenceShape.MERGE_DIVIDE: "Θ(n log n)",
        RecurrenceShape.HALVING: "Θ(log n)",
        RecurrenceShape.LINEAR_DECREMENT: "Θ(n²)",
    }
    return table[shape]
