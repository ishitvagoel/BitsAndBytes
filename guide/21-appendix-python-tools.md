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
