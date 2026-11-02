# Product Requirements

**Date:** 2026-11-02 · **Status:** Baseline v1. This is a proposal and is conditional on the feasibility gates (see [BASELINE.md](../BASELINE.md)).

## 1. Problem
Mythic+ players who want to improve have plenty of *data*: Warcraft Logs, Raider.IO, the in-game meter. They also have *generic AI explanations*. What they lack is a **short, trustworthy answer to "what is the one thing I should fix next for my goal, and did it work?"** This is a hypothesis (H1–H4 in [COMPETITIVE_LANDSCAPE.md](../research/COMPETITIVE_LANDSCAPE.md) §5) and is **not yet validated by user research**.

## 2. Target audience (MVP)
- **Primary:** Assassination Rogue players in Midnight Season 2 M+, rated roughly 1,500–3,000, who upload or are willing to upload WCL logs.
- **Secondary (research only):** other DPS players, interviewed to test whether the format generalizes.
- **Not targeted:** top-0.1% pushers (they already have the expertise and tooling), raid-only players, Classic players.

## 3. Value proposition (revised after research)
The original promise was: *"Connect your character. Understand what's holding you back. Know exactly what to improve next."* Research shows the middle clause is already offered by AI log tools. The revised positioning:

> **Evidence you can check, a plan tied to your goal, and proof of whether you improved.**

Differentiators to test:
1. **Deterministic, cited findings.** Every finding shows the exact numbers, timestamps and the rule behind it. When the evidence is insufficient, Ascend says so instead of guessing.
2. **Goal-anchored loop.** Set goal → top 1–3 findings → play → re-measure the same findings on the next keys.
3. **Current, deep spec logic** for Assassination, updated to 12.1.

## 4. Product principles (binding)
1. Fact, suggestion and insufficient evidence are always visually and textually distinct.
2. No finding without a valid rule version and the evidence it requires.
3. No invented numbers: no Ascend "score", no unsourced thresholds.
4. Simple surface, depth on demand.
5. Private by default.
6. Free and non-commercial until compliance permits otherwise.

## 5. Functional requirements

| ID | Requirement | Priority | Gate dependency |
|---|---|---|---|
| FR-01 | Sign in with Battle.net (OAuth authorization code); no password handling | MVP | G3 |
| FR-02 | List the account's WoW Retail characters; let the user add one or more (one at a time) | MVP | G1 (account endpoint fields) |
| FR-03 | Character dashboard: name, realm, class/spec, level, item level, equipped items with enchant/gem presence, current M+ rating, season best runs per dungeon, data freshness | MVP | G1 |
| FR-04 | Set one progression goal per character: a target M+ rating, or a target key level timed in a named or any dungeon | MVP | – |
| FR-05 | Import a Warcraft Logs report by URL (public; unlisted only if T-WCL-07 confirms client access); select the key run; auto-detect the user's character in the report | MVP | G1, G3 |
| FR-06 | Reject reports that don't contain one of the user's characters, aren't M+, are an unsupported spec, or are from an unsupported game version, each with a specific message | MVP | – |
| FR-07 | Compute verified metrics for the supported rule set; persist derived results only | MVP | G1, G2, G3 |
| FR-08 | Produce findings (observed fact / suggested improvement / insufficient evidence), each with evidence, confidence, limitations and rule version | MVP | G2 |
| FR-09 | Improvement plan: the top 1–3 suggested improvements, ordered by a transparent deterministic priority | MVP | G2 |
| FR-10 | History: per character, the list of analyses and a per-rule trend across analyses ("Deathmark usage on bosses: 2/3 → 3/3"), split by rule version | MVP | – |
| FR-11 | Privacy settings: view stored data, delete an analysis, delete a character, delete the account | MVP | G3 |
| FR-12 | Re-fetch character data on demand (rate-limited) and automatically when stale (>24 h) on visit | MVP | – |
| FR-13 | Private WCL reports via WCL user OAuth | Post-MVP | G3 |
| FR-14 | Additional specs | Post-MVP | G2 per spec |
| FR-15 | Calibration-Chamber practice suggestions (12.2) | Post-MVP | 12.2 release |
| FR-16 | Optional AI-phrased explanations of deterministic findings (never the source of truth) | Post-MVP | – |

## 6. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-01 | Character dashboard first contentful render ≤ 2.0 s p75 on a mid-range mobile on 4G, warm API cache |
| NFR-02 | Report analysis completes ≤ 60 s p90 for a 40-minute key (WCL fetch-bound) and shows progress states |
| NFR-03 | Analysis is deterministic: the same report, rule-set version and game-data version give byte-identical findings |
| NFR-04 | No raw provider event data persisted |
| NFR-05 | All provider calls go through adapters with timeouts, bounded retries and rate limiting |
| NFR-06 | WCAG 2.2 AA for core flows |
| NFR-07 | Operable by one developer: one backend service (with in-process job runner), one database; deploy in under 10 minutes |
| NFR-08 | Monthly infrastructure cost ≤ $25 through the 50-user beta |

## 7. Success metrics (beta)
These are measured from Ascend's own data, with no invented baselines:
- Activation: % of sign-ups who complete one analysis.
- **Return rate:** % of users who import a second report within 14 days. *Primary signal for H4.*
- **Finding persistence:** for users with ≥2 analyses, the share of previously flagged findings that are no longer flagged. Interpret cautiously, since it isn't causal.
- **Reported incorrect findings** per 100 findings, via the in-app "This looks wrong" control. Target: < 5, each one reviewed.
- Qualitative: post-beta interviews.

## 8. Explicit exclusions
See [MVP_SPECIFICATION.md](MVP_SPECIFICATION.md) §4.
