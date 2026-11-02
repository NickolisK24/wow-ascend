# MVP Specification: "Key Review" for Assassination Rogue

**Date:** 2026-11-02 · **Status:** Baseline v1. This is conditional: **implementation of the coaching scope (screens 5–7) starts only after Gates 1 and 2 pass.** Screens 1–4 and 8–9 can proceed after Gate 3 clears the Battle.net terms.

## 1. Scope decision versus the original proposal

| Proposed item | Decision | Reason |
|---|---|---|
| 1. Battle.net login | **Keep** | Identity and character discovery; documented as supported |
| 2. Character selection | **Keep** | – |
| 3. Basic character dashboard | **Keep, minimal** | Raider.IO/WCL already do this well; it is a frame for findings, not the product |
| 4. M+ progression overview | **Keep, Blizzard data only** | Season best runs and rating come from the API. Full run history is UNSUPPORTED by Blizzard. |
| 5. User-defined goal | **Keep** | Core of the differentiation hypothesis |
| 6. Optional WCL import | **Keep; public (and unlisted, if verified) reports only** | Private reports need WCL user OAuth, deferred to post-MVP |
| 7. Small set of coaching insights | **Keep, 2 coaching rules + 3 factual summaries** | Only AR-01 and AR-03/04 qualify as coaching. See [ASSASSINATION_ROGUE.md](../research/ASSASSINATION_ROGUE.md) §6. |
| 8. Prioritized action plan | **Keep, max 3 items** | – |
| 9. Basic improvement history | **Keep: per-rule trend** | Core of the loop |
| *(new)* "This finding is wrong" feedback | **Add** | Needed to measure false positives |
| *(new)* Free, no-ads beta | **Add** | Blizzard §2B and WCL commercial-approval risk |

**Smallest product worth releasing:** sign in → pick an Assassination Rogue → set a goal → paste a WCL link to a key → see up to 3 boss-level findings with checkable evidence → import the next key and see whether those findings changed.

## 2. Finding presentation rules
Each finding is one of three kinds and always shows its kind label:
- **Observed:** a measured fact (e.g. "You interrupted 9 casts in this key"). Neutral styling.
- **Suggested improvement:** a comparison with a cited recommendation and a calibrated threshold. Accent styling, plus a "Why we think this" panel.
- **Not enough evidence:** what couldn't be evaluated and why ("Boss untargetable phases aren't modeled; uptime not judged"). Muted styling.

Wording rules: never "you should have" about a specific moment unless the rule establishes the required state. Never "would have survived". Always say which encounter. Always link the WCL report and timestamp.

## 3. Screens

### S1 Landing
- **Purpose:** explain the value in one screen and start sign-in.
- **Data:** none.
- **Components:**
  - headline;
  - three-step explainer (Connect, Review a key, Track your fix);
  - a sample finding card built from a sanitized fixture and clearly labeled "Example";
  - Sign in with Battle.net button;
  - "not affiliated with Blizzard" footer;
  - privacy link.
- **States:** static page; no loading or empty state needed.
- **Mobile:** single column.
- **Acceptance criteria:**
  - Renders without JavaScript errors.
  - Lighthouse accessibility ≥ 95.
  - The sample is labeled as an example.
  - No real player data appears.

### S2 Sign-in and onboarding
- **Purpose:** OAuth round-trip, consent explanation and region choice.
- **Data:** region selection (US/EU/KR/TW), OAuth callback.
- **Components:**
  - region picker;
  - a "What we access" list (BattleTag, character list, public character data);
  - redirect to Battle.net;
  - callback handler;
  - first-run explainer.
- **Loading:** "Connecting to Battle.net…".
- **Errors:**
  - User denied consent → "You can try again any time." Nothing is stored.
  - State mismatch → generic error. The event is logged.
  - Provider down → retry button.
- **Acceptance criteria:**
  - No password field anywhere.
  - A forged `state` parameter is rejected.
  - Denying consent creates no account row.

### S3 Character selection
- **Purpose:** choose a character.
- **Data:** account character list (`/profile/user/wow`), cached for this session only.
- **Components:**
  - list grouped by realm;
  - class and spec icon;
  - level;
  - a "Supported" badge for Rogue (Assassination analysis);
  - search box.
- **Empty state:** "No Retail characters found on this region's account." Includes a region switch.
- **Errors:** account endpoint failure → retry. Characters below the level cap are shown as "not eligible".
- **Mobile:** list.
- **Acceptance criteria:**
  - Only Retail characters are shown.
  - Selecting one creates or updates the character record and opens S4.

### S4 Character dashboard
- **Purpose:** an at-a-glance status, the goal, and the entry point for imports.
- **Data:** profile summary, equipment, specializations, keystone profile and season details, latest analyses, goal.
- **Components:**
  - header (name, realm, spec, item level);
  - **freshness chip** ("Updated 3 h ago from Blizzard", with a refresh button);
  - M+ rating with the season best per dungeon (8 rows, timed or over-time flag);
  - goal card;
  - gear list with "no enchant" / "empty socket" facts (observed only; no recommendations about *which* enchant);
  - Review a key button;
  - latest findings summary.
- **Loading:** skeletons per card.
- **Empty states:**
  - no goal → goal setter;
  - no runs this season → "No timed or completed keys found this season";
  - no analyses → import call-to-action.
- **Errors:**
  - Character 404 → "Blizzard isn't sharing this character's data right now (it may need to log out, or it was renamed/transferred)." No stale data is shown as current.
  - Partial endpoint failure → only the affected card shows an error.
- **Mobile:** stacked cards; gear collapsed.
- **Acceptance criteria:**
  - Every displayed field maps to a provider field or shows "unavailable".
  - Data older than 24 h is labeled stale.
  - Rating is Blizzard's value, never computed by Ascend.

### S5 Combat report import
- **Purpose:** turn a WCL URL into an analysis.
- **Data:** URL input, report metadata, key list.
- **Components:**
  - URL field with inline validation;
  - "How to get a link" help (public/unlisted upload via Archon App);
  - key picker (dungeon, level, timed or not, date) when the report has several keys;
  - character auto-match;
  - progress steps (Fetching report → Checking supported data → Analyzing → Done).
- **Errors, each with a specific message:**
  - invalid URL;
  - report private;
  - report archived or inaccessible;
  - no M+ fights;
  - character not in report;
  - not Assassination;
  - game version not supported by the current rule set;
  - WCL rate limit (queued; "we'll finish shortly");
  - WCL down;
  - duplicate (link to the existing analysis).
- **Mobile:** works with a pasted URL.
- **Acceptance criteria:**
  - The same report and key imported twice yields one analysis (idempotent).
  - Unsupported input makes no further WCL calls after detection.
  - No raw events are persisted.

### S6 Post-run analysis
- **Purpose:** show the findings for one key.
- **Data:** analysis record, findings, evidence.
- **Components:**
  - run header (dungeon, level, result, duration, date, rule-set version);
  - boss-by-boss sections;
  - finding cards (kind label, one-sentence statement, key number, confidence);
  - an expandable evidence panel (exact values, timestamps with WCL deep links, rule ID/version, calculation description, limitations, sources);
  - an "Insufficient evidence" section;
  - a "This looks wrong" button.
- **Empty state:** "No issues found by the rules we support" plus a list of what was *not* evaluated.
- **Errors:** analysis failed → reason and retry; partial data → findings for the evaluable parts only, plus a limitation banner.
- **Mobile:** cards; the evidence panel opens as a full-screen sheet.
- **Acceptance criteria:**
  - Every suggested-improvement card has non-empty evidence, a rule version and a source citation.
  - The "Insufficient evidence" section lists every rule that was skipped, with the reason.

### S7 Improvement plan
- **Purpose:** what to do next.
- **Data:** the latest analysis's suggested improvements, priority order and the goal.
- **Components:**
  - up to 3 ordered actions, each with "why it matters for your goal" text from rule metadata (not generated);
  - "How we'll check" text (e.g., "We'll compare Deathmark usage on bosses in your next imported key");
  - link to the evidence.
- **Empty state:** "Nothing to fix from what we can measure. Here's what we can't measure yet."
- **Acceptance criteria:**
  - The order is reproducible from the documented priority function.
  - No more than 3 items.

### S8 Progress history
- **Purpose:** show whether the fixes stuck.
- **Data:** analyses over time; per-rule metric values; Blizzard rating snapshots.
- **Components:**
  - timeline of analyses;
  - per-rule trend rows (values per analysis; status flagged / not flagged / not evaluated);
  - rating snapshots versus the goal.
- **Empty state:** "Import a second key to see trends."
- **Rule:** values from different rule versions are shown separately and are **never joined into one trend line** without a version marker.
- **Mobile:** stacked rows.
- **Acceptance criteria:** trends use only stored derived values; no interpolation.

### S9 Account settings and privacy
- **Purpose:** control over the user's data.
- **Components:**
  - connected Battle.net (BattleTag) with Disconnect, which deletes the account (with an explanation);
  - "Your stored data" list;
  - delete analysis / character / account;
  - links to the privacy policy and Battle.net app-authorization management;
  - data retention summary.
- **Acceptance criteria:**
  - Account deletion removes all user-owned rows (verified by an integration test).
  - The session is invalidated.
  - Confirmation is required.

## 4. Non-goals (MVP)
- Full multi-class support.
- Real-time or in-combat assistance of any kind.
- Automated gameplay.
- A Raidbots-style simulation or gear optimizer.
- Proprietary combat simulation.
- Route creation.
- Team or matchmaking features.
- Social features or public profiles.
- Native mobile apps.
- **Billing or ads.**
- Generative AI as a source of gameplay truth.
- Private WCL reports (post-MVP).
- Avoidable-damage analysis (maintenance cost, and it overlaps with Blizzard's meter).
- Raid analysis.
- Cohort comparisons shown live (calibration happens offline only).
- Raider.IO integration (terms unverified).
