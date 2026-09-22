"""String structures and matching."""

from __future__ import annotations

from collections.abc import Iterable, Sequence


class Trie:
    """Prefix tree over string keys."""

    def __init__(self) -> None:
        """Create an empty trie.

        Cost
        ----
        O(1).
        """

        self._children: dict[str, dict] = {}

    def insert(self, key: str) -> None:
        """Insert ``key``.

        Cost
        ----
        O(len(key)) pointer hops.
        """

        node = self._children
        for char in key:
            node = node.setdefault(char, {})
        node["$"] = True

    def contains(self, key: str) -> bool:
        """Return whether ``key`` is stored.

        Cost
        ----
        O(len(key)).
        """

        node = self._children
        for char in key:
            if char not in node:
                return False
            node = node[char]
        return "$" in node


def kmp_search(text: str, pattern: str) -> int:
    """Return the first index of ``pattern`` in ``text``, or -1.

    Cost
    ----
    O(n + m) after O(m) failure-function construction.
    """

    if not pattern:
        return 0
    failure = _kmp_failure(pattern)
    state = 0
    for index, char in enumerate(text):
        while state > 0 and pattern[state] != char:
            state = failure[state - 1]
        if pattern[state] == char:
            state += 1
        if state == len(pattern):
            return index - len(pattern) + 1
    return -1


def _kmp_failure(pattern: str) -> list[int]:
    failure = [0] * len(pattern)
    length = 0
    index = 1
    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            failure[index] = length
            index += 1
        elif length:
            length = failure[length - 1]
        else:
            failure[index] = 0
            index += 1
    return failure


def rabin_karp_search(text: str, pattern: str, *, base: int = 256, mod: int = 10**9 + 7) -> int:
    """Return first match index using rolling hash (expected O(n + m)).

    Cost
    ----
    O(n + m) expected; O(nm) if every window collides on a bad modulus.
    """

    if not pattern:
        return 0
    if len(text) < len(pattern):
        return -1
    pattern_hash = 0
    window_hash = 0
    highest_power = 1
    for index, char in enumerate(pattern):
        pattern_hash = (pattern_hash * base + ord(char)) % mod
        if index < len(pattern) - 1:
            highest_power = (highest_power * base) % mod
    for char in text[: len(pattern)]:
        window_hash = (window_hash * base + ord(char)) % mod
    for start in range(len(text) - len(pattern) + 1):
        if window_hash == pattern_hash and text[start : start + len(pattern)] == pattern:
            return start
        if start + len(pattern) < len(text):
            window_hash = (
                (window_hash - ord(text[start]) * highest_power) * base + ord(text[start + len(pattern)])
            ) % mod
    return -1


class InvertedIndex:
    """Map terms to posting lists of document ids."""

    def __init__(self) -> None:
        self._postings: dict[str, list[int]] = {}

    def add_document(self, document_id: int, tokens: Iterable[str]) -> None:
        """Index one document.

        Cost
        ----
        O(total tokens) appends.
        """

        for token in tokens:
            self._postings.setdefault(token, []).append(document_id)

    def query(self, term: str) -> list[int]:
        """Return document ids containing ``term``.

        Cost
        ----
        O(length of posting list).
        """

        return list(self._postings.get(term, []))


def run_length_encode(text: str) -> list[tuple[str, int]]:
    """Return (character, count) runs.

    Cost
    ----
    O(n) single pass.
    """

    if not text:
        return []
    runs: list[tuple[str, int]] = []
    current = text[0]
    count = 1
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            runs.append((current, count))
            current = char
            count = 1
    runs.append((current, count))
    return runs


def suffix_array_with_lcp(text: str) -> tuple[list[int], list[int]]:
    """Return suffix array and LCP array by sorting suffixes.

    Cost
    ----
    O(n log² n) from Python's sort comparing suffix strings of length O(n).
    """

    suffixes = sorted(range(len(text)), key=lambda index: text[index:])
    lcp = [0] * len(suffixes)
    for index in range(1, len(suffixes)):
        first = text[suffixes[index - 1] :]
        second = text[suffixes[index] :]
        length = 0
        while length < len(first) and length < len(second) and first[length] == second[length]:
            length += 1
        lcp[index] = length
    return suffixes, lcp
