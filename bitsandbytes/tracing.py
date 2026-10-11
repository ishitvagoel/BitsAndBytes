"""Optional step events for lessons. A missing sink adds no work."""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TraceEvent:
    kind: str
    values: dict[str, object]


TraceSink = Callable[[TraceEvent], None]
