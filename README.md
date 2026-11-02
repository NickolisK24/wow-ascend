# WoW Ascend (working name)

A planned web app for World of Warcraft Retail **Mythic+ improvement**. Sign in with Battle.net, choose your character, set a goal, import a Warcraft Logs key, and get a short list of evidence-backed findings you can check yourself. Then see whether the same findings improve on your next keys.

**Status (2026-11-02): research baseline only. No application code yet.** The feasibility gates have not passed. Start with **[docs/BASELINE.md](docs/BASELINE.md)**.

## Repository layout
```
docs/                     Baseline, research, product, architecture, compliance, planning, quality
research/proofs-of-concept/  Stdlib-only probes for the Blizzard and Warcraft Logs APIs (not yet run)
research/fixtures/        Sanitized provider responses (raw/ is git-ignored)
CLAUDE.md                 Binding instructions for AI-assisted development
```

## Running the feasibility probes
You need Python 3.11 or later, a network that can reach Blizzard and Warcraft Logs, and API clients for both. See [docs/quality/FEASIBILITY_TEST_PLAN.md](docs/quality/FEASIBILITY_TEST_PLAN.md).
```bash
python3 -m unittest discover -s research/proofs-of-concept -p 'test_*.py'
python3 research/proofs-of-concept/blizzard_api_probe.py      # needs BNET_* env vars
python3 research/proofs-of-concept/wcl_report_probe.py        # needs WCL_* env vars
```

## Not affiliated
This project is not affiliated with or endorsed by Blizzard Entertainment or Warcraft Logs/Archon. World of Warcraft and Battle.net are trademarks of Blizzard Entertainment. The public product name will not use "WoW" (see D-011).
