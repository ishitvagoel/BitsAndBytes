"""Substitution sentences and the three loop-invariant sentences."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

import bitsandbytes.complexity as complexity
from bitsandbytes.complexity import classify_recurrence

cycle = import_module("bitsandbytes.linked_lists.cycle")
histogram = import_module("bitsandbytes.stacks.largest_rectangle")
shunting_yard = import_module("bitsandbytes.stacks.infix_postfix")

_MERGE_DIVIDE = (
    "Substitution for the merge-divide recurrence ``T(n) = 2T(n/2) + O(n)`` "
    "plugs ``T(n/2) <= c (n/2) log2(n/2)`` into the recurrence and gets "
    "``T(n) <= c n log2(n)`` when ``c`` is at least the hidden constant in "
    "the ``O(n)`` combine, the same bound ``merge_sort`` derives."
)
_HALVING = (
    "Substitution for the halving recurrence ``T(n) = T(n/2) + O(1)`` plugs "
    "``T(n/2) <= c log2(n/2)`` into the recurrence and gets "
    "``T(n) <= c log2(n)`` when ``c`` is at least the hidden constant in the "
    "``O(1)`` work, the same bound binary search derives."
)
_LINEAR_DECREMENT = (
    "Substitution for the linear-decrement recurrence "
    "``T(n) = T(n - 1) + O(n)``, the linear decrement behind the quicksort "
    "worst split, plugs ``T(n - 1) <= c (n - 1) ** 2`` into the recurrence "
    "and gets ``T(n) <= c n ** 2`` when ``c`` is large enough to cover the "
    "linear scan."
)
_FLOYD = (
    "The invariant is that the fast pointer has taken twice as many steps as "
    "the slow pointer, so they meet only inside the cycle."
)
_HISTOGRAM = (
    "The invariant is that stack heights stay strictly increasing from bottom "
    "to top."
)
_SHUNTING_YARD = (
    "The invariant is that the output holds the postfix of tokens already "
    "flushed, and inside the current parenthesis group the operator stack "
    "increases in precedence from bottom to top."
)


def _compact(text: str | None) -> str:
    return " ".join((text or "").split())


def test_substitution_sentences() -> None:
    module_doc = _compact(complexity.__doc__)
    classifier_doc = _compact(classify_recurrence.__doc__)
    for sentence in (_MERGE_DIVIDE, _HALVING, _LINEAR_DECREMENT):
        assert sentence in module_doc
        assert sentence in classifier_doc


def test_invariant_sentences() -> None:
    traces = (
        (cycle, _FLOYD),
        (histogram, _HISTOGRAM),
        (shunting_yard, _SHUNTING_YARD),
    )
    for module, sentence in traces:
        document = module.__doc__ or ""
        source = Path(module.__file__ or "").read_text(encoding="utf-8")
        assert sentence in _compact(document)
        assert source.count("invariant") == 1
