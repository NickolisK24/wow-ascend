"""Blizzard Battle.net API feasibility probe (Gate 1).

STATUS AT BASELINE (2026-11-02): NOT RUN. No Battle.net client credentials were
available and the research sandbox's network policy blocked *.battle.net and
*.blizzard.com. Every endpoint path below comes from documentation research
(docs/research/BLIZZARD_API_CAPABILITIES.md) and MUST be confirmed by running
this script; a 404 on a documented path is itself a finding.

Usage:
  export BNET_CLIENT_ID=... BNET_CLIENT_SECRET=...
  export BNET_REGION=us            # us | eu | kr | tw
  export PROBE_REALM_SLUG=...      # e.g. a realm slug of a character you control
  export PROBE_CHARACTER=...       # lowercase character name
  python3 research/proofs-of-concept/blizzard_api_probe.py

  # Optional authorization-code (user) flow, to test wow.profile:
  export BNET_REDIRECT_URI=http://localhost:8765/callback   # must be registered
  python3 research/proofs-of-concept/blizzard_api_probe.py --user-flow
"""

from __future__ import annotations

import secrets
import sys
import urllib.parse

from _common import basic_auth, http, report, require_env, save

OAUTH_HOST = "https://oauth.battle.net"  # verify: unified host (CN differs)


def client_token(env: dict[str, str]) -> str:
    status, _, body = http(
        "POST", f"{OAUTH_HOST}/token",
        headers={"Authorization": basic_auth(env["BNET_CLIENT_ID"], env["BNET_CLIENT_SECRET"]),
                 "Content-Type": "application/x-www-form-urlencoded"},
        data=b"grant_type=client_credentials",
    )
    ok = status == 200 and isinstance(body, dict) and "access_token" in body
    report("client-credentials token", ok, f"HTTP {status}; expires_in={body.get('expires_in') if isinstance(body, dict) else '?'}")
    if not ok:
        sys.exit(1)
    # Record token *shape* only (never the token).
    save("bnet_token_shape", {k: type(v).__name__ for k, v in body.items()})
    return body["access_token"]


def api(region: str, path: str, namespace: str, token: str, *, ns_in_query: bool = False) -> tuple[int, dict, object]:
    """Token always in the Authorization header (query-string tokens rejected since 2024-09-30).

    Namespace goes in the `Battlenet-Namespace` header (documented by current SDKs);
    `ns_in_query=True` tests whether the legacy `?namespace=` form still works.
    """
    sep = "&" if "?" in path else "?"
    headers = {"Authorization": f"Bearer {token}"}
    if ns_in_query:
        url = f"https://{region}.api.blizzard.com{path}{sep}namespace={namespace}-{region}&locale=en_US"
    else:
        url = f"https://{region}.api.blizzard.com{path}{sep}locale=en_US"
        headers["Battlenet-Namespace"] = f"{namespace}-{region}"
    return http("GET", url, headers=headers)


def probe_public(env: dict[str, str], token: str) -> None:
    region = env["BNET_REGION"]
    realm, char = env["PROBE_REALM_SLUG"], env["PROBE_CHARACTER"].lower()
    base = f"/profile/wow/character/{realm}/{urllib.parse.quote(char)}"

    checks = [
        ("game data: keystone dungeon index", "/data/wow/mythic-keystone/dungeon/index", "dynamic"),
        ("game data: keystone season index", "/data/wow/mythic-keystone/season/index", "dynamic"),
        ("game data: keystone period index", "/data/wow/mythic-keystone/period/index", "dynamic"),
        ("game data: keystone affix index", "/data/wow/keystone-affix/index", "static"),
        ("game data: playable spec 259 (Assassination)", "/data/wow/playable-specialization/259", "static"),
        ("profile: character summary", base, "profile"),
        ("profile: equipment", f"{base}/equipment", "profile"),
        ("profile: specializations", f"{base}/specializations", "profile"),
        ("profile: mythic keystone profile", f"{base}/mythic-keystone-profile", "profile"),
        ("profile: statistics", f"{base}/statistics", "profile"),
    ]
    season_id = None
    for label, path, ns in checks:
        status, hdrs, body = api(region, path, ns, token)
        report(label, status == 200, f"HTTP {status}")
        if status == 200:
            save(label.split(": ")[1].replace(" ", "_"), body)
            if path.endswith("mythic-keystone-profile") and isinstance(body, dict):
                seasons = body.get("seasons") or []
                if seasons:
                    season_id = seasons[-1].get("id")
                report("  keystone profile has current_mythic_rating", "current_mythic_rating" in body)
            if path.endswith("/equipment") and isinstance(body, dict):
                items = body.get("equipped_items") or []
                report("  equipment returns items", bool(items), f"{len(items)} items")
                report("  some item has enchantments", any("enchantments" in i for i in items))
                report("  some item has sockets", any("sockets" in i for i in items))
                report("  items carry item level", all("level" in i for i in items) if items else None)
            if path.endswith("/specializations") and isinstance(body, dict):
                txt = str(body)
                report("  talent loadouts present", "loadouts" in txt)
                report("  hero talent data present (field name UNVERIFIED)", "hero" in txt.lower())
        # Record rate-limit related headers if any are exposed.
        rl = {k: v for k, v in hdrs.items() if "limit" in k.lower() or "retry" in k.lower()}
        if rl:
            print(f"    rate-limit headers: {rl}")

    if season_id:
        status, _, body = api(region, f"{base}/mythic-keystone-profile/season/{season_id}", "profile", token)
        report(f"profile: keystone season {season_id} details", status == 200, f"HTTP {status}")
        if status == 200:
            save("keystone_season_details", body)
            runs = body.get("best_runs", []) if isinstance(body, dict) else []
            report("  season details list best runs only (not full history)", None, f"{len(runs)} runs returned")

    status, _, _ = api(region, "/data/wow/mythic-keystone/dungeon/index", "dynamic", token, ns_in_query=True)
    report("legacy ?namespace= query form still accepted", status == 200, f"HTTP {status}")
    status, hdrs, _ = api(region, f"{base}/status", "profile", token)
    report("profile: character status (30-day validity check)", status == 200, f"HTTP {status}")

    # Negative tests: missing-data and unauthorized handling.
    status, _, body = api(region, f"/profile/wow/character/{realm}/zzzznotarealchar", "profile", token)
    report("nonexistent character -> 404 (handled, not crash)", status == 404, f"HTTP {status}")
    status, _, _ = api(region, base, "profile", "invalid-token")
    report("invalid token -> 401 (handled)", status == 401, f"HTTP {status}")


def user_flow(env: dict[str, str]) -> None:
    redirect = require_env("BNET_REDIRECT_URI")["BNET_REDIRECT_URI"]
    state = secrets.token_urlsafe(16)
    # PKCE support is UNKNOWN (see BLIZZARD_API_CAPABILITIES.md §2). We send a
    # code_challenge alongside the confidential-client flow; if the exchange with
    # code_verifier succeeds, PKCE is at least tolerated. Re-test without the
    # secret to learn whether public-client PKCE is supported.
    import base64, hashlib
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    q = urllib.parse.urlencode({
        "client_id": env["BNET_CLIENT_ID"], "response_type": "code", "redirect_uri": redirect,
        "scope": "openid wow.profile", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256",
    })
    print(f"Open in a browser and authorize:\n  {OAUTH_HOST}/authorize?{q}\n")
    code = input("Paste the `code` query parameter from the redirect: ").strip()
    returned_state = input("Paste the `state` query parameter: ").strip()
    report("state round-trips (CSRF protection)", returned_state == state)
    status, _, body = http(
        "POST", f"{OAUTH_HOST}/token",
        headers={"Authorization": basic_auth(env["BNET_CLIENT_ID"], env["BNET_CLIENT_SECRET"]),
                 "Content-Type": "application/x-www-form-urlencoded"},
        data=urllib.parse.urlencode({"grant_type": "authorization_code", "code": code,
                                     "redirect_uri": redirect, "code_verifier": verifier}).encode(),
    )
    report("authorization-code exchange", status == 200, f"HTTP {status}")
    if status != 200:
        return
    save("bnet_user_token_shape", {k: type(v).__name__ for k, v in body.items()})
    report("refresh_token issued", "refresh_token" in body, "absence is expected per research; confirm")
    utoken = body["access_token"]
    status, _, ui = http("GET", f"{OAUTH_HOST}/userinfo", headers={"Authorization": f"Bearer {utoken}"})
    report("userinfo", status == 200, f"HTTP {status}; keys={sorted(ui) if isinstance(ui, dict) else '?'}")
    status, _, prof = api(env["BNET_REGION"], "/profile/user/wow", "profile", utoken)
    report("account profile summary (character discovery)", status == 200, f"HTTP {status}")
    if status == 200:
        save("account_profile_summary", prof)


def main() -> None:
    env = require_env("BNET_CLIENT_ID", "BNET_CLIENT_SECRET", "BNET_REGION")
    if "--user-flow" in sys.argv:
        user_flow(env)
        return
    env.update(require_env("PROBE_REALM_SLUG", "PROBE_CHARACTER"))
    probe_public(env, client_token(env))


if __name__ == "__main__":
    main()
