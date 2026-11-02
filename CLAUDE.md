# CLAUDE.md: Development Instructions for WoW Ascend

These instructions are binding for every AI-assisted session in this repository. Read [docs/BASELINE.md](docs/BASELINE.md) first.

## 1. Mission
Help Mythic+ players improve through **accurate, checkable, evidence-backed findings** tied to their own goals. Trustworthiness beats breadth. A finding we can't support must be shown as "not enough evidence", or not shown at all.

## 2. Current phase and gates
- The project is in **Stage 0 (feasibility)**. Check the gate table in BASELINE §13 before starting any stage.
- **Do not build the coaching engine (Stage 3) until Gates 1 and 2 are PASS** in BASELINE.md, with linked evidence.
- Never mark a gate PASS without evidence the user can inspect: a test output, a fixture, or a written provider reply.

## 3. Accepted architecture (see docs/planning/DECISION_LOG.md)
- **Shape:** a modular monolith. FastAPI with an in-process job runner, PostgreSQL 17, and a React SPA (Vite + React Router + TanStack Query) on static hosting.
- **No** microservices, message brokers, Redis, Kubernetes or Next.js without a new DECISION_LOG entry that justifies it with evidence.
- **Boundaries:** `ascend.analysis` is pure. It never imports providers, the DB or the web layer. Routers → services → repositories/providers.
- All provider access goes through adapters in `ascend.providers.*`, with timeouts, bounded retries (at most 4, full jitter) and rate limiting.
- **Changing an accepted decision:** add a new DECISION_LOG entry that supersedes the old one, with its reasoning. Never silently contradict an accepted decision.

## 4. Coding standards
- **Python 3.14:** type hints everywhere; Pydantic models at every boundary; ruff and mypy (strict on `analysis/`).
- **TypeScript:** strict; generated API client; no `any` in domain code.
- **Code style:** small modules, explicit names, no clever metaprogramming. Comments explain *why*.
- Dependencies are pinned, and each new one is justified in the pull request. Don't add dependencies the task doesn't need.

## 5. Research requirements
- WoW changes every patch. **Before you write or change any rule, spell ID, cooldown, dungeon or season data, verify it against a current source** and record it in `docs/SOURCE_REGISTER.md` with its date and confidence.
- Evidence hierarchy:
  1. Official Blizzard.
  2. Live API test.
  3. Official WCL.
  4. Maintained project docs and code.
  5. Theorycrafting guides.
  6. Community.
  7. Historical (label it so).
- **Never invent** endpoints, fields, event types, mechanics, numbers, thresholds or terms. If something is unknown, write UNVERIFIED and leave it out of the logic.

## 6. Data provenance rules
- Every stored value is `provider`, `derived`, `user` or `system`. Provider data records the endpoint and `fetched_at`.
- Missing provider values are `NULL` plus a reason; never `0` or `""`.
- **Never persist raw WCL events or raw provider responses** in production (D-006).
- Ascend never computes a Mythic+ rating; it displays Blizzard's (D-016).

## 7. API security requirements
- Never request, accept or log Battle.net passwords.
- Battle.net user tokens are discarded after login (D-005). Provider tokens are never logged or stored unencrypted.
- Secrets live only in environment variables; `.env` is git-ignored. Run the secret scan before committing.
- Every data query is scoped by `user_id`. Add an IDOR test for each new endpoint.
- Analyze only reports that contain the signed-in user's own character (D-013). Never expose another user's report codes.
- Commit only sanitized fixtures (`research/fixtures/sanitized/`, or `tests/fixtures/`), and review them by hand first.

## 8. Game-versioning requirements
- Every rule declares `game_versions`, `spec_ids`, required talents, required metrics and coverage, and either a `calibration_id` (for suggestions) or nothing (for observations).
- **A rule's window is never widened automatically.** On a new patch, run the checklist below; rules outside their window are skipped, with an insufficient-evidence reason.
- Stored analyses are immutable. Re-analysis creates a new analysis record. Trends never mix metric versions.
- **Patch-review checklist** (within 7 days of a patch going live):
  1. Read the patch notes and hotfixes for the class.
  2. List the affected rules and spell IDs.
  3. Re-verify against at least 2 current sources.
  4. Bump the rule and game-data versions or close their windows.
  5. Re-run calibration if a threshold depends on a changed mechanic.
  6. Update the SOURCE_REGISTER and DECISION_LOG.

## 9. Testing requirements
- Every metric needs at least 3 fixture tests with hand-computed expected values; at least 1 must come from a real sanitized report.
- Every rule needs tests for: it fires, it doesn't fire, and insufficient evidence (one test per failing precondition).
- Determinism test: running twice must give byte-identical output.
- Contract tests for provider payloads, plus fault-injection tests (timeout, 429, malformed JSON).
- Integration tests use real Postgres. E2E (Playwright) covers the critical flow.
- **Never skip, disable or loosen a test to get green.**

## 10. Development workflow
1. Read BASELINE.md and the relevant design doc.
2. Confirm the stage and gate prerequisites.
3. Work on a feature branch, in small commits.
4. Run `make check` (lint, types, tests, import-linter, secret scan, audit) locally.
5. Update docs (§13).
6. Open a pull request only when asked.

## 11. Definition of Done
- Acceptance criteria for the feature pass (`docs/quality/ACCEPTANCE_CRITERIA.md`), and their tests are automated.
- CI is green; there are no new warnings in the type checks.
- Docs are updated, including the DECISION_LOG entry if a decision changed.
- No secrets, raw provider data or PII in the diff.
- Loading, empty and error states exist for any new UI.
- Any user-visible finding text follows the wording rules in MVP_SPECIFICATION §2.

## 12. Prohibited shortcuts
- Inventing data, thresholds, or "typical" values to make a feature work.
- Using an LLM to decide whether a finding is true or important (D-009).
- Scraping provider websites, or using users' cookies or sessions.
- Addon-based data collection that circumvents Blizzard's secret values, memory reading, or in-combat assistance.
- Storing raw events "temporarily" in the DB or object storage.
- Marking gates or tests as passing without evidence.
- Adding monetization, ads or tracking before Gate 3 clears it (D-010).
- Committing `research/fixtures/raw/` or `.env`.

## 13. Documentation update requirements
- A behavior or scope change means updating the relevant doc in `docs/` in the same pull request.
- A new or changed decision means a DECISION_LOG entry.
- A new external fact means a SOURCE_REGISTER entry (ID, URL, date, confidence, verification status).
- A gate status change means updating BASELINE §13 with the evidence link.
- A new risk, or a risk that has materialized, means updating the RISK_REGISTER.
