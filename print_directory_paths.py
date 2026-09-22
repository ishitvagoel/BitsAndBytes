"""Backward-compatible entry point for the directory walk.

Prefer ``python -m bitsandbytes.tools.print_directory``.
"""

from bitsandbytes.tools.print_directory import main

if __name__ == "__main__":
    main()
