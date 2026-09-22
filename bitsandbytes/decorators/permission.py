"""Ask for a yes before the wrapped function runs.

The Python 2 script called ``raw_input`` and used ``print`` as a statement.
``input`` is the Python 3 equivalent. ``functools.wraps`` keeps the wrapped
function's name, which the log line prints.

Denied calls return ``None``. Allowed calls return whatever the function
returned; the old wrapper discarded that value.

``input_fn`` is injectable so tests do not have to type at a prompt. It has
the same shape as :func:`input`: it receives the prompt and returns the answer.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

_PROMPT = "Allow to proceed the execution (y/n)? "


def require_confirmation(
    function: Callable[P, R] | None = None,
    *,
    prompt: str = _PROMPT,
    input_fn: Callable[[str], str] | None = None,
) -> Callable[P, R | None] | Callable[[Callable[P, R]], Callable[P, R | None]]:
    """Decorate ``function`` so it runs only when the answer is ``y``.

    Use it as ``@require_confirmation`` or ``@require_confirmation(prompt=...)``.
    ``input_fn`` defaults to :func:`input`, resolved when the wrapper runs so
    tests can replace ``input`` without redecorating.
    """

    def decorate(fn: Callable[P, R]) -> Callable[P, R | None]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            read = input if input_fn is None else input_fn
            # Only an explicit yes proceeds. "yes" and an empty answer do not.
            if read(prompt).strip().lower() != "y":
                print("Method execution denied by the user.")
                return None
            result = fn(*args, **kwargs)
            print(
                f"Method {fn.__name__} executed with {len(args)} positional arguments"
            )
            return result

        return wrapper

    if function is not None:
        return decorate(function)
    return decorate


@require_confirmation
def show_arguments(*arguments: str) -> tuple[str, ...]:
    """Print and return the positional arguments. Used by the module CLI."""

    print(arguments)
    return arguments


def main(argv: list[str] | None = None) -> tuple[str, ...] | None:
    """Prompt, then print the CLI arguments when the answer is yes."""

    args = list(sys.argv[1:] if argv is None else argv)
    return show_arguments(*args)


if __name__ == "__main__":
    main()
