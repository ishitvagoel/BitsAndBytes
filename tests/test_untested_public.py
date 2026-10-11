from bitsandbytes.backtracking.search import backtrack_find
from bitsandbytes.dynamic_programming.classic import (
    dag_dp_longest_path,
    lis_length_quadratic,
    longest_common_subsequence,
    max_non_adjacent_sum,
    unbounded_knapsack_max_value,
)
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import UndirectedGraph, connected_components, prim_minimum_spanning_weight
from bitsandbytes.patterns.arrays import sliding_window_maximum
from bitsandbytes.stacks.algorithm_stack import AlgorithmStack
from bitsandbytes.storage.engines import WriteAheadLog, locality_scan_benchmark, sequential_scan_sum
from bitsandbytes.strings.algorithms import suffix_array_with_lcp
from bitsandbytes.trees.bst import TreeNode
from bitsandbytes.trees.llrb import LeftLeaningRedBlackTree
from bitsandbytes.trees.traversals import map_inorder


def test_connected_components_splits_an_unreachable_vertex():
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_vertex("C")
    assert connected_components(graph) == [["A", "B"], ["C"]]


def test_prim_minimum_spanning_weight_adds_the_two_lightest_edges():
    graph = UndirectedGraph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 9)
    assert prim_minimum_spanning_weight(graph, "A") == 3


def test_longest_common_subsequence_counts_shared_letters_in_order():
    assert longest_common_subsequence("abc", "ac") == 2


def test_lis_length_quadratic_skips_the_descending_prefix():
    assert lis_length_quadratic([3, 1, 2]) == 2


def test_max_non_adjacent_sum_takes_the_ends():
    assert max_non_adjacent_sum([3, 2, 5]) == 8


def test_unbounded_knapsack_reuses_the_lighter_item():
    assert unbounded_knapsack_max_value([1, 3], [2, 4], 4) == 8


def test_dag_dp_longest_path_adds_the_heavier_route():
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("A", "C", 1)
    graph.add_edge("B", "C", 4)
    assert dag_dp_longest_path(graph, "A") == 6


def test_sliding_window_maximum_keeps_the_largest_visible_value():
    assert sliding_window_maximum([1, 3, 2, 5], 2) == [3, 3, 5]


def test_suffix_array_with_lcp_sorts_banana_suffixes():
    suffixes, lcp = suffix_array_with_lcp("banana")
    assert suffixes == [5, 3, 1, 0, 4, 2]
    assert lcp == [0, 1, 3, 0, 0, 2]


def test_backtrack_find_lists_combinations_that_sum_to_the_target():
    found = backtrack_find([2, 3], 5, lambda _path, _remaining: True)
    assert found == [[2, 3]]


def test_map_inorder_visits_bst_values_in_order():
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    seen: list[int] = []
    map_inorder(root, seen.append)
    assert seen == [1, 2, 3]


def test_algorithm_stack_pops_the_last_push():
    stack = AlgorithmStack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_write_ahead_log_replays_a_put_into_the_tree():
    log = WriteAheadLog()
    log.append("put", "a")
    table = LeftLeaningRedBlackTree()
    log.replay(table)
    assert table.inorder() == ["a"]


def test_sequential_scan_sum_adds_every_value():
    assert sequential_scan_sum([1, 2, 3]) == 6


def test_locality_scan_benchmark_returns_a_non_negative_duration():
    duration = locality_scan_benchmark([1, 2, 3], repeats=1)
    assert isinstance(duration, float)
    assert duration >= 0
