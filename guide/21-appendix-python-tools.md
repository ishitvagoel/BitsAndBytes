---
title: Appendix: Python tools
slug: appendix-python-tools
order: 21
status: present
module: bitsandbytes.decorators.permission, bitsandbytes.decorators.access_control, bitsandbytes.tools.print_directory
---

These are not the next data-structure lesson after graphs. They stay in the repo as small Python examples.

* `decorators/permission.py` — wrapper is O(1) plus the wrapped call.
* `decorators/access_control.py` — expected O(1) permission lookup, then the action.
* `tools/print_directory.py` — `os.walk` is O(entries).

`print_directory_paths.py` still runs the directory walk.

## Industry

A working engineer wraps a function instead of copying its body.
`functools.wraps`, applied to the confirmation wrapper,
copies the wrapped callable's metadata onto the wrapper so the visible name
stays the original function's name. Walking a directory tree is `os.walk`,
which yields each directory top-down or bottom-up.
