# Feasibility Test Plan (Stage 0)

**Date:** 2026-11-02 · **Status:** **No test has been run.** Every result field is empty on purpose.

## 1. Prerequisites (owner: project lead)
1. **Network:** run from an unrestricted machine, or allow these hosts in the cloud environment's network settings: `oauth.battle.net`, `*.api.blizzard.com`, `*.battle.net`, `develop.battle.net`, `www.warcraftlogs.com`, `www.archon.gg`, `news.blizzard.com`, `www.blizzard.com`.
2. **Battle.net:** create a developer account at develop.battle.net (2FA required) and a client. Register the redirect URI `http://localhost:8765/callback`.
3. **Warcraft Logs:** create an account and an API client.
4. **Report:** a Midnight Season 2 M+ key containing an Assassination Rogue, used with permission. Ideally your own, uploaded via the Archon App as unlisted or public.
5. `cp .env.example .env` (created in Stage 1; for now, `export` the variables listed in each probe's docstring).

## 2. Tests

| ID | Test | Method | Pass criterion | Result |
|---|---|---|---|---|
| T-BN-01 | Client-credentials token | `blizzard_api_probe.py` | 200, `access_token`, `expires_in` recorded | – |
| T-BN-02 | Character summary, equipment, specializations, keystone profile, season details for a Midnight Assassination Rogue | probe | All 200; ilvl in `level.value`; enchant/socket arrays present where gear has them; hero-talent data present | – |
| T-BN-03 | Game data: keystone dungeon/season/period/affix indexes; spec 259 | probe | 200; current season ID and 8 dungeons match WOW_RETAIL_FOUNDATIONS §3 | – |
| T-BN-04 | Error handling | probe | Nonexistent character → 404; invalid token → 401 | – |
| T-BN-05 | Legacy `?namespace=` form | probe | Record whether it works (either outcome is informative) | – |
| T-BN-06 | Authorization-code flow, userinfo, `/profile/user/wow` | `probe --user-flow` | Exchange succeeds; userinfo keys recorded; character list fields recorded | – |
| T-BN-07 | Refresh token and PKCE | `--user-flow` | Record whether `refresh_token` is issued and whether the `code_verifier` exchange succeeds | – |
| T-BN-08 | Rate-limit headers | probe output | Record any limit or retry headers | – |
| T-WCL-01 | Token and `rateLimitData` | `wcl_report_probe.py` | 200; record limit and points | – |
| T-WCL-02 | Schema introspection of `ReportFight` | probe | `keystoneLevel`, `dungeonPulls`, `friendlyPlayers` present | – |
| T-WCL-03 | Report metadata, key detection, player identification | probe | Key fight found; player actor found with Rogue subType | – |
| T-WCL-04 | Each EventDataType for the player in the key: Casts, Buffs, Debuffs, DamageTaken, Deaths, Interrupts, Resources, CombatantInfo | probe | Non-empty where expected; pagination terminates; timestamps monotonic; **record whether `classResources` and combo-point data exist** | – |
| T-WCL-05 | Points cost per full import | `rateLimitData` before and after | Record points/import; compare with the 20-point assumption in COST_MODEL | – |
| T-WCL-06 | Boss pull boundaries | probe metadata | `dungeonPulls` with `encounterID ≠ 0` matches the dungeon's boss count | – |
| T-WCL-07 | Unlisted report via the client endpoint, with and without `allowUnlisted` | manual query | Record behavior | – |
| T-WCL-08 | Archived report behavior | manual query on an old report | Record the `archiveStatus` fields | – |
| T-CALC-01 | Hand-compute AR-01, AR-03, AR-10 and AR-14 on 3 reports; compare with WCL's own cast and uptime tables | spreadsheet + WCL UI | Uptime within ±1 pp; cast counts equal | – |
| T-CAL-01 | Calibration cohort for AR-01 and AR-03: ≥30 reports per (main boss cell × hero tree) | script (Stage 0 PoC) | Distributions recorded; thresholds meet ANALYSIS_ENGINE §10 | – |
| T-LEGAL-01 | Read the current Blizzard Developer API Terms in full | manual | Memo answering B1–B7 | – |
| T-LEGAL-02 | Read the RPG Logs API ToS; email for approval, asking explicitly about storing derived metrics | manual | Written reply | – |
| T-UX-01 | 15–20 interviews | script in COMPETITIVE_LANDSCAPE §5 | Synthesis against H1–H7 | – |

## 3. Gate mapping
- **Gate 1** requires T-BN-01..04, T-BN-06 and T-WCL-01..06.
- **Gate 2** requires T-CALC-01 and T-CAL-01, with ≥3 rules qualifying. AR-01 and AR-03 as suggestions, plus ≥1 additional defensible insight, which could be AR-10 if it is judged meaningful.
- **Gate 3** requires T-LEGAL-01 and T-LEGAL-02.
- **Gate 4** requires T-UX-01.

## 4. Primary-source re-verification list (R-19)
These claims rest on search summaries. Open the primary page and confirm each:
- Blizzard "Combat Philosophy and Addon Disarmament in Midnight" (`WOW-18`), including its date.
- The Ion Hazzikostas statement on combat log file output (`WCL-10`).
- The 12.1.5 patch notes, Season 2 dungeon pool and affixes (`WOW-02`, `WOW-05`, `WOW-06`).
- The Blizzard OAuth guide: PKCE, refresh, token lifetime (`BNET-04`).
- The WCL API docs and Archon API beta announcement (`WCL-03`, `WCL-06`).
- The Assassination guides on Icy Veins, Maxroll and Method (`ROG-01..03`).
- The competitor pricing pages (`COMP-07`, `COMP-17`, `COMP-20`).

## 5. Fixture handling
Raw responses go only to `research/fixtures/raw/` (git-ignored). The sanitized output (`research/fixtures/sanitized/`) hashes names, BattleTags, report codes and URLs. **Review every sanitized file by hand before committing.** Never commit a private report's content.
