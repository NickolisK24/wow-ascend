# Delivery Roadmap

**Date:** 2026-11-02 · **Capacity assumption:** 15–20 focused hours per week, one developer · **Status:** Baseline v1. This is a planning hypothesis, not a commitment.

## 1. Summary
| Stage | Hours (est.) | Calendar (at ~17 h/wk) | Hard dependency |
|---|---|---|---|
| 0 Research & feasibility (remaining) | 25–35, of which ~15 is interviews | Weeks 1–2, with interviews spread over weeks 1–4 | Credentials, network access |
| 1 Foundation | 20–25 | Weeks 2–3 | Gate 3 (Blizzard part) not FAIL |
| 2 Character experience | 15–20 | Weeks 3–4 | Stage 1 |
| 3 Coaching engine | 35–45 | Weeks 4–7 | **Gates 1 and 2 PASS** |
| 4 User experience | 15–20 | Weeks 7–8 | Stage 3 |
| 5 Validation | 15–20 | Weeks 8–9 | Stage 4; ≥8 beta testers |
| 6 Public beta | 5–10 | Week 10 | Gates 3, 4 and 5 PASS; launch criteria |
| **Total** | **130–175 h** | **≈ 9–11 weeks** | |

**Realism check:** the requested 6–8 weeks is achievable only if Stage 0 interviews run fully in parallel and nothing in Stage 3 needs rework. **The realistic estimate is 9–11 weeks**, which puts the beta around mid-January 2027.

**Season risk:** Patch 12.1.7 is expected around December 2026 (date unconfirmed). Patch 12.2 and Season 3 are announced for winter 2026–27, also without a date. Season 3 replaces the whole dungeon pool and may change Assassination. **Decision point at the end of Stage 3:** launch the beta on Season 2 data, accepting a short shelf life, or hold until Season 3 and recalibrate. The rule-versioning design supports either choice.

**Critical path:** credentials → live probe (T-WCL-01..06) → calibration of AR-01/AR-03 → engine → validation with real players. Character features (Stages 1–2) are off the critical path and can be built while waiting on WCL Terms replies.

## 2. Stages

### Stage 0: Research and feasibility (remaining work)
- **Goal:** turn BLOCKED and NOT YET TESTED gates into evidence.
- **Dependencies:**
  - Battle.net developer account with 2FA.
  - WCL API client.
  - An unrestricted network.
  - Permission to use 1+ Midnight M+ report containing an Assassination Rogue.
- **Deliverables:**
  - Probe runs: T-BN-01..08 and T-WCL-01..08 (see [FEASIBILITY_TEST_PLAN.md](../quality/FEASIBILITY_TEST_PLAN.md)).
  - Sanitized fixtures committed.
  - Hand-computed AR-01/AR-03/AR-10 on ≥3 reports, cross-checked against WCL's own tables.
  - A first calibration pass for AR-01 and AR-03 (≥30 reports per main cell).
  - Terms read in full (Blizzard and WCL) and the WCL approval email sent.
  - A name decision.
  - 15–20 interviews.
- **Hours:** 25–35.
- **Milestones:**
  - M0.1 probes green.
  - M0.2 calibration report.
  - M0.3 interview synthesis.
  - M0.4 compliance memo.
- **Acceptance criteria:**
  - Each gate in [BASELINE.md](../BASELINE.md) is updated with evidence links.
  - Every UNVERIFIED item that blocks the MVP is resolved or explicitly re-scoped.
- **Tests:** none beyond the probes and sanitizer tests.
- **Risks:**
  - The WCL Terms reply could be slow or negative.
  - The calibration cohort may be too thin.
- **Exit conditions:**
  - **Proceed to Stage 3 only if Gates 1 and 2 PASS.**
  - **Stop or pivot** if Gate 1 FAILs (needed events absent) or Gate 3 FAILs (processing prohibited).
  - If Gate 4 FAILs (users prefer existing tools), stop or re-scope before building Stage 3.

### Stage 1: Foundation
- **Goal:** a deployable skeleton with authentication.
- **Dependencies:** Stage 0 compliance memo shows Blizzard usage is permitted for a free product.
- **Deliverables:**
  - Monorepo (`backend/`, `frontend/`).
  - CI covering lint, types, tests, import-linter, secret scan and audit.
  - Docker Compose Postgres.
  - Alembic baseline matching [DATA_MODEL.md](../architecture/DATA_MODEL.md).
  - Battle.net OAuth login and logout; sessions.
  - `/me`.
  - Provider adapter interfaces plus fixture replay mode.
  - Structured logging with redaction; Sentry.
  - Deploys to Render and Cloudflare Pages.
  - `.env.example`.
- **Hours:** 20–25.
- **Milestones:**
  - M1.1 CI green on an empty app.
  - M1.2 login works in production.
- **Acceptance criteria:** AC-AUTH-01..06 ([ACCEPTANCE_CRITERIA.md](../quality/ACCEPTANCE_CRITERIA.md)).
- **Tests:**
  - OAuth state tests.
  - Session tests.
  - Redaction tests.
  - Migration up/down test.
- **Risks:**
  - TypeScript 7 tooling incompatibility; fall back to 6.x.
  - Battle.net redirect rules.
- **Exit conditions:**
  - Login, logout and account deletion work in production.
  - No secrets appear in the repository.

### Stage 2: Character experience
- **Goal:** character import, dashboard and goals.
- **Dependencies:** Stage 1.
- **Deliverables:**
  - Character list.
  - Add a character.
  - Refresh job.
  - Snapshot normalization (`snapshot.v1`).
  - Dashboard (S4) with freshness labels and M+ season bests.
  - Goal setter.
  - Nightly 30-day status-check job.
  - Season and dungeon config for Season 2.
- **Hours:** 15–20.
- **Milestones:**
  - M2.1 dashboard shows real data for the developer's own character.
- **Acceptance criteria:** AC-CHAR-01..07 and AC-GOAL-01..03.
- **Tests:**
  - Contract tests on Blizzard fixtures.
  - 404 and partial-failure handling.
  - Retention job deletion test.
- **Risks:** Blizzard data staleness (updates on logout) confuses users. Mitigated by freshness copy in the UI.
- **Exit conditions:** acceptance criteria pass, and a 2-person dogfood test completes.

### Stage 3: Coaching engine
- **Goal:** deterministic findings from real reports.
- **Dependencies:** Gates 1 and 2 PASS; calibration files exist for AR-01 and AR-03.
- **Deliverables:**
  - WCL adapter with pagination, points accounting and bounds.
  - Import API with idempotency.
  - Job runner.
  - Contracts and normalizer.
  - Metrics: `boss_cd_uses`, `boss_cd_opportunities`, `boss_debuff_uptime`, `interrupt_summary`, `death_review`, `lethal_poisons_at_pull`.
  - Rules: AR-01, AR-03/04, AR-09, AR-10 and AR-14, at their qualified kinds.
  - Prioritizer.
  - Explanation templates.
  - Game-data version `gd-12.1.5-r1`; rule set `assa-12.1-r1`.
  - Golden tests.
- **Hours:** 35–45.
- **Milestones:**
  - M3.1 the first fixture produces findings identical to the hand computation.
  - M3.2 three real reports from different players pass the cross-check.
- **Acceptance criteria:** AC-IMP-*, AC-MET-*, AC-COACH-*.
- **Tests:**
  - Golden fixtures.
  - Property tests.
  - Cross-check against WCL tables.
  - Synthetic edge cases.
  - Determinism (run twice, compare bytes).
- **Risks:**
  - Event-ordering quirks.
  - Memory use on large keys.
  - Points cost higher than assumed.
- **Exit conditions:**
  - Every MVP rule passes its validation method.
  - Any rule that fails is demoted to an observation or removed, and the change is logged.

### Stage 4: User experience
- **Goal:** the full loop is usable on mobile.
- **Dependencies:** Stage 3.
- **Deliverables:**
  - S5–S9 polished.
  - Improvement plan.
  - History trends.
  - Onboarding copy.
  - Privacy page.
  - "This looks wrong" feedback.
  - Accessibility pass.
- **Hours:** 15–20.
- **Milestones:**
  - M4.1 a new user completes the loop without help (hallway test, n=3).
- **Acceptance criteria:** AC-EXPL-*, AC-PROG-*, AC-PRIV-*, AC-PERF-01.
- **Tests:**
  - Playwright E2E for the critical flow.
  - axe accessibility checks.
  - Lighthouse.
- **Risks:** copy that over-claims. Mitigated by a copy review against the wording rules in the MVP spec §2.
- **Exit conditions:** E2E green, and accessibility ≥ AA on the core screens.

### Stage 5: Validation
- **Goal:** prove the findings are correct and useful with real players.
- **Dependencies:** 8–15 beta testers recruited from the interviews.
- **Deliverables:**
  - Closed beta.
  - Review of every "wrong" flag.
  - Analysis of incorrect recommendations.
  - Security review (ASVS L1 subset).
  - Load test of a 10-concurrent-import burst.
  - Incident runbook.
  - Backup and restore drill.
- **Hours:** 15–20.
- **Milestones:**
  - M5.1 50 analyses reviewed.
  - M5.2 security review closed.
- **Acceptance criteria:**
  - Incorrect findings < 5 per 100, with each one root-caused.
  - No high or critical security issues open.
  - AC-FAIL-* pass.
- **Tests:**
  - Manual review protocol.
  - Chaos tests (WCL timeout, 429, malformed events).
- **Risks:**
  - Low tester engagement.
  - Systematic false positives.
- **Exit conditions:**
  - Gate 4 re-evaluated on beta data.
  - Gate 5 confirmed.

### Stage 6: Public beta
- **Goal:** a limited, free, public launch.
- **Dependencies:** all gates PASS; launch criteria in BASELINE §15.
- **Deliverables:**
  - Public name and domain.
  - Launch post to the communities where moderators gave permission.
  - Monitoring dashboard.
  - Feedback channel.
- **Hours:** 5–10.
- **Milestones:**
  - M6.1 the first 50 external users.
- **Acceptance criteria:**
  - Error rate < 1% of requests.
  - Import success ≥ 90% for valid supported reports.
- **Tests:** smoke tests post-deploy.
- **Risks:**
  - A traffic spike on the WCL budget. Mitigated by the per-user caps and the queue.
- **Exit conditions:** a review four weeks after launch (keep, pivot or stop), recorded in the DECISION_LOG.
