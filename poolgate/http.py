"""Put a real matcher through the gate over HTTP.

    POST {url}/rank
    {"vacancy": {...}, "profiles": [{...}, ...]}
    -> {"ranking": [{"id": str, "score": float,
                     "shortlist": bool | null,          (optional)
                     "note": str,                       (optional)
                     "musts": {"beruf": "erfüllt", ...}  (optional)}, ...]}

`vacancy` and each profile are exactly the dicts the built-in matchers get
(see `Vacancy.public` and `Profile.public`). Order the ranking best first;
profiles left out rank last. Optional fields make the report richer: with
`shortlist` the matcher's own yes-list is graded, with `musts` the gate shows
which must-have was misread for every missed fit.
"""

from __future__ import annotations

import json
import urllib.request

from .types import Ranked


class HttpMatcher:
    def __init__(self, url: str, timeout: float = 600.0, name: str | None = None):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.name = name or f"http {self.url}"

    def rank(self, vacancy: dict, profiles: list[dict]) -> list[Ranked]:
        body = json.dumps({"vacancy": vacancy, "profiles": profiles}, ensure_ascii=False)
        req = urllib.request.Request(f"{self.url}/rank", data=body.encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            data = json.loads(r.read())
        known = {p["id"] for p in profiles}
        out, seen = [], set()
        for item in data["ranking"]:
            pid = item["id"]
            if pid not in known or pid in seen:
                continue  # unknown or duplicate ids are ignored, not trusted
            seen.add(pid)
            out.append(Ranked(pid, float(item.get("score", 0.0)), item.get("shortlist"),
                              item.get("note", ""), item.get("musts") or {}, "http"))
        return out
