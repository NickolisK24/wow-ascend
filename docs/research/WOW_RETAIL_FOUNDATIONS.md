# World of Warcraft Retail — Foundations for Engineers

**Research date:** 2026-11-02 · **Status:** Baseline v1 · **Owner:** project lead

> **Evidence caveat (applies to the whole document).** The research sandbox's network policy blocked direct page reads of Blizzard, Wowhead, Icy Veins, Warcraft Wiki and Warcraft Logs. Every time-sensitive claim below comes from **web-search result summaries** of those pages, not from reading them. Source IDs (e.g. `WOW-03`) resolve in [`../SOURCE_REGISTER.md`](../SOURCE_REGISTER.md). Concepts marked **[GK]** are stable, long-standing game concepts described from general knowledge; they were *not* re-verified this session and must not be used as data definitions without confirming against an API response or current source.

Confidence: **High** = multiple consistent sources incl. official/major outlets · **Medium** = one reputable source or mostly consistent · **Low** = conflicting/unclear · **UNVERIFIED** = no evidence found.

---

## 1. Game fundamentals

### 1.1 Retail vs Classic
WoW has two product lines: **Retail** (the current expansion, continuously patched) and **Classic** (historical re-releases with separate game versions and API namespaces). WoW Ascend targets **Retail only**. [GK] — Blizzard's API uses distinct namespaces for Classic, so Classic data must never be mixed in (see [BLIZZARD_API_CAPABILITIES.md](BLIZZARD_API_CAPABILITIES.md)).

### 1.2 Accounts, regions, realms
| Concept | Engineering meaning | Status |
|---|---|---|
| **Battle.net account** | The person's login identity (BattleTag). Owns one or more WoW game accounts. | [GK] |
| **Region** | US (incl. Oceania/LatAm), EU, KR, TW, CN. Separate API hosts; **CN is operated separately** and is out of scope. | [GK], UNVERIFIED this session |
| **Realm** | Game server a character belongs to. Identified in APIs by a *slug* (e.g. lowercase-hyphenated). | [GK] |
| **Connected realm** | Group of realms sharing infrastructure; leaderboards are keyed by connected realm. | [GK] |
| **Character** | Unique by `(region, realm slug, name)`. Names/realms change via paid services — **natural keys are not stable**; prefer provider IDs. | [GK] |

### 1.3 Classes, specializations, roles
- 13 classes; each has 2–4 **specializations** ("specs"). Midnight added a new spec, **Devourer Demon Hunter** (ranged Intellect DPS), bringing the total to **40 specs** (High, `WOW-12`).
- Each spec has one **role**: tank, healer or damage dealer (DPS). [GK]
- **Assassination** is one of three Rogue specs (melee, Agility, damage dealer). Spec detail: [ASSASSINATION_ROGUE.md](ASSASSINATION_ROGUE.md).

### 1.4 Level and item level
- **Level cap is 90** in Midnight (High, `WOW-01`, `WOW-11`). At cap, character power is driven by **item level (ilvl)**, the numeric power rating of each equipped item; "character item level" is an average across slots. [GK]
- Season 2 upgrade tracks (Medium, `WOW-08`; datamined chart, 12.1.5):

| Track | ilvl range |
|---|---|
| Adventurer | 266–282 |
| Veteran | 279–295 |
| Champion | 292–308 |
| Hero | 305–321 |
| Myth | 318–334 |

Max ilvl 344 on rare items/last Mythic bosses (Medium). Blizzard raised the season's item-level jump from 39 to 46 on 2026-07-08, so **older charts are wrong** (Medium, `WOW-08`).

### 1.5 Attributes and equipment
- **Primary stats** (Strength/Agility/Intellect, Stamina) — a spec uses one main stat. [GK]
- **Secondary stats:** Critical Strike, Haste, Mastery, Versatility, with diminishing returns — confirmed still in use by Midnight stat guides (High, `WOW-13`). Exact rating-per-percent conversions: UNVERIFIED; not needed for MVP.
- **Tertiary stats** (Leech, Avoidance, Speed): UNVERIFIED this session.
- **Equipment slots:** ~16 slots (head, neck, shoulder, back, chest, wrist, hands, waist, legs, feet, 2 rings, 2 trinkets, main/off hand). [GK] Items may carry **enchantments** and **gem sockets**. Exact slot list must be taken from the Blizzard equipment response, not this list.

### 1.6 Talents
- Talents are chosen in **class tree + spec tree** plus a **hero talent tree** (one of two per spec; unlocks at level 71). Midnight added a **4th hero row** and **Apex talents** — 4-point spec capstones from level 81 (High for existence, Medium for unlock schedule — sources conflict, `WOW-11`, `WOW-12`).
- Players save **loadouts** and switch them freely out of combat. **Engineering implication:** a talent snapshot from the Blizzard API reflects the *current* loadout, which may differ from what was used in a given log. The authoritative talent build for a run is the one recorded in the combat log (`combatantinfo`) — see [WARCRAFT_LOGS_FEASIBILITY.md](WARCRAFT_LOGS_FEASIBILITY.md).

### 1.7 Combat model [GK]
| Concept | Meaning | Why Ascend cares |
|---|---|---|
| Ability / spell | An action with an ID, cast time, cost, cooldown. | Spell IDs are the join key between logs and game data. Spell IDs change between patches. |
| **Global cooldown (GCD)** | Short lockout after most abilities (nominally ~1.5 s, reduced by haste; Rogues historically 1.0 s). **UNVERIFIED for Midnight.** | Bounds how many actions are possible; "downtime" analysis depends on it. |
| Cooldown (CD) | Time before an ability can be reused. | "Did the player use their major CDs?" analysis. |
| Resource | Energy, mana, rage, combo points, etc. | Over-capping/waste analysis. |
| Buff / debuff | Timed effect on a unit (beneficial / harmful). | Uptime analysis. |
| **DoT** (damage over time) | Debuff that deals periodic damage. | Assassination's core; uptime/refresh analysis. |
| AoE | Hits multiple targets. | M+ trash is AoE-heavy; single-target heuristics mislead on trash. |
| Interrupt | Stops an enemy cast; has a cooldown. | Group contribution; key M+ skill. |
| Crowd control (CC) | Stuns, incapacitates, slows. | Utility, hard to judge from logs alone. |
| Defensive | Reduces damage taken. | Survival analysis around deaths. |

### 1.8 What determines combat performance
Performance = **character power** (gear, ilvl, talents) × **player decisions** (ability choice, timing, target choice, positioning, mechanic avoidance) × **encounter context** (enemy count, mechanics forcing movement or untargetability, group composition, route). A log records *outcomes and actions*, not *intent or circumstances*. **Any coaching claim must isolate player decisions from context; where it cannot, it must say so.** This principle drives the analysis-engine design ([ANALYSIS_ENGINE.md](../architecture/ANALYSIS_ENGINE.md)).

---

## 2. Mythic+ fundamentals

### 2.1 Structure
- A **Mythic+ (M+)** run is a 5-player dungeon (1 tank, 1 healer, 3 DPS) started with a **keystone** item of a given **level** (+2 and up). Higher levels scale enemy health/damage and add **affixes**. [GK + Medium current]
- Goal: kill all bosses and a required percentage of **enemy forces** (trash) before the **timer** expires. Finishing in time ("timing" the key) upgrades the keystone; finishing late completes but depletes/downgrades it. [GK]
- **Route**: which trash packs a group pulls, in what order — planned with tools like Keystone.guru.
- **Deaths** cost time at higher levels (see affixes). [GK + High for +12 rule]

### 2.2 Current affixes (Midnight Season 2) — Medium overall (`WOW-05`, `WOW-06`)
| Key level | Affix | Effect (summarized) | Confidence |
|---|---|---|---|
| +2 to ~+5 | **Lindormi's Guidance** (new in S2) | Marked enemies have 5% less health/deal 5% less damage; **deaths cost no time**. Window edge (+4 vs +5) conflicts. | Medium/Low edges |
| Higher | Lindormi's Glow | Route highlighting only | Medium |
| +5 to +11 | **Xal'atath's Bargain** (rotating weekly: Devour, Pulsar, Ascendant, Voidbound) | Moved from +4 to +5 in 12.0.1 | Medium |
| +7 | Fortified **or** Tyrannical (alternating weekly) | Trash-heavy vs boss-heavy difficulty. One source says they remain at +2 — **unresolved conflict** | Medium/Low |
| +10 | Fortified **and** Tyrannical | | Medium |
| +12 | **Xal'atath's Guile** replaces Bargain | **Each death removes 15 s** from the timer (until last minute) | High |

- Death penalty for roughly +6 to +11: **UNVERIFIED** (sources say "normal penalty" without a number).
- **Resilient Keystones**: timing all 8 dungeons at +12 or higher prevents keys depleting below 12, scaling upward (Medium-High, `WOW-07`).
- **Implication for Ascend:** affixes and penalties are season data, not code. They must live in versioned season metadata (see [DATA_MODEL.md](../architecture/DATA_MODEL.md)).

### 2.3 Mythic+ rating
- Score derived from the **best run per dungeon**; higher level and faster completion give more. **Exact formula: UNVERIFIED** (`WOW-09`). Ascend must **display the provider's rating, never compute its own.**
- Season 2 thresholds (Medium, `WOW-09`): 1,500 Keystone Conqueror; 2,000 Keystone Master; 2,500 Keystone Hero; 3,000 Keystone Legend; 3,400 Keystone Myth. Mythic Saga threshold UNVERIFIED.

### 2.4 Rewards (Season 2, Medium, `WOW-10`)
- +10 end-of-dungeon loot: Hero 3/6 (ilvl 311); Great Vault from +10: Myth 1/6 (318). Higher keys do not raise vault reward.
- **Great Vault** M+ slots unlock at 1, 4, 8 completed runs per week.
- Dungeon **teleports** unlock by timing that dungeon at +10 or higher (Medium).

### 2.5 Group skills Ascend might coach [GK]
Interrupt assignments, CC on dangerous casts, defensive usage on predictable damage, avoiding avoidable damage, staying alive (deaths are the most expensive mistake at +12 and up). Which of these are *measurable* is the subject of [WARCRAFT_LOGS_FEASIBILITY.md](WARCRAFT_LOGS_FEASIBILITY.md).

---

## 3. Current Retail environment (as of 2026-11-02)

| Item | Finding | Confidence | Sources |
|---|---|---|---|
| Live expansion | **Midnight** (launched 2026-03-02) | High | `WOW-01` |
| Live patch | **12.1.5** (NA 2026-10-13, EU 10-14) | High | `WOW-02` |
| Patch family | 12.1 "Curse of Ula'tek" (NA 2026-08-11) | High | `WOW-03` |
| Build | Possibly 69848 (from a test-build record) | **Low** | `WOW-04` |
| Earlier patches | 12.0.5 (~2026-04-21), 12.0.7 (~2026-06-16) | Medium | `WOW-14` |
| PTR | 12.1.7 "Echoes of the Worldcore" on PTR since 2026-10-15; release ~Dec 2026 (guess) | High PTR / Low date | `WOW-15` |
| Next major | 12.2 "Eclipse" + **Season 3**, announced BlizzCon 2026-09-12 for "Winter" 2026–27, no date | High/Low date | `WOW-16` |
| Current season | **Midnight Season 2**, started NA 2026-08-18; end not announced (expected at 12.2) | High / Low end | `WOW-03` |
| Raid | The Venomous Abyss (8 bosses) | High | `WOW-03` |
| **M+ dungeon pool (8)** | Altar of Fangs, Murder Row, Den of Nalorakk, The Blinding Vale, Voidscar Arena, King's Rest, Temple of Sethraliss, Ruby Life Pools | High | `WOW-05` |
| Dungeon timers | 28–34 min, sources conflict | Low | `WOW-05` |
| Season 3 changes (announced) | Top 1%/5% M+ rewards become **per-specialization**; new pool incl. Thraegar's Stand, Magisters' Terrace, Maisara Caverns, The Underrot, Iron Docks, Sanguine Depths, The Stonecore, Uldaman: Legacy of Tyr | Medium | `WOW-17` |

**Season-transition risk:** Season 3 (12.2) likely lands within 2–4 months of this baseline, i.e. **during or just after the planned beta**. The whole dungeon pool changes. Ascend's design must treat dungeon/season data as replaceable configuration (see [RISK_REGISTER.md](../planning/RISK_REGISTER.md) R-07).

### 3.1 Midnight combat & addon restrictions ("addon disarmament")
Blizzard article *"Combat Philosophy and Addon Disarmament in Midnight"* (`WOW-18`; exact publication date UNVERIFIED, late 2025). Principle: addons should no longer provide a competitive combat advantage; visual customization remains.

| Surface | Finding | Confidence | Sources |
|---|---|---|---|
| **Secret values** | Combat-state APIs return opaque values addons can pass to Blizzard UI widgets but cannot read/compute on | High | `WOW-19` |
| `COMBAT_LOG_EVENT_UNFILTERED` for addons | Inaccessible to addons since 12.0.0; scope (only in boss encounters/M+ vs everywhere) **conflicts** | High (restricted) / Medium (scope) | `WOW-19`, `WOW-20` |
| Exceptions | Player's own spellcasts not secret; secondary resources (combo points etc.) not secret; primary resources are | Medium | `WOW-19` |
| 12.1 | New aura-filtering API, reduced aura info leak (framed as tightening by one source, relaxation by another) | Medium | `WOW-21` |
| 12.1.5 | Damage-meter `sourceGUID` becomes secret when unit identity is secret | Medium | `WOW-21` |
| Built-in replacements | Server-side **damage meter** (incl. avoidable damage), encounter warnings/timeline, expanded Cooldown Manager | High | `WOW-22` |
| Addons | WeakAuras ended Midnight support; DBM/BigWigs continue in reduced form; rotation helpers/interrupt automation blocked | High | `WOW-22`, `WOW-23` |
| **Combat log file** (`WoWCombatLog.txt`, Advanced Combat Logging) | **Appears unaffected** — restrictions target in-game Lua, not file output; Warcraft Logs uploads continue (Archon app launched with Midnight) | **Medium-High** — secondhand quote of the game director plus WoWAnalyzer 12.1.0 support; no first-hand Blizzard or WCL statement read | `WOW-24`, `WOW-25`, `WCL-10` |

**The five surfaces the directive asks us to separate:**
1. **In-game addon information** — heavily restricted (secret values). Ascend uses **no addon**; this restriction does not directly limit Ascend, but it eliminates addon-based data collection as an option.
2. **Combat events written by the client** — appear to be unaffected (Medium). Needs a real Midnight log to confirm.
3. **Information accepted by Warcraft Logs** — WCL continues to accept Midnight logs (Medium; inferred from Archon launch and continued rankings).
4. **Information exposed through WCL APIs** — see [WARCRAFT_LOGS_FEASIBILITY.md](WARCRAFT_LOGS_FEASIBILITY.md). **Not live-tested.**
5. **Information Ascend may legally process** — governed by WCL and Blizzard terms; see [SECURITY_AND_DATA_POLICY.md](../compliance/SECURITY_AND_DATA_POLICY.md).

**Product implication:** Midnight did not (on current evidence) remove the post-run log as a data source, but it **did** move several things into Blizzard's own UI (damage meter with avoidable damage, death recap-like information). That raises the bar for what a third-party post-run tool must add.

---

## 4. Explicitly unverified (must not be treated as fact)
Exact live build; 12.0.0/12.0.1 dates; 12.1.7 and 12.2 release dates; Season 2 end date; M+ death penalty for +6–+11; exact Lindormi's window and Fortified/Tyrannical start level; dungeon timers; M+ rating formula; Mythic Saga threshold; official per-spec Season 3 reward post; disarmament article date; **first-party confirmation that the advanced combat log is unredacted in Midnight**; tertiary stats; GCD values; region details.

## 5. Re-verification triggers
Re-run this research when: a new patch (x.y.z) goes live; Season 3 starts; Blizzard publishes addon/combat-log policy changes; WCL announces logging changes. Owner: project lead. Record outcome in [DECISION_LOG.md](../planning/DECISION_LOG.md).
