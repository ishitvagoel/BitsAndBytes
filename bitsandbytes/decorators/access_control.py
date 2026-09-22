"""Run an action only when the current user holds the required permission.

The permission map is the original sample data:

* ``admin`` may manage users
* ``developer`` may modify and read the database
* ``tester`` may read the database

The decorator closes over a :class:`UserContext` instead of reading
``sys.argv`` and looking the function up in ``globals()``. The CLI sets the
user, then calls the action. Tests set ``CONTEXT.user`` directly.

A missing permission raises :class:`PermissionError`.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping, Set
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

# User name -> permission strings that user holds.
PERMISSIONS: dict[str, frozenset[str]] = {
    "admin": frozenset({"admin"}),
    "developer": frozenset({"dev", "test"}),
    "tester": frozenset({"test"}),
}


class UserContext:
    """The user the access decorator checks, plus the permission table."""

    def __init__(self, permissions: Mapping[str, Set[str]]) -> None:
        self.permissions = permissions
        self.user: str | None = None

    def require(self, permission: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Build a decorator that allows ``permission`` for the current user."""

        def decorate(function: Callable[P, R]) -> Callable[P, R]:
            @wraps(function)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                granted = self.permissions.get(self.user or "", frozenset())
                if self.user is None or permission not in granted:
                    raise PermissionError(
                        f"{self.user!r} does not have permission {permission!r}."
                    )
                return function(*args, **kwargs)

            return wrapper

        return decorate


CONTEXT = UserContext(PERMISSIONS)


@CONTEXT.require("admin")
def manage_users() -> str:
    """Action ``manage``. Requires the ``admin`` permission."""

    message = "Managed Users successfully"
    print(message)
    return message


@CONTEXT.require("dev")
def modify_database() -> str:
    """Action ``modifydb``. Requires the ``dev`` permission."""

    message = "Modified Database successfully"
    print(message)
    return message


@CONTEXT.require("test")
def read_database() -> str:
    """Action ``testdb``. Requires the ``test`` permission."""

    message = "Read Database successfully"
    print(message)
    return message


ACTIONS: dict[str, Callable[[], str]] = {
    "manage": manage_users,
    "modifydb": modify_database,
    "testdb": read_database,
}


def run_action(user: str, action: str) -> str:
    """Run ``action`` as ``user`` and return the action's message.

    Unknown users and unknown actions raise ``KeyError``. A known user who
    lacks the action's permission raises ``PermissionError``.
    """

    if user not in PERMISSIONS:
        known_users = ", ".join(sorted(PERMISSIONS))
        raise KeyError(f"Unknown user {user!r}. Known users: {known_users}.")
    try:
        handler = ACTIONS[action]
    except KeyError:
        known_actions = ", ".join(sorted(ACTIONS))
        raise KeyError(f"Unknown action {action!r}. Known actions: {known_actions}.") from None
    CONTEXT.user = user
    return handler()


def main(argv: list[str] | None = None) -> None:
    """CLI: ``python -m bitsandbytes.decorators.access_control USER ACTION``."""

    parser = argparse.ArgumentParser(description="Run an action as a given user.")
    parser.add_argument("user", choices=sorted(PERMISSIONS))
    parser.add_argument("action", choices=sorted(ACTIONS))
    args = parser.parse_args(argv)
    run_action(args.user, args.action)


if __name__ == "__main__":
    main(sys.argv[1:])
