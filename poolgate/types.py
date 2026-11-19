"""What a matcher receives and returns.

A matcher gets a vacancy and the pool as the ATS shows it (public dicts: the
structured fields, which may be empty, and the notes) and returns a ranking,
best first. Any object with a `rank` method fits; a production matcher can
be put behind HTTP (see `HttpMatcher`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Ranked:
    id: str
    score: float
    # The matcher's own yes/no, when it gives one; None = only a ranking.
    shortlist: bool | None = None
    # Why it was placed here, in the matcher's words (for the missed-fit table).
    note: str = ""
    # Per must-have reading, when the matcher reports one:
    # {"beruf": "erfüllt" | "nicht erfüllt" | "unklar", ...}
    musts: dict = field(default_factory=dict)
    # Which stage produced this place, e.g. "rerank" or "prefilter".
    stage: str = ""


class Matcher(Protocol):
    name: str

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        """All or some of the profiles, best first. Omitted profiles rank last."""
