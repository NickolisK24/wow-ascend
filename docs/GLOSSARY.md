# Glossary

Game terms are defined as WoW Ascend uses them. Where current behavior matters, see the research documents for sources.

| Term | Meaning |
|---|---|
| **Affix** | A modifier on a Mythic+ run that changes with key level and week, e.g. Fortified, Tyrannical, Xal'atath's Bargain or Guile, Lindormi's Guidance |
| **Analysis** (Ascend) | One evaluation of one key by one rule-set version. Immutable once created |
| **AoE** | Area of effect: hits multiple targets |
| **Archon** | The company operating Warcraft Logs, Archon.gg, WoWAnalyzer and Wipefest. Also the name of its desktop uploader app |
| **Assassination** | A Rogue specialization built on bleeds and poisons. Spec ID 259 (verify) |
| **Battle.net** | Blizzard's account and login platform. Its OAuth service is what lets Ascend sign users in |
| **BattleTag** | A user's Battle.net display name (`Name#1234`). Treated as PII |
| **Bleed** | A physical DoT, e.g. Garrote or Rupture |
| **Buff / Debuff** | A timed beneficial or harmful effect on a unit |
| **Calibration** (Ascend) | An offline study of metric distributions across many logs, used to set rule thresholds |
| **Combat log** | The file the game client writes (`WoWCombatLog.txt`) when logging is enabled. Warcraft Logs parses it |
| **Combo points (CP)** | The Rogue resource that builders generate and finishers spend |
| **Connected realm** | A group of realms that share infrastructure; leaderboards are keyed by it |
| **Cooldown (CD)** | The time before an ability can be used again |
| **Coverage** (Ascend) | A record of which event categories were requested and returned for an analysis |
| **Deathmark** | Assassination's main cooldown, about 2 minutes. Reworked in 12.1 |
| **DoT** | Damage over time |
| **Dungeon pull** | A WCL subdivision of a Mythic+ run: one trash pack or one boss encounter |
| **Envenom** | Assassination's main damage finisher |
| **Evidence** (Ascend) | Metric values and event references that back a finding |
| **Finding** (Ascend) | A rule output of kind *observation*, *suggestion* or *insufficient evidence* |
| **Game data version** (Ascend) | An immutable, dated snapshot of reference tables such as spells, cooldowns and dungeons |
| **GCD** | Global cooldown: the short lockout after most abilities |
| **Great Vault** | A weekly reward chest. M+ slots unlock at 1, 4 and 8 runs |
| **Hero talents** | A third talent tree, one of two per spec. Assassination's are Deathstalker and Fatebound |
| **Item level (ilvl)** | Numeric item power; the character value is an average across slots |
| **Key / Keystone** | The item that starts a Mythic+ run at a given level. "Timing" a key means finishing within the timer |
| **Kingsbane** | An Assassination cooldown of about 1 minute, synced with Deathmark |
| **Midnight** | The current expansion (12.x), launched 2026-03-02 |
| **Mythic+ (M+)** | Scaling 5-player dungeons with a timer |
| **Mythic+ rating** | Blizzard's seasonal score, based on best runs. Ascend displays it and never computes it |
| **Namespace** | The Blizzard API data partition: `static-`, `dynamic-` or `profile-{region}` |
| **Observation** (Ascend) | A measured fact, with no judgement |
| **Pandemic** | Refreshing a DoT early carries its remaining duration over, up to a limit |
| **Patch** | A game version, e.g. 12.1.5 |
| **Realm slug** | The URL-safe realm identifier used in API paths |
| **Region** | US, EU, KR, TW (and CN, which is out of scope) |
| **Rule / rule version** (Ascend) | A deterministic check with metadata: applicability window, inputs, calibration and explanation |
| **Rule set version** (Ascend) | The rule versions active for a spec, e.g. `assa-12.1-r1` |
| **Rupture / Garrote** | Assassination bleeds that should be maintained on the priority target |
| **Season** | A roughly six-month competitive period with a fixed dungeon pool and rewards. Season 2 is live; Season 3 is announced for winter 2026–27 |
| **Secret values** | The Midnight mechanism that hides combat state from addons |
| **Spec** | A specialization within a class; it determines the role and abilities |
| **Suggestion** (Ascend) | A finding that compares behavior with a cited, calibrated recommendation |
| **Uptime** | The share of time a buff or debuff is active |
| **WCL** | Warcraft Logs, the combat-log analysis site and API |
