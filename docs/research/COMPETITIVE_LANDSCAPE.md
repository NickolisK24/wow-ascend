# Competitive Landscape — Personalized Mythic+ Improvement

**Research date:** 2026-11-02 · **Status:** Baseline v1

> **Evidence basis.** All product information comes from web-search summaries of vendor pages, news posts and GitHub. **No page was opened directly** (sandbox network policy), and no product was used hands-on. Several newer products are known **only from their own marketing**. A product is said to lack a feature only where we found evidence; otherwise the cell is "?" (unknown). Confidence: H = official/primary & recent; M = secondary or vendor marketing; L = inferred/contradictory.

## 1. Headline finding

**"An AI reads your Warcraft Logs report and tells you what to fix" already exists, in at least four products launched 2025–2026:** WowCoach.gg, ExplainMyLogs, ParsePal and the wow.gg Logs Analyzer (M, `COMP-17..20`). WowCoach.gg already offers **Battle.net sign-in, M+ support, a desktop auto-uploader and paid tiers** ($5.99–24.99/mo). A fifth, MythicIQ, offers non-AI M+ death/interrupt/avoidable-damage analysis (`COMP-21`). WoWAnalyzer (owned by Archon/WCL) offers deterministic per-spec checklists, but its Assassination module is only partially updated for Midnight (`WCL-02`).

**Consequence:** the originally proposed differentiator ("personalized post-run coaching") is **not** a differentiator by itself. The remaining credible gaps are narrower (§4) and are **hypotheses requiring user testing.**

## 2. Product profiles

| Product | Audience | Major features | Data sources | Char. connectivity | Perf. analysis | Personalized coaching | M+ focus | Pricing | Strengths | Weaknesses | Covers Ascend? | Integration |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Warcraft Logs / Archon App** (`COMP-01..05`) | Everyone who logs | Upload, rankings, parses, timelines, comparisons; **Archon App** (since 2026-06-29): upload + **gameplay video synced to pulls** | Combat log files | Battle.net link/login; claim characters seen in logs | Raw data & tables, no verdicts | No native per-player AI/insights **found** (unverified absence) | Yes (M+ rankings) | Patreon Silver/Gold/Platinum; prices unverified (~$2/5/10 per one source) | Data monopoly, trust, video | Steep learning curve | Data layer only | **Required dependency** (API) |
| **Archon.gg** (`COMP-01`,`COMP-15`) | Meta-followers | Tier lists, meta builds from WCL incl. ex-Subcreation algorithm | WCL | Shared account | Aggregate only | No | Yes | Free + ads | Authority on "what top players do" | No personal analysis | Partly (builds) | Link-out |
| **Raider.IO** (`COMP-06`,`COMP-07`) | M+ players, PUGs | Score, leaderboards, addon, Desktop Client **Live Tracking**, **M+ Replays**, Auto Route Creator, heatmaps, talent builds; owns Keystone.guru | Blizzard API + its client reading combat log | Battle.net link | Replay/heatmap review | No automated coaching found | **Core** | Revered $5, Exalted $10, Illustrious $20/mo | Owns M+ identity (score) | No recommendations | Score/goal tracking | Public API (terms UNVERIFIED) |
| **Raidbots / SimulationCraft** (`COMP-08`) | Gear optimizers | Quick Sim, Top Gear, Droptimizer | SimC addon export | ? | Simulation, not play | No | No | Premium (prices UNVERIFIED) | Gear truth | No log analysis | Out of MVP scope | Link-out |
| **Wowhead** (`COMP-09`) | All | DB, news, guides; Wowhead Client "combat log support" (purpose unclear) | Game data | ? | No native log analysis found | No | Partial | Premium ~$2? (L) | Reach | – | Guides | Citation source |
| **Icy Veins** | All | Spec guides, sims | Editorial | ? | No | No | Partial | Ads (presumed) | Up-to-date guides | – | Guides | Citation source |
| **Keystone.guru** (`COMP-10`) | Route planners | Routes, MDT import, heatmaps | Community | ? | No run analysis found | No | **Yes** | Free + Patreon | Route standard | – | Not MVP | Link-out |
| **WoWAnalyzer** (`COMP-11`,`WCL-02`) | Spec-improvers | Per-spec checklists, rotation/CD/DoT analysis of one report | WCL | None | **Yes (deterministic)** | Checklist-style suggestions | Partial | Free, open source | Evidence-based model | Midnight support spec-by-spec, Assassination at 12.0.0 partial; single report; no goals | **High overlap** with Ascend's engine | Study design; licence check before reuse |
| **Wipefest** (`COMP-12`) | Raid teams | Raid mechanic/execution analysis | WCL | None | Yes (raid) | Partial | No | Patreon | Mechanics focus | Raid only | Low | – |
| **Lorrgs** (`COMP-13`) | Raiders | Top-parse CD timelines | WCL | None | Aggregate | No | No | Patreon | – | Raid only; Midnight status unknown | Low | – |
| **murlok.io** (`COMP-14`) | Build seekers | Top-50 builds per spec, updated 8-hourly, Midnight S1/S2 | Blizzard API | None | No | No | Yes | Free? | Fresh | No personal analysis | Low | Link-out |
| **Human coaches (Metafy)** (`COMP-16`) | Motivated improvers | Live coaching, **log review** | Human | – | Human | **Yes** | Yes | **$25–60/hr**; $75 bootcamp | Context, judgement | Cost, availability | Same job, different form | WTP benchmark |
| **WowCoach.gg** (`COMP-17`) | Raid + M+ | Free log analysis (death recaps, wipes, interrupts, DPS); **AI chat coach** with timestamps; desktop auto-upload; "Live Analysis" between pulls (Pro); MCP server | Raw logs, desktop app | **Battle.net sign-in** | Yes | **Yes (AI chat)** | Yes | Free credits; $5.99 / $14.99 / $24.99 mo | Closest full competitor; integrated upload | Chat/credit model; marketing numbers inconsistent | **Largely yes** | – |
| **ExplainMyLogs** (`COMP-18`) | DPS improvers | Paste WCL link; compares vs strong same-spec players in **same dungeon & key level**; rotation, CDs, uptimes, lust windows, deaths, gear; SimC run; AI "what to change next pull" | WCL + SimC | ? | Yes | **Yes (AI)**, warns AI can be wrong | Yes | ? | Cohort comparison | AI reliability admitted | **Largely yes** | – |
| **ParsePal** (`COMP-19`) | All specs | "AI rotation coach", 41 specs, <60 s, "play quality" score | WCL? | ? | Yes | **Yes (AI)** | Partial | ~3 free/week; paid ? | Breadth, speed | Likely shallow per spec | Partly | – |
| **wow.gg Logs Analyzer** (`COMP-20`) | All | Fight breakdown, deaths, interrupts, top-log comparison, AI coach, Top Gear | WCL / raw logs | ? | Yes | **Yes (AI)** | Partial | $4.95 / $19.95 / $39.95 mo | Bundled with guides | Metered responses | Partly | – |
| **MythicIQ** (`COMP-21`) | M+ | Deaths, avoidable damage, interrupts, replay; desktop auto-load | Raw logs | ? | Yes | Not described as AI | **Yes** | ? | M+-specific | Unknown traction | Partly | – |
| **Open-source AI analyzers** (`COMP-22`) | Hobbyists | LLM reports, cohort comparison, WCL MCP servers | WCL | – | Varies | Yes | Varies | Free | – | – | Low-quality substitutes | – |
| **Blizzard in-game (Midnight)** (`COMP-23..25`) | Everyone | Built-in damage meter (damage, healing, interrupts, dispels, deaths; **avoidable damage**), improved death recap, Cooldown Manager, encounter timeline; **Calibration Chamber** test room announced for 12.2 | Server | Native | Basic | No | Partial | Free | Zero friction | Shallow | Reduces need for basic facts | **Practice venue** for Ascend findings |

**Addon ecosystem (Midnight):** WeakAuras has no Retail Midnight version (H, `COMP-26`); Hekili discontinued (M); Details! survives on `C_DamageMeter` with secret values (M); DBM/BigWigs survive, reworked (M). In-combat helpers are largely gone, so **learning moves to post-run review**. That supports the category and also explains why it's crowded.

## 3. Feature comparison matrix
Y = yes, P = partial, N = no (evidence found), ? = unknown.

| Feature | WCL/Archon | Archon.gg | Raider.IO | Raidbots | WoWAnalyzer | WowCoach | ExplainMyLogs | ParsePal | wow.gg | MythicIQ | Blizzard UI | **Ascend (proposed)** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Battle.net login | Y | P | Y | ? | N | **Y** | ? | ? | ? | ? | n/a | Y |
| Character dashboard | Y | N | Y | P | N | P | ? | ? | ? | ? | Y | Y (minimal) |
| M+ score tracking | P | N | **Y** | N | N | ? | N | N | ? | ? | Y | Y (display Blizzard's) |
| Log import | Y | N | P | N | Y | Y | Y | Y | Y | Y | n/a | Y (WCL link) |
| Per-player automated analysis | P | N | N | N | **Y** | **Y** | **Y** | **Y** | **Y** | Y | P | Y (one spec) |
| Deterministic, cited findings (no LLM verdicts) | n/a | n/a | n/a | n/a | **Y** | N (AI) | N (AI) | N (AI) | N (AI) | ? | n/a | **Y** |
| Prioritized action plan | N | N | N | N | P | ? | P | ? | ? | ? | N | **Y** |
| Goal-anchored plan | N | N | P | N | N | ? | N | N | ? | ? | N | **Y** |
| Progress tracking across runs | P | N | Y (score) | N | N | ? | ? | ? | ? | ? | N | **Y** |
| Spec guides | N | P | P | N | P | P | N | P | Y | ? | N | N (link-out) |
| Sim / gear optimization | N | N | P | **Y** | N | P | P | N | Y | ? | N | N |
| Route planning | N | N | Y | N | N | N | N | N | ? | ? | N | N |
| Meta builds | N | **Y** | Y | N | N | N | N | N | ? | ? | N | N |
| Video review | **Y** | N | P (replays) | N | N | ? | N | N | ? | P (replay) | N | N |

## 4. Is personalized post-run coaching already solved?

**Generic version: largely yes, and commoditizing.** Players can already get AI explanations of a log within a minute, cohort comparisons by dungeon and key level, and timestamped chat answers.

**Plausible gaps (hypotheses, not facts; competitor capabilities verified only via their marketing):**
1. **Goal → findings → practice → re-measure loop.** No product found anchors findings to a stated M+ goal and checks across later runs whether a specific finding improved. *Strongest hypothesis.*
2. **Deterministic, evidence-cited findings with explicit "insufficient evidence" states.** AI tools warn they can be wrong or meter per answer. WoWAnalyzer has the right model but lags Midnight for Assassination.
3. **Depth on one spec, current to 12.1.** Breadth-first AI tools are likely shallow per spec (unverified).
4. **M+-specific framing** (boss pulls inside keys, deaths at +12 cost 15 s). Partially claimed by ExplainMyLogs, WowCoach and MythicIQ.
5. **Calibration Chamber hand-off** (12.2): pair a finding with an in-game practice drill. Not claimed by anyone found; depends on 12.2 shipping.

**Threats:** Archon (WCL + WoWAnalyzer + video) could add native coaching and controls Ascend's data supply (medium-high likelihood, no announcement). Competitors charge $0–15/mo; Blizzard terms may prohibit charging anyway (see compliance). M+ upload rates are lower than raid, so cohorts for one spec × dungeon × key band may be thin.

**Verdict for Gate 4:** **NOT YET TESTED.** Research shows the broad concept is covered; the narrow gaps above are untested hypotheses. Gate 4 can pass only if user research (§5) shows players value (1) and (2) over existing tools.

## 5. User research plan (no interviews have been conducted)

### 5.1 Hypotheses awaiting validation
| ID | Hypothesis | Disconfirming evidence |
|---|---|---|
| H1 | M+ players who want to improve do not know their highest-impact fix after a run | Most interviewees can name their top issue and how they found it |
| H2 | Existing tools (WCL, AI coaches) are too time-consuming or untrusted for regular post-run review | Interviewees already review regularly and are satisfied |
| H3 | Players trust deterministic, cited findings more than AI-written explanations | No preference, or AI preferred for convenience |
| H4 | A goal-anchored plan with re-measurement would change behavior in the next runs | Players say they'd read once and not return |
| H5 | Players will upload/connect WCL logs for this | Majority don't log M+ and won't start |
| H6 | Assassination-only is enough to recruit a beta cohort of 15–30 users | Recruiting fails within 2 weeks |
| H7 | Players would pay | (Not tested — monetization may be prohibited; ask only about value) |

### 5.2 Recruiting criteria (15–20 players)
- Retail players active in Midnight Season 2 M+.
- Skill bands (by current rating): 4–5 below 1,500; 5–6 at 1,500–2,499; 4–5 at 2,500–2,999; 2–3 at 3,000+.
- At least **8 Rogue players (≥5 Assassination)**; the rest any DPS spec (to test generalizability).
- Mix: ≥5 who already use WCL regularly; ≥5 who never/rarely log; ≥3 who have used an AI log tool.
- Regions: NA and EU. Exclude people with a commercial interest in competitors.
- Channels: rogue class Discord (Ravenholdt — UNVERIFIED that it is still active), r/CompetitiveWoW, M+ community Discords, personal network. Get each community's moderator permission before posting.
- Consent: verbal/written consent for notes; no recording without explicit consent; no account credentials ever requested.

### 5.3 Interview script (30–40 min, semi-structured)
**Warm-up (5 min)**
1. What do you play in M+ and what's your current rating? What's your goal this season?
2. How many keys a week? With a fixed group or PUGs?

**Current improvement behavior (10 min)**
3. Walk me through the last time you tried to get better at your spec. What did you do, step by step?
4. Which tools did you use (WCL, Raider.IO, guides, AI tools, coaches, the in-game meter or death recap)? What did each give you?
5. How much time do you spend reviewing a key after it ends? When did you last do it?
6. What's confusing or annoying about those tools? Show me, if you can (screen-share optional).

**Self-diagnosis (5 min)**
7. What's the main thing holding back your keys right now? How do you know?
8. Has a tool ever told you something about your play that surprised you? Did you change anything?

**Automated recommendations and trust (10 min)**
9. If a website said "On the last boss you used Deathmark 2 of a possible 3 times," how would you react? What would you want to see to believe it?
10. Compare: (a) a short list of 3 issues, each showing the exact evidence and its source; vs (b) an AI chat you can ask about your log. Which would you use after a key, and why?
11. Would you connect Battle.net or Warcraft Logs to a new site? What would stop you?
12. Do you log your M+ runs today? If not, would you start, and what would make it worth it?

**Behavior change (5 min)**
13. If the site told you one thing to fix and then checked your next 3 keys, would that be useful or annoying?
14. What would make you come back after the first visit?

**Close:** anything we didn't ask? May we contact you for the beta?

### 5.4 Synthesis method
Tag notes per hypothesis (supports / contradicts / neutral). Gate 4 PASS criteria (proposed): ≥60% of interviewees choose the evidence-list format, or the goal-plus-re-measure loop, over their current workflow, **and** ≥8 commit to a beta. Record results in `docs/research/USER_RESEARCH_FINDINGS.md`, created only once interviews exist.
