"""Directory walk."""

from pathlib import Path

import pytest

from bitsandbytes.tools.print_directory import format_tree, main


def test_format_tree_top_down_and_bottom_up(tmp_path: Path) -> None:
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    (nested / "c.txt").write_text("c", encoding="utf-8")
    (tmp_path / "top.txt").write_text("top", encoding="utf-8")

    top_down = format_tree(tmp_path, top_down=True)
    bottom_up = format_tree(tmp_path, top_down=False)

    def directories(text: str) -> list[str]:
        prefix = "Found Directory: "
        return [line.removeprefix(prefix) for line in text.splitlines() if line.startswith(prefix)]

    assert "\tc.txt" in top_down
    assert "\ttop.txt" in top_down
    assert directories(top_down)[0] == str(tmp_path)
    assert directories(top_down)[-1] == str(nested)
    assert directories(bottom_up)[0] == str(nested)
    assert directories(bottom_up)[-1] == str(tmp_path)


def test_format_tree_rejects_a_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        format_tree(tmp_path / "missing")


def test_main_defaults_to_top_down(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "note.txt").write_text("n", encoding="utf-8")
    main(["--root", str(tmp_path)])
    output = capsys.readouterr().out
    assert "Found Directory:" in output
    assert "\tnote.txt" in output


def test_main_rejects_an_unknown_order() -> None:
    with pytest.raises(SystemExit):
        main(["sideways"])
