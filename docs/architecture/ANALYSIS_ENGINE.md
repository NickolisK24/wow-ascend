# Analysis Engine Design

**Date:** 2026-11-02 · **Status:** Baseline v1. Accepted design, not yet implemented.

## 1. Principle
```
Source data → Contract validation → Normalization → Verified metrics → Coaching rules → Prioritization → Explanation
```
- No generative model participates in any step that decides *whether* something is true or important.
- An optional LLM may later **rephrase** a finding that has already been decided, from its structured fields only, and must be labeled as rephrased (post-MVP, D-009).
- Every stage is a **pure function** of its inputs plus versioned reference data, so the result is reproducible (NFR-03).

## 2. Components and boundaries

| Component | Package (proposed) | I/O? | Responsibility |
|---|---|---|---|
| Provider adapters | `ascend.providers.wcl`, `ascend.providers.bnet` | Yes | HTTP, auth, pagination, rate limiting, retries. Return raw JSON plus a fetch manifest (what was requested and what came back) |
| Contract validation | `ascend.analysis.contracts` | No | Validate raw events against versioned Pydantic models. Unknown fields are tolerated; missing required fields **fail closed** for the dependent metric only |
| Normalizer | `ascend.analysis.normalize` | No | Convert to the internal model (§3). Resolve actors, players, bosses and pulls. Apply ordering normalizers |
| Game data | `ascend.gamedata` (versioned files in repo) | No | Spell IDs, cooldowns, talents, dungeon/encounter IDs and season config, keyed by `game_data_version` |
| Metrics | `ascend.analysis.metrics` | No | Deterministic calculations. Each metric has `metric_id` and `metric_version` |
| Rules | `ascend.analysis.rules` | No | Rule definitions plus evaluation into findings. Each rule has `rule_id`, `rule_version` and applicability |
| Prioritizer | `ascend.analysis.priority` | No | Deterministic ordering |
| Explainer | `ascend.analysis.explain` | No | Fill in player-facing text templates stored with the rule version |
| Orchestrator | `ascend.jobs.analyze` | Yes | Runs the pipeline for a job and persists derived output only |

The analysis packages (`contracts` through `explain`) import **nothing** from providers, the web layer or the database. This boundary is enforced by an import-linter test.

## 3. Internal (normalized, in-memory) model
Integer milliseconds relative to report start are used throughout.

```text
RunContext      report_code, fight_id, region, game_version (detected), game_data_version,
                dungeon_id, keystone_level, affixes[], timed(bool|None), duration_ms,
                pulls[PullContext], player(PlayerContext), data_coverage{dataType -> Coverage}
PullContext     pull_id, encounter_id (0 = trash), start_ms, end_ms, kill, boss_actor_ids[]
PlayerContext   actor_id, name, server, spec_id, hero_tree (from combatantinfo), talents{node_id: rank},
                item_level, death_intervals[(start_ms, end_ms)]
CastEvent       ts, source, target|None, ability_id
AuraEvent       ts, source, target, ability_id, kind (apply|refresh|remove|stack_*), aura_type (buff|debuff)
DamageEvent     ts, source, target, ability_id, amount, (taken|done)
InterruptEvent  ts, source, target, interrupted_ability_id
DeathEvent      ts, target, killing_ability_id|None
ResourceSample  ts, actor, resource_type, amount, max   (only if Resources verified)
Coverage        requested(bool), returned(bool), pages, events, anomalies[]
```

These events are **never written to the database** (D-006).

## 4. Metrics (initial set, all candidates; none implemented)

| metric_id | Definition | Inputs | Notes |
|---|---|---|---|
| `boss_cd_uses.v1` | For each boss pull and ability in {Deathmark, Kingsbane}: the count of player casts within `[pull.start, pull.end]` | CastEvent, PullContext | Integer |
| `boss_cd_opportunities.v1` | `1 + floor((alive_ms_in_pull − grace_ms) / cd_ms)`, with a floor of 0. `cd_ms` comes from game data. `grace_ms` (opener setup allowance) comes from rule data | game data, PlayerContext.death_intervals | The formula is a **model**, documented in the finding's limitations |
| `boss_debuff_uptime.v1` | The union of intervals where the player's aura X is on any boss actor, divided by the player's alive time in the pull | AuraEvent, PullContext | Unpaired apply/remove pairs are closed at pull end and counted as an anomaly. If anomalies exceed tolerance, the metric is `invalid` |
| `interrupt_summary.v1` | Successful interrupts by the player; casts of the interrupt ability | InterruptEvent, CastEvent | Fact |
| `death_review.v1` | Per death: time, killing ability, total damage taken in the prior 5 s (top 3 abilities), the player's last use of each defensive before the death and whether `now − last_use ≥ cd_ms` | DeathEvent, DamageEvent, CastEvent, game data | Fact |
| `lethal_poisons_at_pull.v1` | Whether each lethal poison buff was active at each boss pull start | AuraEvent / combatantinfo | Fact |

Each metric result has the shape `{metric_id, version, scope (run|pull), value, unit, status: ok|invalid|not_applicable, inputs_hash, anomalies[]}`.

## 5. Rules
A rule is **data plus a small pure function**, kept in `ascend/analysis/rules/assassination/AR-01.py` with metadata:
```yaml
rule_id: AR-01
rule_version: 1
title: Deathmark usage on bosses
kind: suggestion            # observation | suggestion
spec_ids: [259]
hero_trees: [any]
requires_talents: [deathmark]          # checked against PlayerContext.talents
game_versions: ">=12.1.0,<12.2.0"     # supported window; outside = not evaluated
requires_metrics: [boss_cd_uses.v1, boss_cd_opportunities.v1]
requires_coverage: [Casts]
threshold: {calibration_id: CAL-AR01-S2-001, fire_when: "uses < opportunities AND opportunities - uses >= 1 AND alive_ratio >= 0.9"}
priority_rank: 10
sources: [ROG-02, ROG-03]
explanation_template: "On {boss} you used Deathmark {uses} time(s); the fight allowed up to {opportunities}. ..."
limitations: ["Holding Deathmark for a burst phase can be correct.", "Untargetable phases are not modeled."]
validation: "Cohort CAL-AR01-S2-001; manual review of 20 flagged cases"
```
- **A rule without a `calibration_id` can only be `kind: observation`.** CI enforces this.
- A finding cannot be constructed unless all of the following hold: `requires_metrics` all `ok`; `requires_coverage` all returned; the game version is inside `game_versions`; the talents match. Otherwise the rule emits an **insufficient-evidence** record giving the first failing reason.

## 6. Findings
```text
Finding
  finding_id (uuid), analysis_id, rule_id, rule_version, rule_set_version, game_version, game_data_version
  kind: observation | suggestion | insufficient_evidence
  priority (int, from §7), scope (run | pull:<id>)
  statement (rendered text), key_values {name: value}
  evidence[]: {type: metric|event_ref, metric_id?, value?, report_code, fight_id, pull_id?, ts_ms?, ability_id?}
  confidence: high | medium | low   (rule-defined from coverage and anomalies; never a percentage)
  limitations[] (from rule + runtime, e.g. "1 unpaired Rupture removal")
  recommended_action (from rule template; suggestion only)
  validation_next_run (text from rule: what will be compared next time)
```
There is **no numeric "coaching score"** (directive §8.2).

## 7. Prioritization (deterministic)
The sort key, ascending:
1. `kind`: suggestion before observation before insufficient_evidence.
2. `confidence`: high before medium before low.
3. `rule.priority_rank`: set by hand in rule metadata and justified in the DECISION_LOG, e.g. AR-01 = 10, AR-03 = 20.
4. Magnitude bucket from the rule: large, then moderate, then small. The rule defines the bucket edges from its calibration.
5. Encounter order in the run.
6. `rule_id`, as a tie-break.

The improvement plan takes the first ≤3 `suggestion` findings, de-duplicated by rule (one finding per rule; the worst encounter is shown, the others appear in the evidence).

**Goal relevance (MVP).** The plan text includes the rule's static "why it matters" text. Goal-specific weighting (for example, deaths weighted higher for +12 goals, because of the 15 s penalty) is a post-MVP idea; using it would require evidence and a decision-log entry.

## 8. Missing and abnormal information

| Situation | Detection | Behavior | User sees |
|---|---|---|---|
| No report imported | – | Dashboard only | Import call-to-action |
| Invalid URL | Regex | Reject before network | "That isn't a Warcraft Logs report link" |
| Private report | WCL error or permission | Stop | "This report is private. Make it public or unlisted, or (later) connect WCL." |
| Archived report | `archiveStatus.isAccessible=false` | Stop | "WCL has archived this report" |
| No M+ fights | No `keystoneLevel` | Stop | "No Mythic+ runs in this report" |
| Character not in report | Actor match fails | Stop | List of characters found (names only) |
| Unsupported spec | `spec_id ≠ 259` | Stop | "Only Assassination is supported" |
| Game version outside rule windows | detected version vs rule `game_versions` | Rules not evaluated | "This key was played on patch X; our rules support Y" |
| Partial data (a dataType missing or empty) | Coverage | Dependent rules → insufficient evidence | Per-rule reason |
| Inconsistent data (unpaired auras, events outside pull bounds, non-monotonic timestamps) | Anomaly counters | Metric `invalid` beyond tolerance | "Data quality too low to judge X" |
| Unrecognized spell IDs | Not in game data | Ignored for rules; counted | Limitation note if relevant |
| Missing encounter context (no boss pulls) | No `encounterID ≠ 0` pulls | Boss rules not applicable | "No boss fights detected" |
| API error / timeout | Adapter | Bounded retry, then job fails | "Warcraft Logs didn't respond; retry" |
| Rate limit | 429 / `rateLimitData` | Job deferred until reset | "Queued; finishing in ~N min" |
| Outdated character data | Snapshot age > 24 h | Shown with a stale label; background refresh | Freshness chip |
| Changed mechanics (new patch) | Patch calendar | Rules outside their window are skipped | Version note |

## 9. Versioning
- **`game_version`** of a run is detected from report metadata (`masterData.gameVersion`/`logVersion`; mapping UNVERIFIED) **and** cross-checked against a patch calendar (`gamedata/patches.yaml`: version → regional start dates). On disagreement the run is marked `version_uncertain` and rules requiring an exact window are skipped.
- **`game_data_version`**: an immutable, dated snapshot of spell, cooldown and encounter tables (e.g. `gd-12.1.5-r1`). Changes create a new version; old ones are kept.
- **`rule_set_version`**: the set of rule versions active for a spec (e.g. `assa-12.1-r1`). Every analysis records it.
- **Historical interpretability:** stored findings are never recomputed in place. Re-analysis with a newer rule set creates a **new analysis record** and marks the older one superseded, with both kept. Trends join values only within the same `metric_id@version`.
- **Patch/season process:**
  1. On a patch announcement, the maintainer reviews the patch notes for rule-affecting changes (checklist in CLAUDE.md).
  2. Affected rules either receive a new version with an updated window, or their window closes. They are then not evaluated for new keys until revalidated, and the UI says so.
  3. Season change: replace the season config (dungeons, affixes) and re-run calibration.
- **Fail-safe default:** a rule never extends its `game_versions` automatically.

## 10. Calibration (offline)
- **Purpose:** produce thresholds and magnitude buckets without inventing them.
- **Dataset:** public WCL reports of Assassination Rogues in the same season and patch window, split by hero tree and boss encounter, with keys in the target band (initially +8 to +14). **Target n ≥ 30 per (boss × hero tree)**; cells below that are merged across bosses only if the distributions don't differ (documented).
- **Output:** `calibration/CAL-*.json` with the dataset manifest (report codes are stored in a private, non-committed manifest if the Terms require it), metric distributions, chosen thresholds, the rationale and the reviewer.
- Calibration consumes WCL points; it runs on the project's API key outside peak hours and is subject to the WCL Terms (Gate 3).
- **Acceptance:** the threshold flags ≤ 20% of the calibration cohort, and a manual review of 20 flagged cases finds ≥ 80% where an experienced player agrees the finding is reasonable. If this is not met, the rule stays `observation`.

## 11. Testing
- **Golden fixtures:** sanitized, real reports, once available, plus hand-computed expected metric values. Deterministic snapshot tests compare full findings JSON.
- **Synthetic edge cases**, labeled synthetic in code: no deaths; dying mid-boss; unpaired auras; zero boss pulls; Deathmark talent absent; version outside the window.
- Property tests: uptime is in [0, 1]; uses ≤ opportunities + 1 (anything more is an anomaly flag, a sign of a wrong CD).
- **Cross-check test:** where WCL's own `table(dataType: Debuffs)` uptime exists for the same report, Ascend's uptime must match within 1 percentage point, or the difference must be explained.
