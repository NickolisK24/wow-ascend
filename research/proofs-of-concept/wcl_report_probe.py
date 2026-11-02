"""Warcraft Logs v2 API feasibility probe (Gates 1 and 2).

STATUS AT BASELINE (2026-11-02): NOT RUN. No Warcraft Logs API client was
available and the sandbox network policy blocked www.warcraftlogs.com.

Design: the probe first runs GraphQL *introspection* and only queries fields
the live schema actually declares. Field names in QUERIES below are taken
from research and are re-checked against introspection before use, so the
probe reports UNSUPPORTED instead of silently trusting documentation.

Usage:
  export WCL_CLIENT_ID=... WCL_CLIENT_SECRET=...
  export WCL_REPORT_CODE=...        # a PUBLIC Midnight Mythic+ report you may use
  export WCL_PLAYER_NAME=...        # an Assassination Rogue in that report
  python3 research/proofs-of-concept/wcl_report_probe.py

Private reports require the user (authorization-code) API, which this probe
does not implement; see docs/research/WARCRAFT_LOGS_FEASIBILITY.md.
"""

from __future__ import annotations

import json
import sys
from collections import Counter

from _common import basic_auth, http, report, require_env, save

TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"
CLIENT_API = "https://www.warcraftlogs.com/api/v2/client"

# Event dataTypes we hope to verify. Each is tested independently.
DATA_TYPES = ["DamageDone", "DamageTaken", "Casts", "Buffs", "Debuffs",
              "Interrupts", "Deaths", "Resources", "CombatantInfo", "Healing"]


def token(env: dict[str, str]) -> str:
    status, _, body = http("POST", TOKEN_URL,
                           headers={"Authorization": basic_auth(env["WCL_CLIENT_ID"], env["WCL_CLIENT_SECRET"]),
                                    "Content-Type": "application/x-www-form-urlencoded"},
                           data=b"grant_type=client_credentials")
    ok = status == 200 and isinstance(body, dict) and "access_token" in body
    report("WCL client-credentials token", ok, f"HTTP {status}")
    if not ok:
        sys.exit(1)
    return body["access_token"]


def gql(tok: str, query: str, variables: dict | None = None) -> dict:
    status, _, body = http("POST", CLIENT_API,
                           headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                           data=json.dumps({"query": query, "variables": variables or {}}).encode())
    if status != 200 or not isinstance(body, dict):
        return {"errors": [{"message": f"HTTP {status}"}], "_body": body}
    return body


def type_fields(tok: str, type_name: str) -> set[str]:
    q = "query($n:String!){ __type(name:$n){ fields { name } } }"
    t = (gql(tok, q, {"n": type_name}).get("data") or {}).get("__type") or {}
    return {f["name"] for f in (t.get("fields") or [])}


def main() -> None:
    env = require_env("WCL_CLIENT_ID", "WCL_CLIENT_SECRET", "WCL_REPORT_CODE", "WCL_PLAYER_NAME")
    tok = token(env)

    rl = gql(tok, "{ rateLimitData { limitPerHour pointsSpentThisHour pointsResetIn } }")
    report("rateLimitData query", "data" in rl and not rl.get("errors"), json.dumps(rl.get("data")))

    fight_fields = type_fields(tok, "ReportFight")
    save("schema_ReportFight_fields", sorted(fight_fields))
    wanted = ["id", "name", "startTime", "endTime", "encounterID", "kill", "keystoneLevel",
              "keystoneAffixes", "keystoneTime", "keystoneBonus", "dungeonPulls", "friendlyPlayers"]
    for f in wanted:
        report(f"schema: ReportFight.{f}", f in fight_fields)
    present = [f for f in wanted if f in fight_fields and f != "dungeonPulls"]
    pulls = "dungeonPulls { id encounterID startTime endTime kill }" if "dungeonPulls" in fight_fields else ""

    q = f"""query($code:String!){{ reportData {{ report(code:$code) {{
        startTime endTime zone {{ id name }}
        fights {{ {' '.join(present)} {pulls} }}
        masterData {{ actors(type:"Player") {{ id name type subType server }} }}
    }} }} }}"""
    meta = gql(tok, q, {"code": env["WCL_REPORT_CODE"]})
    rep = ((meta.get("data") or {}).get("reportData") or {}).get("report")
    report("report metadata retrieved", bool(rep), json.dumps(meta.get("errors")) if meta.get("errors") else "")
    if not rep:
        sys.exit(1)
    save("report_metadata", rep)

    keys = [f for f in rep["fights"] if f.get("keystoneLevel")]
    report("report contains Mythic+ fight(s)", bool(keys), f"{len(keys)} keystone fights")
    if not keys:
        sys.exit(1)
    fight = keys[0]
    player = next((a for a in rep["masterData"]["actors"]
                   if a["name"].lower() == env["WCL_PLAYER_NAME"].lower()), None)
    report("player identified in masterData", bool(player),
           f"subType={player.get('subType') if player else None}")
    if not player:
        sys.exit(1)

    for dt in DATA_TYPES:
        counts: Counter[str] = Counter()
        pages, start, events_total = 0, fight["startTime"], 0
        sample: list = []
        while start is not None and pages < 50:
            ev = gql(tok, """query($c:String!,$f:[Int]!,$s:Float!,$e:Float!,$d:EventDataType!,$p:Int){
                reportData{ report(code:$c){ events(fightIDs:$f,startTime:$s,endTime:$e,dataType:$d,sourceID:$p,limit:10000){
                    data nextPageTimestamp } } } }""",
                {"c": env["WCL_REPORT_CODE"], "f": [fight["id"]], "s": start, "e": fight["endTime"],
                 "d": dt, "p": player["id"]})
            if ev.get("errors"):
                report(f"events dataType={dt}", False, json.dumps(ev["errors"])[:200])
                break
            page = ev["data"]["reportData"]["report"]["events"]
            data = page.get("data") or []
            events_total += len(data)
            counts.update(e.get("type", "?") for e in data)
            sample.extend(data[:25] if len(sample) < 25 else [])
            start, pages = page.get("nextPageTimestamp"), pages + 1
        else:
            report(f"events dataType={dt}", events_total > 0,
                   f"{events_total} events over {pages} page(s); types={dict(counts)}")
            if sample:
                save(f"events_{dt}_sample", sample[:25])
                ts = [e.get("timestamp") for e in sample if "timestamp" in e]
                report(f"  {dt} timestamps monotonic in sample", ts == sorted(ts))


if __name__ == "__main__":
    main()
