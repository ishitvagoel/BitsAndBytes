"""Chaining hash table."""

import pytest

from bitsandbytes.hash_tables import ChainingHashTable


def test_chaining_hash_table_round_trip() -> None:
    table: ChainingHashTable[str, int] = ChainingHashTable(bucket_count=2)
    table["a"] = 1
    table["b"] = 2
    assert table["a"] == 1
    assert len(table) == 2
    del table["a"]
    with pytest.raises(KeyError):
        _ = table["a"]


def test_chaining_hash_table_rehash_keeps_entries() -> None:
    table: ChainingHashTable[int, str] = ChainingHashTable(bucket_count=2)
    for index in range(6):
        table[index] = str(index)
    for index in range(6):
        assert table[index] == str(index)
