"""A deterministic stand-in matcher with fault knobs.

It reads the hidden facts (which no real matcher sees) and applies the
vacancy's rules, so with every knob off it ranks perfectly. Each knob plants
one failure a real matcher can have, so the gate can be shown to catch it
before it is pointed at a real system. Its numbers say nothing about any real
matcher.

  miss_synonym  probability a fit shown only by a synonym or old name is missed
  miss_buried   probability a fit whose must-have fact is only in the notes is missed
  near_miss     probability a near-miss (fails one must-have) is taken for a fit
  bias          {origin: steps}: lower the score of names of that origin
  noise         score jitter that changes from call to call (a repeat baseline > 0)
"""

from __future__ import annotations

import hashlib
import random
import threading

from .pool import VACANCY_BY_KEY, Profile, case_family, case_type, check, near_miss, origin_of
from .types import Ranked


def _draw(*parts: object) -> float:
    h = hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()
    return int(h[:12], 16) / 16**12


class OfflineMatcher:
    def __init__(self, truth: dict[str, Profile], miss_synonym: float = 0.0,
                 miss_buried: float = 0.0, near_miss: float = 0.0,
                 bias: dict[str, int] | None = None, noise: float = 0.0, name: str = "offline"):
        self.truth = truth
        self.miss_synonym = miss_synonym
        self.miss_buried = miss_buried
        self.near_miss = near_miss
        self.bias = bias or {}
        self.noise = noise
        self.name = name
        self._calls = 0
        self._lock = threading.Lock()

    def _judge(self, v, p: Profile) -> tuple[bool, list[str]]:
        checks = check(v, p.facts)
        failed = [m for m, ok in checks.items() if not ok]
        if not failed:
            fam = case_family(case_type(v, p))
            if fam == "synonym" and _draw("syn", v.key, p.id) < self.miss_synonym:
                return False, ["beruf"]
            if fam == "buried" and _draw("bur", v.key, p.id) < self.miss_buried:
                return False, [case_type(v, p).split(":")[1]]
            return True, []
        if near_miss(v, p.facts) and _draw("near", v.key, p.id) < self.near_miss:
            return True, []
        return False, failed

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        v = VACANCY_BY_KEY[vacancy["key"]]
        with self._lock:
            self._calls += 1
            jitter = random.Random(f"noise-{self._calls}")
        out = []
        for pub in profiles:
            p = self.truth[pub["id"]]
            fit, failed = self._judge(v, p)
            # Tie-break on the id, never on the name: a swap must not move it.
            score = (80.0 if fit else 40.0 - 8 * len(failed)) + 10 * _draw("tie", v.key, p.id)
            score -= 40.0 * self.bias.get(origin_of(pub["name"]) or "", 0)
            if self.noise:
                score += jitter.uniform(-self.noise, self.noise)
            musts = {m: ("nicht erfüllt" if m in failed else "erfüllt") for m in v.musts()}
            out.append(Ranked(pub["id"], score, shortlist=score >= 60, musts=musts,
                              note="" if fit else "nicht erfüllt: " + ", ".join(failed),
                              stage="offline"))
        out.sort(key=lambda r: (-r.score, r.id))
        return out
