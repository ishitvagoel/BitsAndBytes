# Bits and Bytes

Data structures and algorithms in Python 3.12+.

The implementations share one linked list and one stack instead of copying a
`Node` class into every file. Each algorithm module documents the approach,
the complexity, and the steps that are easy to misread.

## Layout

| Path | What it is |
| --- | --- |
| `bitsandbytes/linked_list.py` | Singly linked list used by every list algorithm |
| `bitsandbytes/sorting/` | Bubble, selection, insertion, merge, and quick sort |
| `bitsandbytes/stacks/` | Bounded stack, and bracket matching |
| `bitsandbytes/linked_lists/` | Reverse, palindrome, cycle, intersection, merge, split, modular nodes, reviewers |
| `bitsandbytes/decorators/` | Confirmation prompt, and permission checks |
| `bitsandbytes/tools/print_directory.py` | Top-down or bottom-up directory walk |

`print_directory_paths.py` still runs the directory walk.

## Try it

```bash
python -m bitsandbytes.tools.print_directory topdown
python -m bitsandbytes.decorators.permission
python -m bitsandbytes.decorators.access_control developer testdb
```

## Tests

```bash
python -m pip install pytest
pytest
```
