"""Curriculum gap-list rows 6–19 integration tests."""

from __future__ import annotations

from bitsandbytes.approximate.structures import BloomFilter, PersistentStackFrame, SkipList
from bitsandbytes.backtracking.search import combinations, n_queens_count, permutations, subsets
from bitsandbytes.dynamic_programming.classic import (
    edit_distance,
    fibonacci_modulo,
    knapsack_01,
    lis_length_patience,
    min_coin_change,
    word_break_possible,
)
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import has_directed_cycle, kosaraju_strongly_connected_components
from bitsandbytes.greedy.classic import fractional_knapsack_value, huffman_codes, interval_scheduling_max_count
from bitsandbytes.limits.approximation import vertex_cover_two_approximation
from bitsandbytes.patterns.arrays import PrefixSum, longest_unique_substring_length, two_sum_sorted
from bitsandbytes.range_queries.structures import FenwickTree, SegmentTree, SparseTable
from bitsandbytes.storage.engines import BTree, ToyLSM, nearest_neighbor_linear
from bitsandbytes.strings.algorithms import InvertedIndex, Trie, kmp_search, rabin_karp_search, run_length_encode
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree


def test_llrb_insert_rank_select_delete() -> None:
    tree: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    for value in range(8):
        tree.insert(value)
    assert tree.rank(5) == 5
    assert tree.select(3) == 3
    assert tree.delete(3)
    assert not tree.contains(3)
    assert tree.contains(4)


def test_dp_and_greedy_samples() -> None:
    assert fibonacci_modulo(10) == 55
    assert min_coin_change([1, 3, 4], 6) == 2
    assert knapsack_01([2, 3], [4, 5], 5) == 9
    assert edit_distance("kitten", "sitting") == 3
    assert lis_length_patience([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert word_break_possible("leetcode", ["leet", "code"])
    assert interval_scheduling_max_count([(1, 3, "a"), (2, 4, "b"), (3, 5, "c")]) == 2
    assert fractional_knapsack_value([10, 20], [60, 100], 50) == 160.0
    codes = huffman_codes({"a": 5, "b": 9, "c": 12})
    assert set(codes) == {"a", "b", "c"}


def test_backtracking_and_patterns() -> None:
    assert len(permutations([1, 2, 3])) == 6
    assert len(combinations([1, 2, 3, 4], 2)) == 6
    assert len(subsets([1, 2])) == 4
    assert n_queens_count(4) == 2
    assert two_sum_sorted([1, 2, 4, 7], 6) == (1, 2)
    assert longest_unique_substring_length("abcabcbb") == 3
    assert PrefixSum([1, 2, 3]).range_sum(1, 3) == 5


def test_strings_and_range_structures() -> None:
    trie = Trie()
    trie.insert("cat")
    assert trie.contains("cat")
    assert kmp_search("ababcabc", "abc") == 2
    assert rabin_karp_search("hello", "ll") == 2
    index = InvertedIndex()
    index.add_document(0, ["alpha", "beta"])
    assert index.query("beta") == [0]
    assert run_length_encode("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]
    tree = FenwickTree(5)
    tree.add(1, 3)
    assert tree.prefix_sum(1) == 3
    segment = SegmentTree([1, 2, 3])
    segment.range_add(0, 1, 2)
    assert segment.point_query(0) == 3
    sparse = SparseTable([4, 2, 7, 1])
    assert sparse.range_min(1, 3) == 1


def test_approximate_storage_and_limits() -> None:
    bloom = BloomFilter(bit_count=64)
    bloom.add("key")
    assert bloom.maybe_contains("key")
    skip: SkipList[int] = SkipList()
    skip.insert(3)
    assert skip.contains(3)
    stack = PersistentStackFrame(None, None)
    v1 = stack.push(1)
    v2 = v1.push(2)
    value, _previous = v2.pop()
    assert value == 2
    assert v1.top == 1
    btree: BTree[int] = BTree(branching=3)
    for key in range(10):
        btree.insert(key)
    assert btree.search(7)
    lsm = ToyLSM()
    for index in range(10):
        lsm.put(str(index))
    assert lsm.maybe_contains("3")
    assert nearest_neighbor_linear([(0, 0), (3, 4)], (3, 3)) == 1
    graph: Graph = Graph()
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 0, 1)
    assert has_directed_cycle(graph)
    dag: Graph = Graph()
    dag.add_edge("a", "b", 1)
    dag.add_edge("b", "c", 1)
    assert not has_directed_cycle(dag)
    components = kosaraju_strongly_connected_components(graph)
    assert len(components) == 1
    cover = vertex_cover_two_approximation(graph)
    assert len(cover) >= 1
