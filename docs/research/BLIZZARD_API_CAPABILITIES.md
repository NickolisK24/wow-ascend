# Blizzard Battle.net API — Capabilities for WoW Ascend

**Research date:** 2026-11-02 · **Status:** Baseline v1 — **documentary research only; NO live test performed**

> **Evidence basis.** `develop.battle.net`, `blizzard.com` and the Blizzard forums could not be reached from the research sandbox (network policy), and no Battle.net client credentials were available. Evidence is (a) search-result excerpts of Blizzard pages and forum posts, and (b) **source code of maintained open-source SDKs read directly from GitHub**, chiefly `Pewtro/blizzard-api` (the `@blizzard-api/*` npm packages, updated for Midnight; `BNET-02`). SDK types are hand-written by third parties, not Blizzard's schema. **Every field below is "documented by a third-party SDK, not confirmed against a live response"** until the probe in [`research/proofs-of-concept/blizzard_api_probe.py`](../../research/proofs-of-concept/blizzard_api_probe.py) is run. Status labels reflect documentation evidence only.

## 1. Documentation and platform

| Item | Finding | Conf | Src |
|---|---|---|---|
| Doc portal | develop.battle.net still referenced; a `community.developer.battle.net/documentation/...` alias also appears in search. Redirect relationship UNVERIFIED. | Med | `BNET-04` |
| **Token transport** | Since **2024-09-30**, api.blizzard.com **rejects access tokens in the query string**; use `Authorization: Bearer`. | High | `BNET-01` |
| Gateway IPs | May change; never allow-list by IP. | High | `BNET-01` |
| Namespace | `Battlenet-Namespace: {static|dynamic|profile}-{region}` header (current SDK). Legacy `?namespace=` query form: UNKNOWN (probe tests both). | High / UNKNOWN | `BNET-02` |
| API hosts | `https://{us,eu,kr,tw}.api.blizzard.com`; China `gateway.battlenet.com.cn` (out of scope). | High | `BNET-02` |
| OAuth host | `https://oauth.battle.net` (`/authorize`, `/token`, `/oauth/userinfo`); token check `https://{region}.battle.net/oauth/check_token`. | High / Med-High | `BNET-02`, `BNET-05` |
| Developer account | 2FA required; must accept Developer API Terms. | Med | `BNET-04` |
| 2025–26 deprecations | None found beyond the 2024 header change. | Low (gap) | – |

## 2. Authentication (OAuth 2.0)

| Topic | Finding | Conf | Src |
|---|---|---|---|
| Client credentials | `POST oauth.battle.net/token`, `grant_type=client_credentials`, HTTP Basic. Sufficient for **Game Data** and **public character Profile** endpoints. | High | `BNET-02`,`BNET-03` |
| Authorization code | `/authorize` → `/token`; scopes `openid`, `wow.profile`. Needed for **account character list** and protected-character endpoints. | High | `BNET-02`,`BNET-22` |
| Identity (userinfo) | `id` (numeric), `battletag`, `sub`. **No email.** Use Bearer header (query → 403/500 reports). | Med | `BNET-05`,`BNET-06` |
| **PKCE** | **UNKNOWN.** Only an auto-generated third-party OpenAPI file claims support. → Use a **confidential server-side client** (secret on backend). Probe sends `code_challenge` to test tolerance. | Low | `BNET-19` |
| Token lifetime | ~24 h (forum statement). | Med | `BNET-07` |
| **Refresh tokens** | **Historically not issued**; Blizzard staff: "refresh tokens are not available." | Med | `BNET-07` |
| Revocation / disconnect / redirect URI rules | **UNVERIFIED** — no source found. | – | – |
| Region behavior | One OAuth host for US/EU/KR/TW; API host is per region; a character must be fetched from its own region. | High/Med | `BNET-02` |

**Design consequences.**
1. **User tokens are used once, at login**, to establish identity (`sub`/`id`, BattleTag) and to list the account's characters. They are **not stored** after the character list is retrieved (no refresh token ⇒ no long-lived value; storing it only adds risk).
2. All later character refreshes use the **app's client-credentials token** against public profile endpoints. This works only for characters whose profile is publicly visible; if a character returns 404, Ascend shows "Blizzard isn't sharing this character's data" (see §5 issues).
3. Session security is Ascend's own (HttpOnly session cookie), independent of Blizzard token expiry.
4. "Disconnect Battle.net" = delete Ascend account data; there is no evidence of a Blizzard-side revoke endpoint to call. The user can revoke app authorization in their Battle.net account settings (location UNVERIFIED).

## 3. Character data (Profile API, namespace `profile-{region}`)

Paths verified as present in maintained SDK code (High); fields per SDK types (Medium).

| Data | Endpoint | Auth | Fields (SDK-documented) | Freshness / issues | Ascend use | Status |
|---|---|---|---|---|---|---|
| Account character list | `/profile/user/wow` | user `wow.profile` | character list (fields not extracted) | – | Character picker | **SUPPORTED** (fields UNVERIFIED) |
| Protected character | `/profile/user/wow/protected-character/{realmId}-{characterId}` | user | not extracted | – | Not needed MVP | SUPPORTED |
| Name, region, realm, class, race, faction, level, avg/equipped ilvl, active spec, last login | `/profile/wow/character/{realmSlug}/{name}` | client creds | `id, name, level, average_item_level, equipped_item_level, active_spec, character_class, race, faction, realm, guild?, last_login_timestamp, …` | Updates on **logout**; lowercase slug/name; 404 for long-inactive, renamed, or privacy-restricted characters | Dashboard header | **SUPPORTED** |
| Validity | `…/status` | client creds | `id, is_valid` | **Required for 30-day retention rule** (§6) | Retention job | **SUPPORTED** |
| Equipment, item level, enchants, gems | `…/equipment` | client creds | `equipped_items[]: slot, item, level{value}, quality, bonus_list, context, enchantments[]{display_string, enchantment_id, enchantment_slot, source_item}, sockets[]{socket_type, item, display_string}, stats, set` | Item level is `level.value` (no `item_level` field) | Gear panel; missing-enchant/gem facts | **SUPPORTED** |
| Specialization, talents, **hero talents** | `…/specializations` | client creds | `active_specialization, active_hero_talent_tree, specializations[]{loadouts[]{is_active, talent_loadout_code, selected_class_talents, selected_spec_talents, selected_hero_talents, …}}` | Talents unsorted; unreachable nodes omitted; reflects **current** loadout only | Display only; analysis uses the **log's** talents | **SUPPORTED** (hero: Med-High) |
| Mythic+ rating | `…/mythic-keystone-profile` + `/season/{id}` | client creds | `current_period, seasons`; season: `mythic_rating{rating,color}, best_runs[]{completed_timestamp, dungeon, duration, is_completed_within_time, keystone_level, keystone_affixes, members[], mythic_rating}` | `current_mythic_rating` ≠ sum of run ratings | M+ overview, goal progress | **SUPPORTED** |
| Seasonal best runs | as above | client creds | `best_runs[]` | Overtime runs listed separately? UNVERIFIED | Progress | **SUPPORTED** |
| **Full M+ run history** | – | – | Only season bests are exposed; full history exists only in-game (`C_MythicPlus.GetRunHistory`, addon-only; `BNET-11`) | – | Would power "runs this week" | **UNSUPPORTED** |
| Statistics, media, achievements, encounters, professions, etc. | `…/statistics`, `…/character-media`, … | client creds | not extracted | – | Avatar (media) only | SUPPORTED (paths) |

Missing values: `guild` optional; characters below some level threshold or inactive since 8.2 may 404 (level threshold UNVERIFIED); new document types require a fresh logout (`BNET-08`, `BNET-09`).

## 4. Game data (namespace `static`/`dynamic`)

| Data | Endpoint | Status | Notes |
|---|---|---|---|
| M+ dungeons | `/data/wow/mythic-keystone/dungeon/index`, `/{id}` (`keystone_upgrades`, `is_tracked`) | **SUPPORTED** | Season pool via season/period data |
| M+ periods (weeks) | `/data/wow/mythic-keystone/period/{id}` | SUPPORTED | **No affix list on periods** |
| M+ seasons | `/data/wow/mythic-keystone/season/{id}` (`start/end_timestamp, periods, season_name`) | SUPPORTED | Season boundaries for versioning |
| Weekly affixes | `/data/wow/keystone-affix/*` gives names/descriptions only; current week's affixes inferable from leaderboard `keystone_affixes{starting_level}` (inference) | **PARTIAL** | `BNET-12` |
| M+ leaderboards | `/data/wow/connected-realm/{id}/mythic-leaderboard/{dungeonId}/period/{periodId}` | SUPPORTED | `leading_groups` may be missing |
| Items / item media | `/data/wow/item/{id}`, `/media/item/{id}` | SUPPORTED | |
| Spells / spell media | `/data/wow/spell/{id}`, `/media/spell/{id}` | SUPPORTED | Name/description/icon; **does not reliably give cooldowns** (UNVERIFIED) — cooldowns for rules must come from verified game data or log observation |
| Talents | `/data/wow/talent-tree/*`, `/talent/{id}` | SUPPORTED | Index has regressed before; hero names null in some locales |
| Specializations | `/data/wow/playable-specialization/{id}` (259 = Assassination per long-standing ID, verify) | SUPPORTED | |
| Journal instances/encounters | `/data/wow/journal-instance/*`, `/journal-encounter/*` | SUPPORTED | Boss names; **no mechanic data suitable for coaching** |

**Requires alternative sources:** spell cooldowns/rules interactions, avoidable-ability lists, encounter mechanics, enemy forces counts. Options: Warcraft Logs game data, community data (Wowhead/wago.tools DB2 exports — licensing UNVERIFIED), or manual curation with citations. MVP avoids needing any of these except a small, manually verified spell table for Assassination.

## 5. Rate limits and errors
- **36,000 requests/hour and 100 requests/second per client** — long-cited, secondary sources only (Med, `BNET-13`).
- HTTP **429** when throttled; forum reports of 429s at ~5 rps due to per-node throttles (Med, `BNET-14`). `Retry-After` header UNVERIFIED → bounded exponential backoff with jitter.
- Expected Ascend load: ~5 profile calls per character refresh. 500 active users × 2 characters × 1 refresh/day ≈ 5,000 calls/day — **far below** quota.

## 6. Terms of use (summarized; full text NOT read — see compliance doc)
| Topic | Finding | Conf | Src |
|---|---|---|---|
| **Monetization** | Section 2B (forum quotes): may not charge for "Premium" versions with for-pay features using the APIs; may not require payment for access where features use the APIs; may not use APIs/data to market products; may not sell/license data. | **Med — HIGH RISK** | `BNET-16` |
| **Retention** | Check `/status` at least every **30 days**; delete stored character data on 404, `is_valid=false`, or changed `id`. Keeping invalid data can lose API access. | Med-High | `BNET-17` |
| On stopping use | Delete held data. | High (excerpt) | `BNET-15` |
| Attribution | Credit Blizzard as data source (third-party summary only). | Low-Med | – |
| Trademark | No policy found permitting "WoW" in a product name; Blizzard enforces IP. **"WoW Ascend" name is a legal risk.** | – | `BNET-20` |

## 7. Capability matrix (documentary)

| Capability | Status |
|---|---|
| Battle.net login (auth code, server-side) | SUPPORTED |
| PKCE | UNKNOWN |
| Refresh tokens | UNSUPPORTED (historical) — re-verify |
| BattleTag / account ID | SUPPORTED |
| Email | UNSUPPORTED |
| Account character discovery | SUPPORTED |
| Character name/realm/region/class/spec/level | SUPPORTED |
| Equipped items + item level | SUPPORTED |
| Enchantments / gems | SUPPORTED |
| Talents (class/spec) | SUPPORTED |
| Hero talents | SUPPORTED (Med-High) |
| Current M+ rating | SUPPORTED |
| Season best runs per dungeon | SUPPORTED |
| Full M+ run history | UNSUPPORTED |
| Weekly affixes (direct) | PARTIAL |
| Character statistics | SUPPORTED (fields unknown) |
| Spell definitions (name/icon) | SUPPORTED |
| Spell cooldowns/mechanics | UNKNOWN (assume UNSUPPORTED) |
| Dungeon/season metadata | SUPPORTED |
| Encounter mechanics | UNSUPPORTED |
| Revocation endpoint | UNKNOWN |

## 8. Feasibility tests still required (see [FEASIBILITY_TEST_PLAN.md](../quality/FEASIBILITY_TEST_PLAN.md) T-BN-*)
Live token; character lookup + equipment + specializations + keystone profile for a Midnight Assassination Rogue; 404 and 401 handling; `?namespace=` legacy; PKCE; refresh token issuance; account character list fields; rate-limit headers; overtime runs in `best_runs`; current Terms text (legal read).
