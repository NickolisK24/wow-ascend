# Security, Data and Provider Compliance Policy

**Research date:** 2026-11-02 · **Status:** Baseline v1. **Not legal advice.** No terms document was read in full: the provider legal pages were unreachable from the research sandbox, so every term below comes from quotes in forums or GitHub issues, or from search summaries. **Every item marked OPEN must be resolved by reading the current primary text, and where noted, by written confirmation from the provider, before public launch.**

## 1. Provider obligations

### 1.1 Blizzard Developer API Terms of Use (`BNET-15`, not read)
| # | Obligation / restriction | Evidence | Status | Ascend response |
|---|---|---|---|---|
| B1 | **No charging for "Premium" for-pay features that use the APIs. No requiring payment for access when features use the APIs** (Section 2B, as quoted) | Forum quotes (`BNET-16`), Medium | **OPEN — HIGH IMPACT** | MVP and beta are **free, with no ads and no paid tier** (D-010). Monetization is deferred until legal review of the current text. |
| B2 | No using API data to market your own or third-party products. No selling, licensing or transferring data | `BNET-16` | OPEN | No data resale, no affiliate marketing using character data |
| B3 | Check character `/status` **at least every 30 days**. Delete stored data on a 404, `is_valid=false`, or a changed id | Data Protection Notice/FAQ (`BNET-17`), Med-High | OPEN (current text) | Nightly retention job (§3) |
| B4 | Delete held data when you stop using the API | Excerpt (`BNET-15`) | OPEN | Runbook: shutdown deletion |
| B5 | Attribution to Blizzard as the data source | Third-party summary only | OPEN | Footer: "Character data from the Blizzard Battle.net API. WoW Ascend is not affiliated with or endorsed by Blizzard Entertainment." |
| B6 | Developer account needs 2FA; the terms must be accepted | `BNET-04` | Known | Project-owned developer account with 2FA |
| B7 | **Trademark use: "WoW" in the product name** | No permission found; Blizzard enforces its IP (`BNET-20`) | **OPEN — rename likely** | Treat "WoW Ascend" as a working name only. Choose a public name without "WoW"/"Warcraft" before any public launch (D-011). |
| B8 | Rate limits (36k/h, 100/s) | Secondary (`BNET-13`) | Known-ish | Client-side limiter (see architecture) |

### 1.2 Warcraft Logs / Archon API Terms (`WCL-07`, not read)
| # | Obligation / restriction | Evidence | Status | Ascend response |
|---|---|---|---|---|
| W1 | **Commercial use (earning money, including advertising) needs prior approval by email** | `WCL-08` (Med-Low) | **OPEN** | Email support@rpglogs.com (address per `WCL-08`; verify) before the beta, describing the use case. Gate 3 blocker. |
| W2 | **No keeping cached copies longer than the cache header allows**; `Cache-Control: no-cache, private` was observed | `WCL-09` (Med) | **OPEN — HIGH IMPACT** | Never persist raw events (D-006). Derived-metric storage is to be confirmed in writing. |
| W3 | No public display to third parties unless the content owner permits it | `WCL-09` | OPEN | Findings are private to the importing user. No sharing feature in the MVP. |
| W4 | No building a client "substantially the same as the APIs" | Med-Low | OPEN | Ascend exposes no WCL data API |
| W5 | **Commercial access tier** (price not announced) under the new rate-limit system | `WCL-05` (Med) | OPEN | Budget: unknown. Re-check when the beta ends (Nov 2026+). |
| W6 | Privacy policy required | Low | OPEN | Publish one regardless (§5) |
| W7 | Unlisted-report codes must not leak between users | Schema guidance (`WCL-01`, High) | Known | Imports are scoped per user. Never show a report to a user who didn't import it themselves. |

### 1.3 Other providers
- **Raider.IO API:** terms UNVERIFIED. Not used in the MVP.
- **Hosting / email / monitoring:** standard SaaS terms. **Vercel Hobby forbids commercial use** (H, `COST-01`), which is one reason the frontend is hosted on Cloudflare Pages (see cost model).
- **Anthropic API** (optional, post-MVP): standard commercial terms; never sends account identifiers.

## 2. Data classification

| Class | Examples | Sensitivity | Stored? | Protection |
|---|---|---|---|---|
| **Identity** | Battle.net account id (`sub`), BattleTag | **High (PII)** | Yes | Encrypted at rest (provider). BattleTag shown only to its owner. Hashed id used in logs. |
| **Session** | Ascend session token | **High** | Server-side hash only | HttpOnly, Secure, SameSite=Lax cookie. Rotated on login. 14-day idle expiry. |
| **Provider tokens** | Battle.net user access token; WCL user token | **Critical** | **Battle.net: never persisted** (used at login, then discarded). WCL user token: in memory for the import request only in the MVP; if stored later, encrypted with an app key (AES-GCM) and scoped per user | Never logged |
| **App credentials** | Blizzard / WCL client secrets, DB URL, session key | **Critical** | Host environment secrets only | Never in git (`.gitignore`, secret scanning). Rotated on suspicion. |
| **Public character data** | Name, realm, class, gear, rating | Medium (public, but tied to an identity) | Yes, with a 30-day validity check | Owner-scoped access |
| **Private report data** | Events from private or unlisted WCL reports | **High** (third-party content) | **Raw: never.** Derived: pending W2 | Owner-scoped. Purged when the user deletes it. |
| **Derived findings** | Metrics, findings, evidence references | Medium | Yes (pending W2) | Owner-scoped |
| **User-entered** | Goals, notes | Low-Medium | Yes | Owner-scoped |

## 3. Retention and deletion
| Data | Retention | Trigger for deletion |
|---|---|---|
| Character snapshots | Latest snapshot plus history while the character is valid | `/status` check every ≤30 days fails (404, `is_valid=false`, id mismatch) → delete the character and its snapshots (B3) |
| Imported analyses (derived) | Until the user deletes them, or the account is deleted. **Default cap: 180 days** (pending W2) | User action; account deletion; W2 outcome |
| Raw provider responses | **0 days** (memory only) | – |
| Application logs | 30 days | Rolling |
| Error monitoring events | Per provider (Sentry free tier: 14–30 days) | Rolling. PII scrubbing on. |
| Backups | Per DB provider (7 days typical) | Rolling. Deletion requests take effect in backups as they expire; this is disclosed. |
| Account | Until the user deletes it | "Delete my account" removes all rows owned by the user in one transaction. Confirmation shown. Target: under 1 minute. |

## 4. Security controls (MVP)
1. **OAuth:** server-side authorization-code flow (confidential client). `state` is random, bound to the pre-auth session, and single-use. PKCE is added if supported. The redirect URI is exact-match and HTTPS-only in production.
2. **Never request Battle.net passwords**, and never embed Blizzard login in an iframe.
3. **Sessions:** opaque random token (≥256 bits). Only its SHA-256 is stored. Cookie flags: HttpOnly, Secure, SameSite=Lax. CSRF protection: SameSite plus an `Origin` check on state-changing requests.
4. **Authorization:** every query is filtered by `user_id` at the repository layer. Tests assert that one user cannot read another user's analyses (IDOR tests).
5. **Input validation:** a WCL report URL must match `^https://(www\.)?warcraftlogs\.com/reports/[A-Za-z0-9]{16}` (code length to be verified with the probe). Anything else is rejected before any network call. Ascend never fetches arbitrary URLs (SSRF prevention).
6. **Secrets:** environment variables on the host. A `.env.example` holds names only. Pre-commit secret scanning (gitleaks or similar, chosen in Stage 1).
7. **Logging:** structured JSON logs. Tokens, cookies, BattleTags and character names are redacted; a hashed user id is used.
8. **Dependencies:** pinned lockfiles; automated update PRs; `pip-audit` / `npm audit` in CI.
9. **Transport:** HTTPS only, HSTS.
10. **Rate limiting:** per-user import limit (e.g., 20 imports/day) to protect the WCL budget.
11. **Security review** at Stage 5 (OWASP ASVS L1 checklist subset).

## 5. Privacy disclosures (to publish before beta)
A plain-language privacy page covering: what is collected (above table); why; providers involved (Blizzard, Warcraft Logs, hosting, email, monitoring); retention; deletion; no sale of data; no advertising; contact address; the "not affiliated with Blizzard" statement. GDPR/UK-GDPR applies to EU/UK users: lawful basis is contract/consent; data-subject rights are fulfilled through self-service deletion plus an email contact. CCPA thresholds are almost certainly not met at beta scale, but the same rights are honored. **Formal legal review is recommended before any commercial launch** (OPEN).

## 6. Prohibited practices
Scraping provider websites; using a user's WCL session or cookies; bypassing private-report permissions; addon-based data collection that circumvents secret values; memory reading; any in-combat assistance; storing raw provider responses in production; sharing a user's findings publicly without explicit opt-in; selling data.

## 7. Open compliance items (Gate 3 blockers)
1. Read the current Blizzard Developer API Terms in full, especially §2B (monetization), retention, attribution and trademark. **Owner:** project lead.
2. Read the current RPG Logs API Terms. Email for written approval of the use case, and ask explicitly whether storing derived metrics is permitted.
3. Name/trademark check for the public product name; pick a name without "WoW".
4. Draft the privacy policy and terms of service (template plus review).
