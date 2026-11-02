# Cost Model

**Date:** 2026-11-02 · **Status:** Baseline v1

> **Pricing evidence.** Vendor pricing pages were not reachable from the sandbox. Prices come from 2026 third-party pricing summaries found through web search (`COST-01..09, 11, 12`), except Fly.io (official docs via search). **Verify every price on the vendor page before you commit money.** "V" = verified by several consistent sources; "A" = assumption, or sources conflict.

## 1. Workload assumptions (all are assumptions, A)

| Parameter | Value | Rationale |
|---|---|---|
| Characters per active user | 2 | Alts are common; only Assassination gets analyzed |
| Imports per active user per month | 6 | ~1.5 analyzed keys a week for an engaged improver |
| Dashboard visits per user per month | 10 | – |
| Character refreshes | ≤1/day/character, on visit only | No background polling, except the 30-day status checks |
| Stored per analysis | ~50 KB (metrics, findings, pull summaries; no events) | JSON estimate |
| Stored per snapshot | ~20 KB; a new snapshot only when data changes | – |
| DB size per user per year | ~4–5 MB | 72 analyses × ~50 KB ≈ 3.6 MB, plus snapshots |
| Analysis job | 10–60 s wall time, mostly waiting on WCL I/O. **Peak memory per job: UNKNOWN**, est. 100–400 MB if events are held in Python objects | Stream per dataType to reduce it. Measure in Stage 3 |
| WCL points per import | **~20 (pure assumption)** | Must be measured (T-WCL-05). "2–6 points per full fight query" observed by one project |
| Peak-hour factor | 4× the average hourly import rate | Evening and weekend play |

## 2. Unit prices used

| Item | Price | Status | Src |
|---|---|---|---|
| Cloudflare Pages (static) | $0 | V | `COST-05` |
| Render web service Starter (512 MB) | $7/mo | V-ish (M) | `COST-02` |
| Render Standard instance | ~$25/mo | A (sources conflict) | `COST-02` |
| Render background worker | from $7/mo | M | `COST-02` |
| Render free Postgres | **expires after 30 days**, unusable | V | `COST-02` |
| Neon Free | $0, ~0.5 GB, scale-to-zero | M | `COST-03` |
| Neon Launch | ~$0.106/CU-h + $0.35/GB-mo (a $5 minimum may apply) | A | `COST-03` |
| Sentry Developer / Team | $0 (5k errors) / ~$26–29/mo | M | `COST-06` |
| Domain .com (Cloudflare Registrar) | ~$11.17/yr | M | `COST-08` |
| Domain .gg | ~$52–83/yr; Cloudflare doesn't sell it | M | `COST-08` |
| Email (Resend) | $0 (3k/mo, 100/day) | V | `COST-07`. **Not needed in the MVP**: Battle.net provides no email, and the MVP sends none |
| WCL API (non-commercial) | Free key (1,000 App points/h); higher limits tied to the key owner's WCL subscription: Gold 3,000, Platinum 9,000 | M (beta system) | `WCL-05` |
| WCL API (commercial tier) | **UNKNOWN, not announced** | – | `WCL-05` |
| WCL subscription | ~$2 / $5 / $10 per month for Silver / Gold / Platinum | **A** | `WCL-17` |
| Claude Haiku 5.5 (optional, post-MVP) | $0.10 / $0.50 per M input/output tokens | M (cached price table, 2026-10-06) | `COST-09` |
| Vercel Pro (if ever needed) | $20/seat/mo | M | `COST-01` |

## 3. Monthly estimates

| Stage | Users | Infra | Monthly cost | Notes |
|---|---|---|---|---|
| **Local development** | 1 | Docker Postgres, fixtures | **$0** | A WoW subscription is needed to generate your own test logs (assumed to be held already) |
| **Private alpha** | ≤20 | Pages + Render Starter + Neon Free + Sentry free + domain | **~$8** ($7 + ~$1 domain) | Free WCL key is enough: about 3 imports/hour at peak, ≈60 points |
| **50 active users** | 50 | Same | **~$8–13** | Neon may cross the free tier, adding ~$0–5. WCL: 300 imports/mo, ≈2 per peak hour, ≈40 points/h |
| **500 active users** | 500 | Render Standard (memory headroom) + Neon Launch + optional Sentry Team | **~$35–65** | 3,000 imports/mo, ≈17 per peak hour, ≈340 points/h: fits the free WCL key if ~20 pts/import holds. Storage ~2–2.5 GB, ≈$1 |
| **5,000 active users** | 5,000 | Render Standard web + Standard worker + Neon Launch (bigger CU) + Sentry Team | **~$115–175 + WCL cost (UNKNOWN)** | 30k imports/mo, ≈170 per peak hour, ≈3,400 points/h: **exceeds the free 1,000/h**. Needs Platinum (9,000) if non-commercial use is allowed, or the commercial tier at an unknown price. Storage ~20–25 GB, ≈$8 |
| Optional AI rephrasing | – | Haiku 5.5, ~1.5k in / 400 out per finding | ≈$0.35 per 1,000 findings; ≈$32/mo at 5,000 users | Post-MVP only |

**Calibration workload** (one-off per season and patch window): roughly 30 reports × 2 hero trees × 8 dungeons ≈ 480 reports per key band (each report covers all bosses of its dungeon). Fetching only the boss pulls, that's an estimated 480–1,000 imports' worth of points, spread over several days on the free key. **Assumption.**

## 4. Development cost
- **Developer time:** 140–190 hours (see [ROADMAP.md](ROADMAP.md)), unpaid solo work. At a notional $50/h, the opportunity cost is $7–9.5k.
- **Cash costs during development:** domain ~$11/yr, plus Render Starter from Stage 1 deploys at $7/mo. **≈ $30 for the beta period.**
- **Not budgeted:** legal review (strongly recommended before any monetization; quote not obtained), trademark search.

## 5. Simplest practical ops design for a solo developer
One Render web service with the in-process job runner, Neon Postgres, Cloudflare Pages, Sentry free, and a free uptime monitor. GitHub Actions CI and auto-deploy on `main`. No Redis, no queue service, no cron service, no email provider. Total about **$8/mo until real load appears**.

## 6. Cost risks
1. **WCL commercial tier price (unknown)** could dominate costs at scale. **Revenue may be legally impossible** under Blizzard §2B (see compliance), so costs must stay inside a hobby budget unless both issues resolve.
2. Memory per analysis job may force the Standard instance earlier than planned.
3. Price conflicts between sources for Render, Neon and Railway. Re-verify before Stage 1 deploy.
