"""Backtracking search templates."""

from __future__ import annotations

from collections.abc import Callable


def permutations(items: list[int]) -> list[list[int]]:
    """Return all permutations of ``items``.

    Cost
    ----
    n! leaves, each O(n) to copy: O(n · n!) time. Recursion depth n.
    """

    output: list[list[int]] = []

    def extend(path: list[int], remaining: list[int]) -> None:
        if not remaining:
            output.append(path.copy())
            return
        for index, value in enumerate(remaining):
            path.append(value)
            extend(path, remaining[:index] + remaining[index + 1 :])
            path.pop()

    extend([], items)
    return output


def combinations(items: list[int], choose: int) -> list[list[int]]:
    """Return all ``choose``-element subsets in increasing index order.

    Cost
    ----
    C(n, k) outputs, recursion depth k.
    """

    output: list[list[int]] = []

    def extend(start: int, path: list[int]) -> None:
        if len(path) == choose:
            output.append(path.copy())
            return
        for index in range(start, len(items)):
            path.append(items[index])
            extend(index + 1, path)
            path.pop()

    extend(0, [])
    return output


def subsets(items: list[int]) -> list[list[int]]:
    """Return all subsets.

    Cost
    ----
    2^n subsets, O(n) work per subset in the worst case.
    """

    output: list[list[int]] = []

    def extend(index: int, path: list[int]) -> None:
        if index == len(items):
            output.append(path.copy())
            return
        extend(index + 1, path)
        path.append(items[index])
        extend(index + 1, path)
        path.pop()

    extend(0, [])
    return output


def n_queens_count(board_size: int) -> int:
    """Return the number of solutions to N-queens.

    Cost
    ----
    Exponential in ``board_size`` in the worst case; pruning does not change
    the worst-case tree size in theory. Recursion depth ``board_size``.
    """

    columns: set[int] = set()
    diag_a: set[int] = set()
    diag_b: set[int] = set()

    def place(row: int) -> int:
        if row == board_size:
            return 1
        total = 0
        for column in range(board_size):
            if column in columns or (row - column) in diag_a or (row + column) in diag_b:
                continue
            columns.add(column)
            diag_a.add(row - column)
            diag_b.add(row + column)
            total += place(row + 1)
            columns.remove(column)
            diag_a.remove(row - column)
            diag_b.remove(row + column)
        return total

    return place(0)


def backtrack_find(
    candidates: list[int],
    target: int,
    combine: Callable[[list[int], int], bool],
) -> list[list[int]]:
    """Generic backtracking when ``combine(path, remaining)`` prunes extensions.

    Cost
    ----
    Depends on ``combine``; worst case explores the full subset tree.
    """

    output: list[list[int]] = []

    def extend(index: int, path: list[int], remaining: int) -> None:
        if remaining == 0:
            output.append(path.copy())
            return
        if index == len(candidates) or not combine(path, remaining):
            return
        extend(index + 1, path, remaining)
        value = candidates[index]
        if value <= remaining:
            path.append(value)
            extend(index, path, remaining - value)
            path.pop()

    extend(0, [], target)
    return output
