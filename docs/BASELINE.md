# WoW Ascend: Project Baseline

**Baseline date:** 2026-11-02 · **Version:** 1.0 · **Status:** research and architecture complete; **feasibility gates not passed** (see §13). This is the entry point for all future work. The documents it links to hold the detail.

> **Research limitation.** In the research environment, the network policy blocked the primary sites (Blizzard, Warcraft Logs, Archon, Icy Veins, Wowhead, Raider.IO), and no API credentials were available. The findings come from web-search summaries plus directly read open-source code and schema dumps. **No API call to Blizzard or Warcraft Logs has been made, and no real Midnight report has been analyzed.** Each claim's evidence level is recorded in [SOURCE_REGISTER.md](SOURCE_REGISTER.md).

## 1. Executive summary
- **Data path:** documentary evidence suggests the core data is there.
  - Blizzard's API documents character, gear, talent and M+ season-best data.
  - Warcraft Logs' GraphQL schema exposes per-player casts, auras, deaths, interrupts, resources and per-pull boundaries inside Mythic+ keys.
  - Midnight's addon restrictions reportedly leave the combat-log file untouched.
- **The original value proposition is crowded.** At least four products already do AI-written, personalized post-run coaching from WCL logs, and one has Battle.net login and paid tiers. WoWAnalyzer already does deterministic per-spec analysis, though its Assassination module lags patch 12.1.
- **The business model is constrained.** Blizzard's API terms, as quoted in forums, prohibit charging for features that use API data. WCL requires prior approval for commercial use and appears to limit caching.

**Recommendation:** do **not** proceed as originally proposed (a commercial coaching platform). **Proceed conditionally** with a free, narrow validation beta, the "Key Review" for Assassination Rogue, differentiated by deterministic, cited findings and a goal → fix → re-measure loop. Build the coaching engine only after Gates 1, 2 and 4 are PASS and WCL has approved the processing in writing. The public beta needs all five gates PASS.

## 2. Product problem
Players have data and generic AI explanations, but no **trustworthy, prioritized answer tied to their own goal, with follow-up measurement**. This is a hypothesis; see [PRODUCT_REQUIREMENTS.md](product/PRODUCT_REQUIREMENTS.md) §1.

## 3. Target audience
Assassination Rogues in Midnight Season 2 Mythic+, rated about 1,500–3,000, who log or will log their runs. Details: [PRODUCT_REQUIREMENTS.md](product/PRODUCT_REQUIREMENTS.md) §2.

## 4. Product differentiation
**Researched fact:** generic AI log coaching exists (WowCoach.gg, ExplainMyLogs, ParsePal, wow.gg Logs Analyzer). Deterministic analysis exists too (WoWAnalyzer, partial for Midnight Assassination).

**Hypotheses, untested:**
1. Deterministic, cited findings with explicit "not enough evidence" states.
2. A goal-anchored loop that re-measures each finding on later keys.
3. Depth and currency on one spec.

See [COMPETITIVE_LANDSCAPE.md](research/COMPETITIVE_LANDSCAPE.md).

## 5. Research findings (documentary; none live-verified; evidence level shown)
| Finding | Evidence |
|---|---|
| Live: Midnight, patch 12.1.5 (2026-10-13). Season 2 since 2026-08-18. 12.2 and Season 3 announced for "winter" | Multiple press sources (SS) |
| Season 2 M+ pool: Altar of Fangs, Murder Row, Den of Nalorakk, The Blinding Vale, Voidscar Arena, King's Rest, Temple of Sethraliss, Ruby Life Pools | SS, High |
| From +12, each death costs 15 s (Xal'atath's Guile) | SS, High |
| Addons can no longer read combat-log events (secret values). The file log is reportedly unchanged | SS; Medium-High (secondhand quote of the game director, plus WoWAnalyzer support for 12.1.0); no first-hand Blizzard or WCL statement read |
| WCL v2 schema has `ReportFight.keystone*`, `dungeonPulls`, `events(dataType…)` with pagination, `rateLimitData` | **DR** (schema dump, July 2026) |
| WoWAnalyzer supports patches through 12.1.0; its Assassination module is "MaintainedPartial", targeting 12.0.0 | **DR** (repo, 2026-11-02) |
| Blizzard: client-credentials token covers public profiles; `wow.profile` covers the account character list; tokens must be in the header since 2024-09-30; no refresh tokens historically | DR (SDK code) + SS |
| Blizzard exposes M+ **season bests only**, not full run history | SS, Medium |
| Assassination 12.1: Deathmark reworked (75% amplification, restores energy); Crimson Tempest is now a bleed-spreading generator; Kingsbane −15%; Indiscriminate Carnage and Serrated Bone Spike removed | SS, multiple guides |

Details: [WOW_RETAIL_FOUNDATIONS.md](research/WOW_RETAIL_FOUNDATIONS.md), [BLIZZARD_API_CAPABILITIES.md](research/BLIZZARD_API_CAPABILITIES.md), [WARCRAFT_LOGS_FEASIBILITY.md](research/WARCRAFT_LOGS_FEASIBILITY.md), [ASSASSINATION_ROGUE.md](research/ASSASSINATION_ROGUE.md).

## 6. Critical technical constraints
1. Coaching depends entirely on users having **uploaded WCL logs**. M+ logging rates are lower than raid.
2. WCL event JSON is "not frozen": validate everything and fail closed.
3. No raw WCL events are stored (caching terms), so analyses cannot be recomputed later without re-fetching.
4. Blizzard data updates only on logout. A 30-day validity check is mandatory.
5. M+ context (trash, untargetable phases, assignments) can't be reconstructed reliably. The MVP evaluates **boss pulls only**.
6. Patches change the spec's mechanics often. Rules carry version windows and stop when outside them.

## 7. Confirmed data capabilities
**None are confirmed by a live test.** The documentary capability matrices are in [BLIZZARD_API_CAPABILITIES.md](research/BLIZZARD_API_CAPABILITIES.md) §7 and [WARCRAFT_LOGS_FEASIBILITY.md](research/WARCRAFT_LOGS_FEASIBILITY.md) §4.

## 8. Unresolved dependencies
| Item | Owner | Blocks |
|---|---|---|
| Battle.net developer client and WCL API client | Project lead | Gate 1 |
| An unrestricted network for probes | Project lead | Gate 1 |
| A permitted Midnight M+ report with an Assassination Rogue | Project lead | Gates 1, 2 |
| Calibration cohort (≥30 reports per cell) | Developer | Gate 2 |
| Full read of the Blizzard Developer API Terms (§2B, retention, trademark) | Project lead (legal review advised) | Gate 3 |
| WCL written approval, including whether derived data may be stored | Project lead | Gate 3 |
| 15–20 interviews | Project lead | Gate 4 |
| Public product name without "WoW" | Project lead | Launch |

## 9. Proposed MVP scope
**"Key Review"**, in this order:
1. Battle.net login.
2. Pick an Assassination Rogue.
3. Minimal dashboard: Blizzard rating, season bests, gear facts, freshness.
4. Set a goal.
5. Paste a public or unlisted WCL key link.
6. Boss-level findings:
   - **Suggestions (only once calibrated):** AR-01 (Deathmark usage), AR-03 (Rupture uptime) and AR-04 (Garrote uptime).
   - **Observations:** AR-10 (death review), AR-09 (interrupts) and AR-14 (poisons).
7. A plan of at most 3 items.
8. Per-rule history.
9. Privacy controls.

The beta is free, with no ads. Full spec: [MVP_SPECIFICATION.md](product/MVP_SPECIFICATION.md).

## 10. Architecture decision summary
- **Shape:** a modular monolith. FastAPI (Python 3.14) with an in-process Postgres-backed job runner, PostgreSQL 17 on Neon, and a React 19 + Vite + React Router SPA on Cloudflare Pages.
- **Analysis:** a pure, deterministic analysis package. Versioned rules and game data live in the repo.
- **Rejected:** Next.js/Vercel (D-004), and any LLM in the decision path (D-009).

Details: [SYSTEM_ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md), [ANALYSIS_ENGINE.md](architecture/ANALYSIS_ENGINE.md), [DATA_MODEL.md](architecture/DATA_MODEL.md), [DECISION_LOG.md](planning/DECISION_LOG.md).

## 11. Data governance
- No Battle.net passwords, ever.
- No stored provider tokens.
- No raw events.
- Owner-scoped data.
- A 30-day Blizzard validity check.
- Self-service deletion.
- Logs with PII redaction.

See [SECURITY_AND_DATA_POLICY.md](compliance/SECURITY_AND_DATA_POLICY.md).

## 12. Quality requirements
Deterministic analyses, golden fixtures from real sanitized reports, a cross-check against WCL's own tables, calibrated thresholds, and fewer than 5 incorrect findings per 100. See [ACCEPTANCE_CRITERIA.md](quality/ACCEPTANCE_CRITERIA.md) and [FEASIBILITY_TEST_PLAN.md](quality/FEASIBILITY_TEST_PLAN.md).

## 13. Feasibility gate outcomes
| Gate | Status | Evidence | What changes the status |
|---|---|---|---|
| **1. Data feasibility** | **BLOCKED** | Schema and docs are favorable (DR), but there are no credentials, no network and no live report | The Gate 1 tests listed in FEASIBILITY_TEST_PLAN §3 pass on a real Midnight M+ report |
| **2. Coaching feasibility** | **NOT YET TESTED** | 14 candidate rules designed. 3 are suggestion candidates (AR-01, AR-03, AR-04) and 3 are factual observations; nothing is calibrated or validated | The criterion in FEASIBILITY_TEST_PLAN §3: ≥3 insights qualify, of which ≥2 are calibrated suggestions |
| **3. Compliance** | **BLOCKED** | Blizzard §2B monetization restriction (as quoted); WCL commercial approval and caching limits; the terms haven't been read in full; "WoW" trademark risk | Terms read; WCL written approval; name change. *Note: a free, non-commercial beta may be compliant, but that is unconfirmed.* |
| **4. Product differentiation** | **NOT YET TESTED** | Research shows the generic concept is already covered; the narrow differentiators are hypotheses | Interview synthesis meets the criteria in COMPETITIVE_LANDSCAPE §5.4 |
| **5. Delivery feasibility** | **NOT YET TESTED** | Estimate: 140–190 h, about 10–12 weeks at 15–20 h/week, versus the 6–8 week target; about $8/mo infrastructure | Stage 0 completes within ~3 weeks, and the Stage 1–2 actual hours stay within 25% of the estimate |

**No gate has passed.**

## 14. Development roadmap
Stage 0 (feasibility) → Stage 1 (foundation) → Stage 2 (character) → **gate check** → Stage 3 (engine) → Stage 4 (UX) → Stage 5 (validation) → Stage 6 (beta). Realistic total is **10–12 weeks**. Season 3 timing is a decision point. See [ROADMAP.md](planning/ROADMAP.md).

## 15. Launch criteria (public beta)
1. All five gates PASS.
2. Acceptance criteria pass, including the performance and failure-handling criteria.
3. ≥50 beta analyses reviewed, with fewer than 5 wrong per 100.
4. The security review is closed.
5. A privacy page and attribution are published.
6. The public name contains no "WoW".
7. WCL approval is on file.
8. Monthly cost is ≤ $25.
9. The deletion flow is verified in production.

## 16. Explicit exclusions
See [MVP_SPECIFICATION.md](product/MVP_SPECIFICATION.md) §4. In short:
- Other specs; raids.
- Real-time or in-combat help, and automation.
- Simulation and gear optimization.
- Routes; social features; mobile apps.
- Billing and ads.
- An LLM as a source of truth.
- Private WCL reports and avoidable-damage analysis (post-MVP).

## 17. Next recommended engineering task
**Run the Stage 0 data probes** (T-BN-01..06, T-WCL-01..06) from a network that can reach Blizzard and WCL, using real credentials and one permitted Midnight Season 2 key containing an Assassination Rogue. Then run the hand-computation check T-CALC-01 (rule list in the test plan) on that report and compare the results with WCL's own tables. The scripts are ready: [`research/proofs-of-concept/`](../research/proofs-of-concept/). In parallel, the project lead reads both providers' terms and sends the WCL approval email.

---
**Document index:**
- [README](../README.md) · [CLAUDE.md](../CLAUDE.md) · [Glossary](GLOSSARY.md) · [Sources](SOURCE_REGISTER.md)
- **Research:** [Foundations](research/WOW_RETAIL_FOUNDATIONS.md) · [Competitors](research/COMPETITIVE_LANDSCAPE.md) · [Blizzard API](research/BLIZZARD_API_CAPABILITIES.md) · [Warcraft Logs](research/WARCRAFT_LOGS_FEASIBILITY.md) · [Assassination](research/ASSASSINATION_ROGUE.md)
- **Product:** [Requirements](product/PRODUCT_REQUIREMENTS.md) · [MVP](product/MVP_SPECIFICATION.md)
- **Architecture:** [System](architecture/SYSTEM_ARCHITECTURE.md) · [Analysis engine](architecture/ANALYSIS_ENGINE.md) · [Data model](architecture/DATA_MODEL.md)
- **Compliance:** [Security & data](compliance/SECURITY_AND_DATA_POLICY.md)
- **Planning:** [Roadmap](planning/ROADMAP.md) · [Cost](planning/COST_MODEL.md) · [Risks](planning/RISK_REGISTER.md) · [Decisions](planning/DECISION_LOG.md)
- **Quality:** [Acceptance](quality/ACCEPTANCE_CRITERIA.md) · [Feasibility tests](quality/FEASIBILITY_TEST_PLAN.md)
