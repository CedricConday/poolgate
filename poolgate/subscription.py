"""Run Claude through the `claude` CLI on a subscription, with no API key.

Same backend as screengate's: one `claude -p` per call, with a fresh session,
no tools, no MCP servers and no settings files, and the matcher's own system
prompt in place of Claude Code's, so nothing but the prompt reaches the model.
Structured output comes from `--json-schema`; the CLI's JSON envelope also
carries token usage and `total_cost_usd` (the list-price equivalent).

A call that fails (rate limit, overload, timeout, a malformed answer) is
retried with exponential backoff, because another run may share the
subscription. Only after the last attempt does the error reach the caller.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass


class CliError(RuntimeError):
    pass


@dataclass
class CallMeta:
    model: str | None
    input_tokens: int
    output_tokens: int
    cost_usd: float
    attempts: int


class CliClient:
    def __init__(self, binary: str = "claude", timeout: float = 900.0, attempts: int = 6,
                 backoff: float = 20.0, log=None, sleep=time.sleep):
        self.binary = shutil.which(binary) or binary
        self.timeout = timeout
        self.attempts = attempts
        self.backoff = backoff
        self.log = log or (lambda msg: print(f"[poolgate] {msg}", file=sys.stderr, flush=True))
        self.sleep = sleep
        # An empty working directory, so no project CLAUDE.md is picked up.
        self.cwd = tempfile.mkdtemp(prefix="poolgate-cli-")

    def _once(self, model: str, system: str, prompt: str, schema: dict,
              effort: str | None) -> dict:
        cmd = [self.binary, "-p", "--model", model, "--system-prompt", system,
               "--tools", "", "--strict-mcp-config", "--setting-sources", "",
               "--no-session-persistence", "--output-format", "json",
               "--json-schema", json.dumps(schema, ensure_ascii=False)]
        if effort:
            cmd += ["--effort", effort]
        try:
            proc = subprocess.run(cmd, check=False, input=prompt, capture_output=True,
                                  text=True, timeout=self.timeout, cwd=self.cwd)
        except subprocess.TimeoutExpired as e:
            raise CliError(f"claude -p timed out after {self.timeout:.0f}s") from e
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            raise CliError(f"claude -p exit {proc.returncode}: "
                           f"{(proc.stderr or proc.stdout)[-500:]}") from e
        if out.get("is_error"):
            raise CliError(f"claude -p failed: {str(out.get('result'))[:500]}")
        if out.get("structured_output") is None:
            raise CliError(f"claude -p returned no structured output "
                           f"(stop_reason={out.get('stop_reason')})")
        return out

    def structured(self, model: str, system: str, prompt: str, schema: dict,
                   effort: str | None = None, check=None) -> tuple[dict, CallMeta]:
        """One structured answer. `check(obj)` may raise ValueError to force a retry."""
        last = None
        for attempt in range(1, self.attempts + 1):
            try:
                out = self._once(model, system, prompt, schema, effort)
                obj = out["structured_output"]
                if check:
                    check(obj)
                u = out.get("usage", {})
                meta = CallMeta(
                    model=next(iter(out.get("modelUsage") or {}), None),
                    input_tokens=(u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                                  + u.get("cache_read_input_tokens", 0)),
                    output_tokens=u.get("output_tokens", 0),
                    cost_usd=out.get("total_cost_usd") or 0.0, attempts=attempt)
                return obj, meta
            except (CliError, ValueError) as e:
                last = e
                if attempt == self.attempts:
                    break
                wait = min(self.backoff * 2 ** (attempt - 1), 600)
                self.log(f"call failed ({e}); retry {attempt}/{self.attempts - 1} in {wait:.0f}s")
                self.sleep(wait)
        raise CliError(f"gave up after {self.attempts} attempts: {last}")
