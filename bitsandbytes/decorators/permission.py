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

    Cost
    ----
    Building the decorator is O(1). Each later call pays the wrapper's cost
    plus the wrapped function. The wrapper itself is O(1) beyond that call:
    one prompt, one string compare, and one print.
    """

    def decorate(fn: Callable[P, R]) -> Callable[P, R | None]:
        """Attach the confirmation wrapper.

        Cost
        ----
        ``functools.wraps`` and the closure are built once. That is O(1)
        time and O(1) extra memory. ``fn`` is not called here.
        """

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            """Ask once, then either return or call ``fn``.

            Cost
            ----
            Reading the answer and comparing it with ``y`` is O(1) plus the
            time spent in ``input``. A denial returns immediately. An
            acceptance calls ``fn`` once, so total time is O(1) plus the
            wrapped call. No extra structure is stored.
            """
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
    """Print and return the positional arguments. Used by the module CLI.

    Cost
    ----
    Let k be the number of arguments. Printing the tuple is O(k). The
    confirmation wrapper around this function adds O(1) plus the prompt.
    """

    print(arguments)
    return arguments


def main(argv: list[str] | None = None) -> tuple[str, ...] | None:
    """Prompt, then print the CLI arguments when the answer is yes.

    Cost
    ----
    Copying the argument vector is O(k) for k arguments. The prompt and the
    print are the rest of the work, so time is O(k) plus waiting on input.
    """

    args = list(sys.argv[1:] if argv is None else argv)
    return show_arguments(*args)


if __name__ == "__main__":
    main()
