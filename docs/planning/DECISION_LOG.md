# Decision Log

An accepted decision may be changed only by adding a new entry that **supersedes** it, with its reasoning. Never edit an accepted entry's decision text; append instead.

Status values: **Accepted** · **Proposed** (awaiting a gate or owner approval) · **Superseded by D-xxx**

| ID | Date | Decision | Status | Rationale | Evidence | Revisit when |
|---|---|---|---|---|---|---|
| D-001 | 2026-11-02 | Retail only; regions US/EU/KR/TW; China excluded | Accepted | Separate China API, legal and hosting setup | `BNET-02` | Demand from China |
| D-002 | 2026-11-02 | **MVP spec: Assassination Rogue only** | Accepted | Directive; depth over breadth; the WoWAnalyzer module lags 12.1 | ASSASSINATION_ROGUE.md | After beta |
| D-003 | 2026-11-02 | Modular monolith: FastAPI with an in-process job runner, one Postgres | Accepted | Solo developer, low cost, NFR-07 | SYSTEM_ARCHITECTURE.md | Split triggers in §9 |
| D-004 | 2026-11-02 | Frontend is a **Vite + React Router SPA on Cloudflare Pages**, not Next.js/Vercel | Accepted | No SSR need; one server runtime; Vercel Hobby bans commercial use | `COST-01` | Public indexable pages become a requirement |
| D-005 | 2026-11-02 | Battle.net **user tokens are not persisted**. Character refresh uses the client-credentials token against public profile endpoints | Accepted | No refresh token (historical); minimizes stored secrets | `BNET-07` | If Blizzard issues refresh tokens, or a protected endpoint becomes necessary |
| D-006 | 2026-11-02 | **No raw WCL events persisted.** Process in memory; store derived metrics and evidence references only | Accepted (derived storage pending W2) | WCL cache-header restriction; privacy | `WCL-09` | Written WCL response |
| D-007 | 2026-11-02 | No rule may produce a *suggestion* without a calibration dataset; uncalibrated rules are observations only | Accepted | Directive: no invented thresholds | ANALYSIS_ENGINE §5, §10 | – |
| D-008 | 2026-11-02 | MVP coaching rules are AR-01 and AR-03/04 (suggestions); AR-09, AR-10 and AR-14 are observations. Boss pulls only | Proposed (needs Gates 1 and 2) | Only these are defensible on current evidence | ASSASSINATION_ROGUE §6 | After calibration |
| D-009 | 2026-11-02 | No generative AI in the MVP. Later it may only rephrase decided findings, labeled as rephrased | Accepted | Directive; trust differentiator; R-16 | COMPETITIVE_LANDSCAPE §4 | Post-beta |
| D-010 | 2026-11-02 | **Beta is free, with no ads and no billing** | Accepted | Blizzard §2B (as quoted) prohibits paid features using API data; WCL commercial use needs approval | `BNET-16`,`WCL-08` | Legal review of the current terms |
| D-011 | 2026-11-02 | "WoW Ascend" is a working name only; pick a public name without "WoW"/"Warcraft" before launch | Proposed | Trademark risk | `BNET-20` | Stage 0 |
| D-012 | 2026-11-02 | Public and unlisted WCL reports only in the MVP; private reports (WCL user OAuth) after the MVP | Accepted | Scope; user API scope unknown | `WCL-03` | Beta feedback |
| D-013 | 2026-11-02 | Analyze only reports containing one of the signed-in user's own characters | Accepted | Privacy; WCL display restriction (W3) | `WCL-09` | – |
| D-014 | 2026-11-02 | Reference game data (spells, CDs, seasons, patches, rules) is versioned files in the repo, not DB tables | Accepted | Reviewability; avoids speculative tables | DATA_MODEL §1 | If non-developers need to edit it |
| D-015 | 2026-11-02 | PostgreSQL 17 on Neon; Python 3.14; FastAPI; SQLAlchemy 2.1/Alembic; React 19.3; TS 7.0 (fallback 6.x) | Accepted | Versions checked 2026-11-02 | `COST-10` | At Stage 1 scaffold |
| D-016 | 2026-11-02 | Display Blizzard's M+ rating; never compute our own | Accepted | Formula unverified; Blizzard's value is authoritative | `WOW-09`,`BNET-10` | – |
| D-017 | 2026-11-02 | Rule priority ranks: AR-01 = 10, AR-03/04 = 20, AR-10 = 30, AR-09 = 40, AR-14 = 50 | Proposed | Major-cooldown usage is the guides' top cooldown advice. Bleed uptime is the core of the spec. Deaths are facts only in the MVP. Low ranks come first | ROG sources | After calibration |
