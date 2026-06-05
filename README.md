# Skill Forge

Forge, scaffold, package, and retire production-grade agent skills with eval gates and team governance. Implements a 5-phase lifecycle: **Capture & Design → Draft & Scaffold → Evaluate & Iterate → Harden & Gate → Package & Ship**, with Go/No-Go signals between phases and a Gate checklist (including the new Gate 5: gotchas completeness) at packaging time.

## When to use

Trigger this skill when the user wants to:

- Build a skill for **team reuse** with structured evals and gates
- Run an **eval iteration loop** with `with-skill` vs `baseline` comparison
- Decide whether a skill should be **retired** (capability skills)
- **Package** a skill into a `.skill` file for distribution

For pure **architectural pattern selection**, use [`skill-architect`](https://github.com/xifeng12/skill-architect) instead. For **autonomous skill quality optimization** via hill-climbing, see [`darwin-skill`](https://github.com/xifeng12/darwin-skill). For **quick personal skills or MCP integration**, see `skill-creator`.

## Quick start

```
Phase 1: Capture & Design   →  Go signals checklist (7 items)
Phase 2: Draft & Scaffold   →  init_skill.py + evals/evals.json
Phase 3: Evaluate & Iterate →  run_eval_suite.py + gotchas extraction
Phase 4: Harden & Gate      →  5 gates (resource, governance, description, blind eval, gotchas)
Phase 5: Package & Ship     →  manifest.json + .skill file
```

## What's new in v1.3.0

- New `references/anthropic-content-quality.md` — content quality checklist (description writing, gotchas, state files, on-demand hooks, content strategy by scene category)
- New `references/gotchas-template.md` — append-only gotcha log template with `G-1-001` style IDs
- **2 new Go signals** in Phase 1: identifiability of gotchas + cross-invocation state retention
- New **Gotchas Extraction** subsection in Phase 3 (extract structured gotchas after each eval iteration)
- New **Gate 5** in Phase 4: `scripts/gotchas_check.py` verifies every NOT-instruction in SKILL.md has a matching gotcha entry
- New Reference Map entries for `Gotchas Template` and `Content Quality`

## Repo layout

```
skill-forge/
├── SKILL.md
├── AGENTS.md
├── STATE.md
├── manifest.json
├── README.md
├── LICENSE
├── references/
│   ├── anthropic-content-quality.md
│   ├── gotchas-template.md
│   └── ... (full set: goal-vs-procedure, design-patterns, governance, etc.)
└── scripts/
    ├── init_skill.py
    ├── run_eval_suite.py
    ├── validate_skill.py
    ├── trigger_eval.py
    ├── diff_eval.py
    ├── build_confusion_matrix.py
    └── gotchas_check.py
```

> The scripts in this repo are the ones referenced by `SKILL.md` → Scripts Map. Additional internal scripts used by the author during development (e.g. `darwin-skill` automation helpers) are intentionally omitted to avoid ghost-script anti-patterns.

## Install

```bash
npx skills add xifeng12/skill-forge
# or copy to ~/.claude/skills/custom/skill-forge/
```

## License

MIT — see [LICENSE](LICENSE).
