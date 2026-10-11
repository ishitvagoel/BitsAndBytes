from bitsandbytes.heaps.heapsort import heapify
from bitsandbytes.sorting.merge_sort import merge_sort
from bitsandbytes.tracing import TraceEvent


def test_merge_sort_emits_the_split_and_each_take():
    events: list[TraceEvent] = []
    assert merge_sort([3, 1], trace_sink=events.append) == [1, 3]
    assert [event.kind for event in events] == ["split", "take", "take"]
    assert events[0].values == {"left": [3], "right": [1]}
    assert events[1].values["value"] == 1
    assert events[2].values["merged"] == [1, 3]


def test_merge_sort_without_a_sink_still_returns_the_sorted_list():
    assert merge_sort([3, 1, 4, 2]) == [1, 2, 3, 4]


def test_heapify_emits_one_sift_per_parent():
    events: list[TraceEvent] = []
    values = [3, 1, 4, 2]
    heapify(values, trace_sink=events.append)
    assert values == [4, 2, 3, 1]
    assert [event.kind for event in events] == ["sift", "sift"]
    assert events[-1].values["values"] == [4, 2, 3, 1]
