"""Decorators: ask before running, and check a permission before running."""

from bitsandbytes.decorators.access_control import ACTIONS, PERMISSIONS, run_action
from bitsandbytes.decorators.permission import require_confirmation

__all__ = [
    "ACTIONS",
    "PERMISSIONS",
    "require_confirmation",
    "run_action",
]
