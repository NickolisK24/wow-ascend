"""Shared helpers for WoW Ascend feasibility proofs-of-concept.

Standard library only (no dependency installs). These scripts are research
tools, NOT production code. They exist to answer Gate 1 (data feasibility)
questions with real responses.

Security rules (see CLAUDE.md):
- Credentials come only from environment variables; never hard-code them.
- Raw responses are written to research/fixtures/raw/ which is git-ignored.
- Only sanitized output (research/fixtures/sanitized/) may be committed.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "research" / "fixtures" / "raw"
SANITIZED_DIR = ROOT / "research" / "fixtures" / "sanitized"

# Keys whose values identify a real person/account/character. Values are
# replaced with a stable salted hash so structure is preserved for tests.
IDENTIFYING_KEYS = {
    "name", "battletag", "id_token", "access_token", "sub", "realm_name",
    "guild", "character_name", "server", "owner", "title", "guid",
    "displayName", "icon", "href", "url", "code",
}


def require_env(*names: str) -> dict[str, str]:
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        print(f"BLOCKED: missing environment variables: {', '.join(missing)}")
        print("See docs/quality/FEASIBILITY_TEST_PLAN.md for how to obtain them.")
        sys.exit(2)
    return {n: os.environ[n] for n in names}


def http(method: str, url: str, *, headers: dict[str, str] | None = None,
         data: bytes | None = None, timeout: int = 30) -> tuple[int, dict[str, str], Any]:
    req = urllib.request.Request(url, method=method, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            status, hdrs = resp.status, dict(resp.headers)
    except urllib.error.HTTPError as exc:  # non-2xx is data, not a crash
        body, status, hdrs = exc.read(), exc.code, dict(exc.headers or {})
    try:
        parsed: Any = json.loads(body) if body else None
    except json.JSONDecodeError:
        parsed = {"_non_json_body": body[:500].decode("utf-8", "replace")}
    return status, hdrs, parsed


def basic_auth(client_id: str, client_secret: str) -> str:
    return "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def _hash(value: str, salt: str) -> str:
    return "anon_" + hashlib.sha256((salt + value).encode()).hexdigest()[:12]


def sanitize(obj: Any, salt: str | None = None) -> Any:
    salt = salt or os.environ.get("ASCEND_FIXTURE_SALT", "local-salt-change-me")
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in IDENTIFYING_KEYS and isinstance(v, (str, int)):
                out[k] = _hash(str(v), salt)
            else:
                out[k] = sanitize(v, salt)
        return out
    if isinstance(obj, list):
        return [sanitize(v, salt) for v in obj]
    return obj


def save(name: str, payload: Any) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SANITIZED_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{name}.json").write_text(json.dumps(payload, indent=2))
    (SANITIZED_DIR / f"{name}.json").write_text(json.dumps(sanitize(payload), indent=2))
    print(f"  saved fixture: {name} (raw=git-ignored, sanitized=reviewable)")


def report(check: str, ok: bool | None, detail: str = "") -> None:
    label = {True: "PASS", False: "FAIL", None: "N/A "}[ok]
    print(f"[{label}] {check}{' — ' + detail if detail else ''}")
