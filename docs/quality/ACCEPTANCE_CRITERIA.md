# MVP Acceptance Criteria

**Date:** 2026-11-02 · **Status:** Baseline v1. Each criterion is testable. *Verification* names the method: **U** unit, **I** integration, **E** end-to-end (Playwright), **M** manual review, **P** performance measurement, **R** code or config review.

## Authentication (FR-01)
| ID | Criterion | Verification |
|---|---|---|
| AC-AUTH-01 | A user can sign in with Battle.net for a chosen region, and an account row is created on the first successful callback only | I (mock provider), E |
| AC-AUTH-02 | A callback with a missing, reused or mismatched `state` is rejected (400) and creates no session | I |
| AC-AUTH-03 | No page, form or API ever accepts a Battle.net password | R + E (grep and form audit) |
| AC-AUTH-04 | Session cookie is HttpOnly, Secure, SameSite=Lax; only the token's SHA-256 is stored | I |
| AC-AUTH-05 | Logout invalidates the session server-side; the old cookie then returns 401 | I |
| AC-AUTH-06 | Battle.net access tokens appear in no DB table and no log line | I (log capture plus DB scan after login) |
| AC-AUTH-07 | "Disconnect / delete account" removes every user-owned row, and the session stops working | I (row counts before and after) |

## Character import and dashboard (FR-02, FR-03, FR-12)
| ID | Criterion | Verification |
|---|---|---|
| AC-CHAR-01 | The character list shows only Retail characters returned by the account endpoint | I (fixture) |
| AC-CHAR-02 | Every dashboard field maps to a named provider field, or shows "unavailable" with no fabricated default | U (mapping table test) + M |
| AC-CHAR-03 | Item level is taken from `level.value` in equipment, and the character's average/equipped item level from the summary | U |
| AC-CHAR-04 | The freshness chip shows `fetched_at`; data older than 24 h is labeled stale | U + E |
| AC-CHAR-05 | A 404 from Blizzard shows the "not sharing" message and hides prior data as non-current | I |
| AC-CHAR-06 | A partial endpoint failure affects only its own card | I |
| AC-CHAR-07 | The M+ rating shown equals Blizzard's `mythic_rating.rating`; Ascend computes no rating | U |
| AC-CHAR-08 | Characters failing the 30-day `/status` check are deleted together with dependent data, and the owner sees a one-time notice | I (time-travel test) |
| AC-CHAR-09 | Manual refresh is limited to 1 per 5 minutes per character; extra requests get 429 and a clear message | I |
| AC-CHAR-10 | Opening a dashboard whose snapshot is older than 24 h enqueues exactly one refresh (deduplicated) | I |
| AC-CHAR-11 | A user can add several characters, one at a time, and each appears in their stored list | E |

## Goals (FR-04)
| ID | Criterion | Verification |
|---|---|---|
| AC-GOAL-01 | A user can set one active goal per character (rating or key level, optionally a dungeon) | I |
| AC-GOAL-02 | Goal progress is shown only from Blizzard data, e.g. current rating against the target, or the best timed level in the target dungeon | U |
| AC-GOAL-03 | "Achieved" is set only when Blizzard data meets the target | U |

## Combat report import (FR-05, FR-06)
| ID | Criterion | Verification |
|---|---|---|
| AC-IMP-01 | Non-WCL or malformed URLs are rejected before any network call | U |
| AC-IMP-02 | Importing the same report and key twice for the same character returns the existing import (idempotent) | I |
| AC-IMP-03 | Private, archived and inaccessible reports produce their specific error codes and no analysis | I (fixtures) |
| AC-IMP-04 | Reports without M+ fights, without the user's character, without Assassination, or from a game version outside every rule set's window are rejected with specific codes, and no analysis is created | I |
| AC-IMP-05 | After a job finishes, no raw event data exists in the DB or on disk | I (scan the tables for event-shaped JSON; check the temp dir) |
| AC-IMP-06 | An unlisted report code imported by user A is never visible to user B | I (IDOR) |
| AC-IMP-07 | When WCL points are insufficient, the job is deferred (not failed) and the UI says it is queued | I |
| AC-IMP-08 | Once a report is detected as unsupported, no further WCL calls are made for it | I (call-count assertion) |

## Metrics
| ID | Criterion | Verification |
|---|---|---|
| AC-MET-01 | Each metric has a versioned ID, a written definition and ≥3 fixture tests with known expected outputs, of which ≥1 comes from a real sanitized report | U |
| AC-MET-02 | Same inputs, same rule set and same game-data version produce byte-identical metric output | U (run twice) |
| AC-MET-03 | Debuff **active time** (numerator, ms) on a boss target is within ±1% of the active duration in WCL's own Debuffs table for the same report, target and time range. Percentages aren't compared, because Ascend's denominator (player alive time in the pull) may differ from WCL's (UNVERIFIED) | U (cross-check fixture) |
| AC-MET-04 | Metrics whose inputs are missing or anomalous return `invalid` or `not_applicable`, never a number | U |

## Coaching (FR-07..FR-09)
| ID | Criterion | Verification |
|---|---|---|
| AC-COACH-01 | A `suggestion` cannot be persisted without non-empty evidence, a rule version and a recommended action (enforced by a DB CHECK and application validation) | U + I |
| AC-COACH-02 | Rules outside their `game_versions` window, or lacking required talents or coverage, emit an `insufficient_evidence` record with a reason | U |
| AC-COACH-03 | No rule of kind `suggestion` exists without a `calibration_id` (CI check) | R (CI script) |
| AC-COACH-04 | The improvement plan contains ≤3 items, ordered exactly by the documented priority function | U |
| AC-COACH-05 | In the beta, incorrect-finding reports are < 5 per 100 findings, and each one is reviewed and root-caused | M |

## Explainability
| ID | Criterion | Verification |
|---|---|---|
| AC-EXPL-01 | Every finding card shows its kind label (Observed / Suggested improvement / Not enough evidence) | U (component) + E |
| AC-EXPL-02 | Every suggestion shows its key values, the encounter, the rule ID and version, limitations, sources and a WCL deep link | E |
| AC-EXPL-03 | Every number in finding text appears in that finding's `key_values` or evidence | U (template test) |
| AC-EXPL-04 | The analysis page lists every rule that was not evaluated, with the reason | E |

## Progression (FR-10)
| ID | Criterion | Verification |
|---|---|---|
| AC-PROG-01 | History trends show only stored derived values; there is no interpolation or projection | U |
| AC-PROG-02 | Trends are per rule; values from different `rule_id@rule_version` are never shown as one continuous trend | U |
| AC-PROG-03 | Rating snapshots are shown against the active goal using Blizzard values only | U + E |

## Privacy (FR-11)
| ID | Criterion | Verification |
|---|---|---|
| AC-PRIV-01 | A user can list, and delete, each stored analysis, character and their account | E |
| AC-PRIV-02 | A privacy page describing collected data, retention, providers and deletion is reachable from every page | E |
| AC-PRIV-03 | Logs redact tokens, cookies, BattleTags and character names | U (redaction test) |
| AC-PRIV-04 | Attribution and a "not affiliated with Blizzard" notice appear in the footer | E |

## Performance (NFR-01, NFR-02)
| ID | Criterion | Verification |
|---|---|---|
| AC-PERF-01 | Dashboard LCP ≤ 2.0 s at p75 (Lighthouse mobile, simulated 4G, warm API) | P (Lighthouse CI) |
| AC-PERF-02 | API p95 ≤ 300 ms for read endpoints at 10 rps on the Starter instance | P (load test) |
| AC-PERF-03 | Analysis ≤ 60 s at p90 for a ≥35-minute key, measured over ≥10 real reports | P |
| AC-PERF-04 | Peak memory of one analysis job ≤ 350 MB on the largest fixture | P |

## Failure handling
| ID | Criterion | Verification |
|---|---|---|
| AC-FAIL-01 | WCL or Blizzard timeouts, 5xx or 429 never produce findings; the job retries with bounded backoff and then fails with a code | I (fault injection) |
| AC-FAIL-02 | Malformed or unexpected event JSON fails the dependent metric only, never the process, and is reported as a data-quality limitation | U |
| AC-FAIL-03 | Provider error bodies are never shown to users | I |

## Maintainability
| ID | Criterion | Verification |
|---|---|---|
| AC-MAINT-01 | `ascend.analysis` imports no provider, DB or web modules (import-linter in CI) | R (CI) |
| AC-MAINT-02 | Adding a new rule version or a game-data version requires no changes outside `analysis/rules/`, `gamedata/` and tests | R (demonstrated by a dry run in Stage 3) |
| AC-MAINT-03 | Swapping a provider for its fixture replay requires only configuration | I |

## Landing, feedback, accessibility, operations
| ID | Criterion | Verification |
|---|---|---|
| AC-LAND-01 | The landing page renders with no JS errors, scores Lighthouse accessibility ≥ 95, and shows only a sample finding that is labeled "Example" and built from a sanitized fixture | P + E |
| AC-FEED-01 | Each finding has a "This looks wrong" control with verdicts wrong / unclear / helpful (plus an optional comment ≤ 2,000 chars); one verdict per user per finding, editable | I + E |
| AC-FEED-02 | Every `wrong` verdict appears in a review queue that the maintainer works through (Stage 5) | M |
| AC-A11Y-01 | Core flows (S2–S7, S9) meet WCAG 2.2 AA: axe reports no serious or critical violations, and the flows can be completed by keyboard only | E (axe) + M |
| AC-OPS-01 | A deploy from merge to live takes < 10 minutes, and a rollback to the previous release works | M (timed drill) |

## Stage mapping
Each criterion is implemented, and its automated test written, in the stage listed. Manual verifications happen in that stage, unless the criterion says otherwise.

| Stage | Criteria |
|---|---|
| 1 Foundation | AC-AUTH-01..07, AC-PRIV-03, AC-MAINT-01, AC-OPS-01 |
| 2 Character | AC-CHAR-01..11, AC-GOAL-01..03, AC-LAND-01, AC-PRIV-04 |
| 3 Engine | AC-IMP-01..08, AC-MET-01..04, AC-COACH-01..04, AC-FAIL-01..03 (implemented), AC-PERF-03, AC-PERF-04, AC-MAINT-02, AC-MAINT-03 |
| 4 UX | AC-EXPL-01..04, AC-PROG-01..03, AC-PRIV-01..02, AC-FEED-01, AC-A11Y-01, AC-PERF-01 |
| 5 Validation | AC-COACH-05, AC-FEED-02, AC-PERF-02, AC-FAIL-01..03 (fault-injection run against the deployed beta) |
