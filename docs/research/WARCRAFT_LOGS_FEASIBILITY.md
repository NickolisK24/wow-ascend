# Warcraft Logs — Post-Run Analysis Feasibility

**Research date:** 2026-11-02 · **Status:** Baseline v1 · **Live sample validation: BLOCKED** (§6)

> **Evidence basis.** `warcraftlogs.com` and `archon.gg` were blocked by the sandbox network policy (proxy 403). Two kinds of evidence were used:
> 1. **Primary, read directly:** a full dump of the WCL v2 GraphQL schema (`schema/schema.graphql`, 4,270 lines) shipped in the open-source `math280h/go-wcl` client, commit `5b07433`, **2026-07-19** (`WCL-01`); and the WoWAnalyzer source tree, commit `27b1efb`, **2026-11-02** (`WCL-02`). Schema fields listed as "verified" were read in that dump; fields added after July 2026 would be missing.
> 2. **Secondary:** search-result summaries of WCL/Archon docs and announcements, and third-party GitHub issues.
>
> **What this does NOT establish:** that a real Midnight Mythic+ report returns the expected events for an Assassination Rogue. That is Gate 1's central test and has not been run.

## 1. Summary verdict
| Question | Answer | Confidence |
|---|---|---|
| Does the WCL API expose the event categories needed for per-player analysis? | **Yes, by schema** | High (schema) |
| Do Midnight logs still contain those events? | **Very likely** — the game director is quoted (secondhand) saying file logging is unchanged; WoWAnalyzer supports patches to 12.1.0; a 2026-11-01 project documents casts/resources/talents in current logs | Medium-High |
| Can a third party legally store and process them commercially? | **Unresolved** — commercial use requires prior approval; caching limited by cache headers (`no-cache, private` observed) | Medium-Low (terms not read) |
| Can a solo app afford the rate limits? | **Probably at beta scale**, uncertain beyond; new points system in beta since 2026-10-20 | Medium |
| Has the live sample test been done? | **No — BLOCKED** | – |

## 2. API surface (verified unless noted)

| Item | Value | Conf | Src |
|---|---|---|---|
| Public endpoint | `https://www.warcraftlogs.com/api/v2/client` | High | `WCL-01` (client code) |
| User endpoint | `https://www.warcraftlogs.com/api/v2/user` | High | `WCL-01` |
| Authorize / token | `/oauth/authorize`, `/oauth/token` | High | `WCL-01`,`WCL-03` |
| Grants | client credentials; authorization code; **PKCE (S256)** | High | `WCL-01`,`WCL-03` |
| Client-credentials access | "only public information… no private reports" | High | `WCL-03` |
| Private reports | Only via user API with the user's permission | Med-High | `WCL-03` |
| Unlisted reports | `report(code, allowUnlisted: Boolean)`; schema warns multi-user apps caching codes to set it carefully. Default UNVERIFIED | High (field) | `WCL-01` |
| Visibility | `Report.visibility` ∈ public / private / unlisted | High | `WCL-01` |
| Archive | `Report.archiveStatus{isArchived,isAccessible,archiveDate}`; "Events, tables, and graphs for archived reports are inaccessible unless the retrieving user has a subscription including archive access"; `isAccessible` false without user auth | High | `WCL-01` |
| CORS for browser PKCE | UNVERIFIED → Ascend calls WCL **server-side only** | – | `WCL-04` |
| Scope for private reports | UNKNOWN (`view-user-profile` scope exists for claimed characters) | – | `WCL-01` |

### 2.1 Report and fight model
- **One Mythic+ key = one `ReportFight`** with `keystoneLevel`, `keystoneAffixes: [Int]`, `keystoneBonus` (1–3 upgrades), `keystoneTime` ("official time used on Blizzard leaderboards"), `rating`, `kill`, `startTime`/`endTime` (ms relative to report start), `friendlyPlayers`, `friendlySpecs`, `friendlyItemLevels`, `enemyNPCs`, `talentImportCode(actorID)` (High, `WCL-01`; field list re-read 2026-11-02).
- **`dungeonPulls: [ReportDungeonPull]`** — each pull has `id, name, encounterID (0 = trash), startTime, endTime, kill, enemyNPCs, maps, boundingBox, x, y` (High). **Boss encounters inside a key are separable** by pull time range.
- Whether a pull `id` works as a `fightIDs` argument: UNVERIFIED → use the pull's time range.
- Enemy-forces fields (`countReached`, `countRequired`) seen only in WoWAnalyzer's v1 type: UNVERIFIED in v2.
- **Actors:** `masterData.actors{id, gameID, name, server, type, subType, petOwner, icon}`; `id` is report-local. **No GUID field.** Cross-report identity = `(region, server, name)`; WCL `Character.canonicalID` survives renames.

### 2.2 Events
- `report.events(startTime, endTime, fightIDs, encounterID, dataType, sourceID, targetID, hostilityType, abilityID, filterExpression, includeResources, limit 100–10000 default 300, translate, useAbilityIDs, useActorIDs, …)` → `ReportEventPaginator{ data: JSON, nextPageTimestamp: Float }` (High, `WCL-01`).
- `EventDataType`: All, Buffs, Casts, CombatantInfo, DamageDone, DamageTaken, Deaths, Debuffs, Dispels, Healing, Interrupts, Resources, Summons, Threat (High, re-read 2026-11-02).
- **Event JSON shape is not defined by the schema** and is documented as "not considered frozen… can change without notice." ⇒ Ascend must validate every event against its own versioned contract and fail closed (see [ANALYSIS_ENGINE.md](../architecture/ANALYSIS_ENGINE.md) §3).
- Event `type` strings observed in WoWAnalyzer's parser (mirrors WCL output): `damage, heal, absorbed, begincast, cast, applybuff, applydebuff, applybuffstack, applydebuffstack, refreshbuff, refreshdebuff, removebuff, removedebuff, removebuffstack, removedebuffstack, aurabroken, summon, death, resurrect, resourcechange, interrupt, combatantinfo, …` (High that these exist). There is **no separate "energize" type** — energy gains are `resourcechange`.
- With `includeResources`, events carry `classResources{amount, max, type, cost}`; `resourcechange` carries `resourceChange, waste, maxResourceAmount`; `combatantinfo` carries `talentTree[{id, rank, nodeID}]` — documented in current logs by a 2026-11-01 project (Med-High, `WCL-04`).
- Also available: `table()`, `graph()` (incl. Survivability), `playerDetails`, `rankings`, and **Report Components** (`evaluateScript`, server-side scripting; limits UNKNOWN).

### 2.3 Rate limits
- `rateLimitData{limitPerHour, pointsSpentThisHour, pointsResetIn}` (High, schema). HTTP 429 when exceeded.
- Observed: ~1,000 points/hour; "one full fight costs about 2–6 points" (Med, `WCL-04`, 2026-11-01).
- **New system in beta since 2026-10-20** (Med, `WCL-05` citing `WCL-06`): App points (all requests), DB points (rankings & report search; deeper pages cost more), User points (requests on behalf of a signed-in user). Hourly App/DB by key owner's subscription: Unsubscribed 1000/250; Silver 1000/350; Gold 3000/1050; Platinum 9000/3200. "Report events don't cost DB points." **"For-profit apps will need a new commercial access tier (no price yet)."**
- **Budget estimate (assumption):** one import ≈ metadata (1 query) + ~6 event dataTypes × ~1–5 pages ≈ 10–30 queries. If per-fight cost is a few points, 1,000 points/hour supports roughly **dozens of imports/hour** — adequate for beta, to be **measured** in T-WCL-05. Cohort calibration (pulling many ranked reports) is the expensive workload; it runs offline and infrequently.

## 3. Midnight combat-data restrictions — the five surfaces

| # | Surface | State as of 2026-11-02 | Conf | Src |
|---|---|---|---|---|
| 1 | In-game addon information | `COMBAT_LOG_EVENT_UNFILTERED` forbidden to addons since 12.0.0; secret values; easing reportedly limits restrictions to boss encounters and M+ | High | `WOW-19`,`WOW-20` |
| 2 | Combat log written by client | Ion Hazzikostas (quoted secondhand): "/combatlog functionality, advanced combat log, exporting for parsing by other tools, all of that is going to remain completely unchanged. The only changes are about the in-game add-on API." Healing under-reporting for some healers reported (disputed). | **Med-High** (secondhand quote) | `WCL-10`,`WCL-11`,`WCL-14` |
| 3 | Accepted by WCL | WCL continues to ingest Midnight logs via the **Archon App** (old uploader retired 2026-06-29); WoWAnalyzer supports 12.0.0–12.1.0 | Med-High | `WCL-13`,`WCL-02` |
| 4 | Exposed by WCL API | Schema unchanged in shape; event JSON unfrozen; field-level loss in 12.0 **not evidenced either way** | Med | `WCL-01`,`WCL-04` |
| 5 | Legally processable by Ascend | **Unresolved** (§5) | – | `WCL-07..09` |

Conflicting claim: one Medium article says external logs are "partially blocked" (Low, uncorroborated, `WCL-16`).

**Prohibited approaches (unchanged by any finding):** no addon-based bypasses, memory inspection, protected-API workarounds, in-combat decision support, or automated gameplay. Ascend operates only on completed, uploaded logs.

## 4. Metric feasibility table

Legend — Evidence quality: **S** = schema-verified data path; **P** = WoWAnalyzer implements an equivalent for Assassination (proves computability historically; its Assassination module is `SupportLevel.MaintainedPartial`, `patchCompatibility: '12.0.0'`, last changelog entry "Spells adjusted and partial support for 12.0.0" — **not updated for 12.1's Deathmark rework**; `WCL-02`); **U** = unverified for Midnight data. *No row is live-verified.*

| Desired metric | Required source events | Available fields (documented) | Calculation | Validity assumptions | Missing-data behavior | Evidence | Difficulty | MVP? |
|---|---|---|---|---|---|---|---|---|
| Cooldown usage count (Deathmark, Kingsbane) on bosses | `cast` by player; boss pull boundaries | `Casts` events: timestamp, sourceID, abilityGameID; `dungeonPulls` | uses vs opportunities (see AR-01) | CD length verified; no CDR effects unknown to us | Skip rule if pull boundaries or casts absent | S + P (WoWAnalyzer `Deathmark`, `Kingsbane` modules) + U | Low | **Yes (candidate)** |
| Ability usage frequency | `cast` | as above | casts / minute active | Death/dead time excluded | Fact only | S + U | Low | Yes (supporting fact) |
| Ability sequence analysis | `cast` ordering | timestamps | pattern match (e.g., Vanish→Garrote→Deathmark) | Event ordering reliable (WoWAnalyzer has ordering normalizers ⇒ **ordering quirks exist**) | Skip | S + P (`DeathmarkImprovedGarroteLinkNormalizer`) | Medium | Later |
| Target-specific damage | `damage` with targetID | DamageDone events | sum by target | Target identity via actors | Fact only | S | Low | No (not coaching) |
| **DoT uptime** (Rupture/Garrote) on boss | `applydebuff/refreshdebuff/removedebuff` by player on boss | Debuffs events with targetID | interval union / (boss pull duration − player dead time) | Untargetable windows not modeled (stated) | Skip if unpaired apply/remove > tolerance | S + P (`RuptureUptimeAndSnapshots`, `GarroteUptimeAndSnapshots`) + U | Medium | **Yes (candidate)** |
| Finisher CP / energy waste | `cast` with `classResources`; `resourcechange` `waste` | includeResources; resourcechange | % finishers < threshold CP; energy wasted | Resource fields present in Midnight (documented by `WCL-04`, not by us) | Rule disabled until T-WCL-04 confirms | S + P (`FinisherUse`, `EnergyGraph`) + U | Medium | No (pending) |
| Interrupt contribution | `interrupt` events by player; `cast` of Kick | Interrupts events | counts | Assignments unknown | Fact only | S + U | Low | **Yes (fact)** |
| Avoidable damage | DamageTaken + curated ability list | DamageTaken events | sum listed abilities | Curated list per season | Not offered | S (data) / curated list absent | High (maintenance) | **No** |
| Death timing and cause | `death` events; preceding `damage` taken | Deaths, DamageTaken | killing blow + `window_ms` (rule data, D-018) | Killing blow identifiable | Show "cause unknown" | S + U | Low-Med | **Yes (fact)** |
| Defensive availability at death | player `cast` history of defensives | Casts | last use vs verified CD | CDs verified | Omit availability line | S + U | Medium | **Only after T-VER-01** |
| Downtime | casts + movement/untargetable info | Casts; no reliable untargetable data | – | Requires encounter context | – | U | High | **No** |
| Comparison vs similar players | rankings + other reports | `characterRankings`, `fightRankings` (DB points) | percentile of metric in cohort | Cohort large enough; same patch/tree/key band | Show no comparison | S (fields) + U (costs) | High | **No for live**; used **offline** for calibration only |

## 5. Terms and permissions (not read directly — see [SECURITY_AND_DATA_POLICY.md](../compliance/SECURITY_AND_DATA_POLICY.md))
- **Commercial use** (earning money incl. advertising) requires **prior approval by email** (Med-Low, `WCL-08`).
- **Caching:** reportedly may not keep cached copies longer than permitted by the cache header; observed `Cache-Control: no-cache, private` (Med, `WCL-09`). ⇒ **Decision D-006:** Ascend does **not** persist raw event streams; it processes events in memory and stores only derived metrics plus minimal evidence references (report code, fight/pull ID, timestamps, ability IDs). Whether even derived-metric storage is permitted: **UNVERIFIED → must be confirmed in writing.**
- Public display to third parties restricted unless content owner permits ⇒ findings are private to the importing user by default.
- Clause against building a client "substantially the same as the APIs" (Med-Low).
- Ownership: WCL operated by **Archon** (formerly RPGLogs), which also owns WoWAnalyzer, Wipefest, Subcreation, Warcraft Recorder (High, `WCL-15`). **Ascend would depend on a competitor-adjacent platform.**

## 6. Live sample validation — BLOCKED
**Blockers:** (1) no WCL API client; (2) sandbox network policy blocks `www.warcraftlogs.com`; (3) no confirmed permitted Midnight M+ report with an Assassination Rogue.

**Exact steps to unblock** (owner: project lead; ~2 h):
1. Create a WCL account; register an API client at the WCL client management page (location per `WCL-03`); store ID/secret in a local `.env` (git-ignored).
2. Obtain a report: preferably the project lead's own (or a consenting friend's) Midnight Season 2 key log uploaded via Archon App as **public or unlisted**; alternatively a public report from WCL M+ rankings for an Assassination Rogue (public reports are accessible to client-credentials by design; confirm Terms allow analysis — §5).
3. Run `python3 research/proofs-of-concept/wcl_report_probe.py` from an unrestricted network.
4. Commit only `research/fixtures/sanitized/*` after manual review; raw responses stay in the git-ignored `research/fixtures/raw/`.
5. Record results in [FEASIBILITY_TEST_PLAN.md](../quality/FEASIBILITY_TEST_PLAN.md) and update Gate 1 in [BASELINE.md](../BASELINE.md).

**What the probe checks:** schema introspection of `ReportFight` (incl. `dungeonPulls`); report metadata; M+ fight detection; player identification; each `EventDataType` independently with pagination and timestamp monotonicity; `rateLimitData` cost per call. It never trusts a field it did not first see in live introspection.

### 6.1 Sample report study checklist (to execute)
Retrieve metadata → identify key and boss pulls → identify player/spec/hero tree (from `combatantinfo`) → inspect event categories → verify timestamps within pull bounds → test pagination → check for unpaired debuff events and missing deaths → record limits → sanitize fixtures → run T-CALC-01 (rule list in the test plan) and compare to WCL's own tables for the same report (independent cross-check).

## 7. Conclusion for Gate 1
Documentary evidence is **strongly favorable** for the data path and **unfavorable-to-unclear** for permissions and scale economics. Gate 1 cannot PASS without the live sample; status **BLOCKED**.
