"""Print the files under a directory, top-down or bottom-up."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def format_tree(root: Path | str = ".", *, top_down: bool = True) -> str:
    """Return the walk as ``Found Directory`` lines and tab-indented file names.

    ``top_down`` controls ``os.walk``: directories are listed before their
    children when it is true, and after them when it is false. Missing roots
    raise ``FileNotFoundError`` instead of printing nothing.

    Cost
    ----
    Let e be the number of directory entries under ``root`` (each directory
    and each file counted once). ``os.walk`` visits every directory once and
    yields each of its names once, so the walk is O(e). Each visit appends
    one line, amortized O(1) per entry, and joining the lines copies O(e)
    characters. Time is O(e). The returned string is the output, so extra
    memory is O(e). Checking that the root exists is O(1) before the walk.
    """

    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(root_path)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    lines: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root_path, topdown=top_down):
        lines.append(f"Found Directory: {dirpath}")
        for name in filenames:
            lines.append(f"\t{name}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    """Print a directory tree.

    The optional positional argument is ``topdown`` (the default) or
    ``bottomup``. ``--root`` selects the directory; it defaults to ``.``.

    Cost
    ----
    Parsing the two arguments is O(1). Printing the tree is proportional to
    the string ``format_tree`` already built, which is O(e) for e entries.
    """

    parser = argparse.ArgumentParser(description="Print a directory tree.")
    parser.add_argument(
        "order",
        nargs="?",
        choices=("topdown", "bottomup"),
        default="topdown",
        help="Visit each directory before its children (topdown) or after (bottomup).",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Directory to walk. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)
    print(format_tree(args.root, top_down=args.order == "topdown"))


if __name__ == "__main__":
    main(sys.argv[1:])
