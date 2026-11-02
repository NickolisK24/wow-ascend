# Assassination Rogue — Specialization Study (MVP spec)

**Research date:** 2026-11-02 · **Live patch:** 12.1.5 (tuning baseline effectively **12.1**, 2026-08-11, plus 2026-08-25 hotfix — 12.1.5 had no meaningful Assassination changes per Icy Veins, Maxroll, Method; Medium-High, consistent search digests, `ROG-01..03`) · **Status:** Baseline v1

> **Evidence caveat.** Guide pages (Icy Veins, Maxroll, Method, Wowhead) could not be opened directly; claims come from search-result digests of them. The SimulationCraft `midnight` branch APL (`ROG-05`) was retrieved only as a summarised extract; it is undated and still names War Within trinkets, so it may lag 12.1. **No number in this document may be used as a coaching threshold.** Thresholds must come from the calibration study defined in §6.

## 1. Gameplay identity (for a non-player)

Assassination is a melee damage spec built on **bleeds and poisons**. The loop:
1. **Builders** generate **combo points (CP)** and cost **energy** (a fast-regenerating resource).
2. **Finishers** spend CP: **Rupture** (a bleed DoT) and **Envenom** (direct damage + a buff that boosts poison damage).
3. **Garrote** (a bleed that also builds 1 CP) and **Rupture** must be kept on the priority target.
4. Every ~2 minutes, **Deathmark** amplifies the bleeds/poisons on one target; **Kingsbane** (~1 min) is synced with it.
5. In AoE (common in M+ trash), **Crimson Tempest** spreads bleeds and **Fan of Knives** hits everything.

The spec is "ramp-up" heavy: value comes from bleeds ticking over time, so short-lived targets and target swaps reduce its effectiveness. **This makes naive uptime metrics misleading on M+ trash.**

## 2. Ability status in Midnight (12.1.5)

Status: present / changed / removed / UNVERIFIED. Cooldowns are only listed where sourced.

| Ability | Status | Summary (as sourced) | CD | Coaching relevance | Src / conf |
|---|---|---|---|---|---|
| Energy / combo points | present | Builder/spender. Sanguine Stratagem +1 max CP; Method uses 7-CP Envenom under Darkest Night. **Base max CP UNVERIFIED** | – | CP at finisher cast | `ROG-02`,`ROG-03` Med |
| Mutilate | present | ST builder, 2 CP | – | Builder choice | `ROG-01` High |
| Ambush | present | Builder; Blindside/Improved Ambush | – | Opener | `ROG-05`,`ROG-03` Med-High |
| Fan of Knives | present | AoE builder at 2+ targets | – | AoE execution | `ROG-03` Med |
| **Crimson Tempest** | **changed** | Reworked from finisher/DoT into a **generator that spreads Garrote/Rupture** to nearby enemies; exact spread rule conflicts ("copies longest bleed" vs "2 nearby enemies"). Talent. | UNVERIFIED | AoE bleed spreading | `ROG-01`,`ROG-03`,`ROG-05` Med-High |
| Envenom | present | Main finisher; keeps Envenom buff up; 5+ CP (7 w/ Darkest Night) | – | CP at cast; buff uptime | `ROG-02`,`ROG-03`,`ROG-05` High |
| **Rupture** | present | Finisher bleed; pandemic refresh window scales with CP (Maxroll: ≤7.2 s @5 CP, ≤8.4 s @6 CP); Avulsion +25% in 12.1 | – | **Uptime**, refresh timing | `ROG-02`,`ROG-05`,`ROG-06` High |
| **Garrote** | present | Bleed, 1 CP; Deathstalker opener applies Deathstalker's Mark | UNVERIFIED | **Uptime**, Improved Garrote | `ROG-01`,`ROG-02` High |
| Improved Garrote | present (talent) | Empowered Garrote from stealth/Vanish | – | Vanish→Garrote before Deathmark | `ROG-05`,`ROG-01` Med-High |
| **Deathmark** | present, **changed in 12.1** | Main ~2-min CD; amplifies target's Rupture/Garrote/lethal poisons by 75% (was 100%); no longer duplicates bleeds; restores energy | **2 min** | **Cast count vs opportunities** | `ROG-07`,`ROG-08` High |
| **Kingsbane** | present, changed | ~1-min CD, synced with Deathmark; −15% dmg in 12.1; Regicide's Reward talent | **1 min** | Cast count; inside Envenom | `ROG-03`,`ROG-01`,`ROG-05` High |
| Shiv | present | 1 CP generator; Improved Shiv reportedly removed | UNVERIFIED | – | Med |
| Thistle Tea | present | Energy restore | UNVERIFIED | – | Med |
| Vanish | present | Enables Improved Garrote | UNVERIFIED | Pairing with Deathmark | `ROG-05`,`ROG-03` Med-High |
| Slice and Dice | present | Pre-combat in SimC | – | Pre-pull | `ROG-05` Med |
| Deadly + Amplifying Poison | present | Always both lethal poisons (dual lethal) | – | **Applied before pull** | `ROG-01`,`ROG-02` High |
| Numbing / Atrophic Poison | present | Non-lethal; Atrophic reduces damage the group takes | – | M+ utility choice | Med-High |
| Implacable (Apex) | present, changed 2026-08-25 | +10% Envenom; 2 energy per CP spent. **Season-1 advice to let Envenom drop is obsolete** | – | Stale-advice hazard | `ROG-01`,`ROG-09` Med |
| Indiscriminate Carnage, Arterial Precision, Master Assassin | **removed** (Midnight) | – | – | Do **not** coach old Vanish-AoE patterns | Med |
| Serrated Bone Spike, Cold Blood, Shadowheart, Acrobatic Strikes, Rushed Setup | **removed** | – | – | – | `ROG-02` Med |
| Deadly Momentum | removed in 12.1 | – | – | – | Med |
| Exsanguinate | removed (pre-Midnight, likely) | – | – | – | Low-Med |
| Instant/Wound/Crippling poisons; Caustic Spatter; Internal Bleeding; Sepsis | **UNVERIFIED** | – | – | – | – |

### Defensives, interrupt, CC, utility
| Ability | Finding | CD | Conf |
|---|---|---|---|
| **Kick** (interrupt) | Interrupts + 5 s school lockout | **UNVERIFIED** | Med |
| Feint | 40% AoE DR for 6 s | UNVERIFIED | Med |
| Cloak of Shadows | Magic immunity | 2 min (Method only) | Med |
| Evasion | 100% dodge 10 s | UNVERIFIED | Med |
| Crimson Vial | Small heal | UNVERIFIED | Med |
| Cheat Death | **UNVERIFIED** | – | – |
| Kidney Shot | Finisher stun up to 6 s | UNVERIFIED | Med |
| Shroud of Concealment | 15 s group stealth for trash skips; Stillshroud reduces CD | UNVERIFIED | Med |
| Sap / Blind / Gouge / Cheap Shot / Tricks of the Trade | Sap used for skips; others **UNVERIFIED** | – | Low |

**Rule:** cooldown values must be loaded from versioned game data verified against logs (observed minimum cast interval across many logs), never from this table.

## 3. Hero talents
Both trees are confirmed Assassination options (`ROG-10`, `ROG-02`):
- **Deathstalker** — Deathstalker's Mark applied via opener Garrote; **Darkest Night** procs when final Mark stack consumed/target dies → next max-CP Envenom guaranteed crit (values conflict; none recorded). Clear the Witnesses empowers next Fan of Knives.
- **Fatebound** — Hand of Fate flips a coin on 5+ CP finishers: Heads = stacking damage buff, Tails = Cosmic damage; Mean Streak, Edge Case.

**M+ preference conflicts between sources:** Method (Whispyr, 12.1.5) — Deathstalker ahead 2–5%, default for high-end M+. Icy Veins (12.1.5) — Fatebound for almost all key levels, Deathstalker for push keys. Mythistone popularity ~51% Fatebound. **Decision: rules must branch by hero tree; Ascend must not recommend a hero tree in MVP.** The hero tree used in a run is read from the log's combatant info, not from Blizzard's current profile.

## 4. Maintained guides consulted

| Guide | Patch label / last update | Notes |
|---|---|---|
| Icy Veins PvE DPS guide (`ROG-01`) | 12.1.5; main update seen 2026-08-25 | Author unknown |
| Maxroll M+ guide (`ROG-02`) | 12.1.5 | Author unknown |
| Method guide, Whispyr (`ROG-03`) | 12.1.5 (intro page still 12.0.1) | |
| Wowhead (Whispyr) rotation (`ROG-04`) | last confirmed 2026-05-05, 12.0.5 | **Possibly stale for 12.1** |
| SimC midnight APL (`ROG-05`) | undated | Extract only; may lag 12.1 |

**Consensus priority (Method + Maxroll + SimC consistent):** maintain Garrote + Rupture; in AoE spread bleeds with Crimson Tempest, then Fan of Knives at 2+ targets; Mutilate/Ambush in single target; Envenom at 5+ CP (7 w/ Darkest Night); Deathmark and Kingsbane on cooldown, bleeds refreshed before Deathmark, Vanish→Improved Garrote before Deathmark, Thistle Tea with Kingsbane. "Kick on cooldown" in SimC is a simulation abstraction and **must not** be read as real-play advice.

**Spec standing:** consistently A/S tier for M+ across Method, wow.gg, MythicSim (Medium). Not material to MVP.

## 5. What can reasonably be evaluated post-run

| Area | Evaluable from a log? | Key caveat |
|---|---|---|
| Major CD usage (Deathmark, Kingsbane) | **Likely** — cast events + fight duration | M+ trash: holding CDs for bosses/big packs is often correct. Evaluate **boss encounters only** in MVP. |
| Bleed uptime (Rupture/Garrote) on priority target | **Likely** — debuff apply/remove events on target | Requires defining "priority target" and excluding untargetable windows. Bosses only. |
| Finisher CP | **Uncertain** — needs CP state at cast; WCL resource fields in Midnight unverified | Not MVP until verified. |
| Energy capping | **Uncertain** — needs energy state; primary resources are "secret" to addons but log-file status unverified | Not MVP. |
| DoT spreading in AoE | **Hard** — needs enemy count per moment | Not MVP. |
| Target selection | **Hard** — needs knowledge of which enemy *should* die first (route/mechanics) | Not MVP. |
| Interrupts | **Partially** — successful interrupts are logged; *missed opportunities* require knowing interruptible casts and group assignments | MVP: **factual summary only**, no judgement. |
| Defensive usage | **Partially** — casts logged; "should have used" requires mechanic knowledge | MVP: only in a death review, as observed facts. |
| Downtime | **Hard** — movement/untargetable phases indistinguishable from idling without encounter data | Not MVP. |
| Deaths | **Yes** — death events + preceding damage | MVP: factual death review. |

**Prior art (read directly, `WCL-02`):** WoWAnalyzer's Assassination module implements Garrote/Rupture uptime-and-snapshot tracking, Deathmark, Kingsbane, Envenom, finisher/builder use, Crimson Tempest, AoE hit counts, energy and combo-point graphs, plus event-ordering normalizers (e.g. Deathmark↔Improved Garrote linking). This shows these metrics were computable from WCL data historically, and that **event-ordering quirks exist and need normalization**. The module is marked *MaintainedPartial*, `patchCompatibility: '12.0.0'`. It has **not been updated for 12.1**, which changed Deathmark, Crimson Tempest and Implacable. That is both evidence of feasibility and a gap Ascend could fill.

## 6. Candidate coaching rules (none implemented)

**Threshold policy (applies to every rule).** No rule may fire on an invented threshold. Each rule's threshold is set by a **calibration study**: run the metric over a sample of ≥ N public logs of the same spec, hero tree, encounter and key-level band (cell definition and N in [ANALYSIS_ENGINE.md](../architecture/ANALYSIS_ENGINE.md) §10), record the distribution in versioned rule data, and fire only when the player falls in a clearly separated tail. The threshold and calibration dataset ID are stored with the rule version. Until calibration exists, the rule may only show the **observed fact** with no judgement.

| ID | Behavior | Data dependencies | Calculation | Evidence for expected behavior | Build applicability | Context limits | Confidence criteria | False-positive risks | Player-facing explanation (draft) | Validation | MVP? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **AR-01** | Deathmark usage on bosses | Cast events (player), boss encounter boundaries, verified CD | `uses` vs `opportunities` as defined by metric `boss_cd_opportunities.v1` (ANALYSIS_ENGINE §4: player alive time in the boss pull minus a calibrated grace period, divided by the verified CD) | Guides: use on CD (`ROG-02`,`ROG-03`) | All builds (Deathmark talent assumed core; verify via combatantinfo) | Boss pulls only; pulls with 0 opportunities are not evaluated; untargetable phases may justify holds | Encounter fully logged; CD verified from game data/logs; talent present | Intentional holding for burst phases or for Bloodlust; boss immunity phases | "On [boss] you used Deathmark 2 times; the fight allowed up to 3. Using it on cooldown is the standard recommendation (sources)." | Compare against cohort distribution; manual review of 20 flagged cases | **Candidate** |
| AR-02 | Kingsbane usage on bosses | as AR-01 | as AR-01 with 1-min CD | Guides (`ROG-03`) | Kingsbane talent | as AR-01 | as AR-01 | Synchronization with Deathmark may legitimately delay | similar | as AR-01 | Later (merge with AR-01 if both fire) |
| **AR-03** | Rupture uptime on boss | applydebuff/refreshdebuff/removedebuff events with target IDs; boss actor ID; encounter boundaries | Σ(time Rupture active on any boss actor) / (player alive time in the boss pull) | Guides: ~100% on priority target (`ROG-01`) | All | Untargetable windows are not modeled, and the finding states this; multi-boss encounters complex | Debuff events present and paired; boss identified | Untargetable/intermission phases; boss swaps; player death time (exclude dead time) | "Rupture was active on [boss] for 81% of the time you were alive. Guides recommend keeping it up as close to always as possible." | Cohort distribution; check against WCL's own uptime table for same report (cross-check) | **Candidate** |
| AR-04 | Garrote uptime on boss | as AR-03 | as AR-03 | Guides (`ROG-01`) | All | as AR-03 | as AR-03 | as AR-03 | similar | as AR-03 | **Candidate** (separate rule ID; displayed next to AR-03) |
| AR-05 | Finisher CP efficiency | Cast events with CP state at cast, or resource change events | % of Envenom/Rupture casts below 5 CP (7 w/ Darkest Night buff active) | Guides (`ROG-02`,`ROG-03`) | Hero-tree dependent | Low-CP Rupture can be correct on dying targets | Resource fields verified present | Target-death, emergency | – | – | **No** — resource data UNVERIFIED |
| AR-06 | Energy capping | Energy resource state | time at max energy / active time | Common principle; no sourced threshold | All | – | Resource data verified | Movement/untargetable | – | – | **No** |
| AR-07 | Vanish → Improved Garrote before Deathmark | Cast sequence; Improved Garrote talent | % of Deathmark casts preceded by Vanish + Garrote within T seconds (T from calibration) | Icy Veins (`ROG-01`) | Requires Improved Garrote | Vanish may be used defensively/for skips | Talent confirmed in log | Vanish on CD for other reasons | – | Cohort | Later |
| AR-08 | AoE bleed spreading (CT before FoK) | Casts + enemy count over time | – | Guides (`ROG-03`) | Crimson Tempest talent | Requires per-moment enemy counts | – | High | – | – | **No** |
| AR-09 | Interrupt summary | Interrupt events by player; Kick casts | Count successful interrupts; count Kick casts without interrupt | General M+ principle | All | Assignments unknown; "missed" kicks unknowable | Interrupt events present | Kick used and target died/cast already finished | "You interrupted 9 casts this run (Kick used 11 times)." **Fact only.** | Cross-check with WCL interrupts table | **Candidate (fact, no judgement)** |
| **AR-10** | Death review | Death events; damage taken before death; player defensive casts | For each death: killing ability and damage taken in the prior `window_ms` (rule data, D-018). The defensive-availability line is added only once defensive cooldowns pass T-VER-01; it is excluded from the MVP until then | General principle | All | Whether a defensive *would have* prevented death is unknowable without mechanic data | Death event + damage events present; CDs verified | Some deaths unavoidable; defensive used just before window | "You died to [ability] at 14:32; most damage in the preceding seconds came from [ability]." Availability wording only after T-VER-01. Never says "would have survived". | Manual review | **Candidate (facts + availability only)** |
| AR-11 | Avoidable damage | Damage-taken events + curated per-season avoidable-ability list | Sum of damage from listed abilities | Requires curated list | All | List maintenance every season; Blizzard's built-in meter already tracks avoidable damage | List versioned & reviewed | Mislabeling | – | – | **No** (maintenance, overlap with built-in meter) |
| AR-12 | Feint on predictable AoE | Mechanic catalog | – | – | All | Needs mechanic catalog | – | High | – | – | **No** |
| AR-13 | Envenom buff uptime | Buff events | uptime | Icy Veins: "cannot be 100%, more is better" (no threshold) | All | Implacable changes interaction | – | High without threshold | – | – | **No** |
| **AR-14** | Lethal poisons at pull | Buff state at encounter start (combatantinfo auras or buff events) | Deadly and Amplifying Poison present at encounter start? | Guides: always both (`ROG-01`,`ROG-02`) | All, if dual lethal poisons are confirmed (T-VER-01) | None significant | Aura data verified present | Talent build without dual lethal | "Amplifying Poison wasn't active when the fight on [boss] started." | Manual check vs log | **Candidate (low value, very low risk)** |

### MVP candidate selection (contingent on Gate 1)
1. **AR-01** Deathmark usage on boss encounters.
2. **AR-03** Rupture uptime and **AR-04** Garrote uptime on bosses (separate rule IDs, displayed together).
3. **AR-10** Death review (facts; defensive availability only after T-VER-01).
4. **AR-09** Interrupt summary (fact only — not a "coaching" judgement).
5. **AR-14** Lethal poisons at pull (low-risk sanity check).

**Honest assessment:** only AR-01, AR-03 and AR-04 are genuinely *coaching* (they compare behavior to a recommended standard). AR-10, AR-09 and AR-14 are factual summaries. Whether even these are defensible depends on (a) WCL returning the needed events for Midnight M+ reports and (b) a calibration study. **Both are untested; Gate 2 is NOT YET TESTED.** Gate 2 needs ≥3 qualifying insights, of which ≥2 are calibrated suggestions (FEASIBILITY_TEST_PLAN §3). If fewer than two of AR-01, AR-03 and AR-04 calibrate, the coaching premise fails for this spec.

## 7. Maintenance hazards specific to this spec
- Two of the five central abilities (Crimson Tempest, Deathmark) changed function within the last ~9 months; Implacable changed via hotfix. Expect **at least one rule-affecting change per major patch.**
- Guide sources disagree on hero tree preference; rule logic must be hero-tree aware.
- Wowhead guide may be stale; SimC APL may lag. Prefer a dated cross-check of ≥2 sources before changing a rule.

## 8. UNVERIFIED list
Base max CP; Deeper Stratagem; cooldowns for Kick, Shroud, Vanish, Shiv, Thistle Tea, Crimson Tempest, Evasion, Feint, Crimson Vial, Blind, Kidney Shot (Cloak 2 min from one source only); existence/status of Cheat Death, Tricks of the Trade, Gouge, Cheap Shot, Blind, Instant/Wound/Crippling poisons, Internal Bleeding, Caustic Spatter, Sepsis; exact Crimson Tempest spread rule and whether baseline; Darkest Night values; Deathstalker's Mark stacking; full Fatebound node list; Unstable Toxin effect; whether Kingsbane/Deathmark are baseline or talents; stat priority for 12.1.5; SimC APL currency.
