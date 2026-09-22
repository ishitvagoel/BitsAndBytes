"""Confirmation and permission decorators."""

import pytest

from bitsandbytes.decorators.access_control import main as access_main
from bitsandbytes.decorators.access_control import run_action
from bitsandbytes.decorators.permission import main as permission_main
from bitsandbytes.decorators.permission import require_confirmation


def test_confirmation_runs_only_after_yes(capsys: pytest.CaptureFixture[str]) -> None:
    calls: list[int] = []

    @require_confirmation(input_fn=lambda _prompt: "y")
    def add(left: int, right: int) -> int:
        calls.append(1)
        return left + right

    assert add(2, 3) == 5
    assert calls == [1]
    output = capsys.readouterr().out
    assert "Method add executed with 2 positional arguments" in output


def test_confirmation_denies_anything_other_than_yes(capsys: pytest.CaptureFixture[str]) -> None:
    @require_confirmation(input_fn=lambda _prompt: "yes")
    def blocked() -> str:
        raise AssertionError("function should not run")

    assert blocked() is None
    assert "Method execution denied by the user." in capsys.readouterr().out


def test_permission_cli_prompts(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt: " Y ")
    assert permission_main(["a", "b"]) == ("a", "b")
    output = capsys.readouterr().out
    assert "('a', 'b')" in output
    assert "executed with 2 positional arguments" in output


@pytest.mark.parametrize(
    ("user", "action", "message"),
    [
        ("admin", "manage", "Managed Users successfully"),
        ("developer", "modifydb", "Modified Database successfully"),
        ("developer", "testdb", "Read Database successfully"),
        ("tester", "testdb", "Read Database successfully"),
    ],
)
def test_allowed_actions(user: str, action: str, message: str) -> None:
    assert run_action(user, action) == message


@pytest.mark.parametrize(
    ("user", "action"),
    [
        ("admin", "modifydb"),
        ("admin", "testdb"),
        ("tester", "manage"),
        ("tester", "modifydb"),
        ("developer", "manage"),
    ],
)
def test_denied_actions(user: str, action: str) -> None:
    with pytest.raises(PermissionError):
        run_action(user, action)


def test_unknown_user_and_action() -> None:
    with pytest.raises(KeyError, match="Unknown user"):
        run_action("guest", "manage")
    with pytest.raises(KeyError, match="Unknown action"):
        run_action("admin", "drop")


def test_access_cli_rejects_unknown_action() -> None:
    with pytest.raises(SystemExit):
        access_main(["admin", "drop"])
