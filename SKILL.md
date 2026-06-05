---
name: skill-forge
description: Forge, scaffold, package, and retire production-grade agent skills with eval gates and team governance. Use when building a skill for team reuse, running structured evals with pass/fail gates, deciding whether a skill should be retired, or packaging skills for distribution. Covers the full lifecycle with Go/No-Go assessment, phased design, iterative evaluation, and production governance. For quick personal skills or MCP integration guidance, see skill-creator. For optimizing an existing skill's quality via autonomous experiments, use darwin-skill. For architecture-only questions (which pattern to use), see skill-architect.
license: MIT
metadata:
  version: "1.3.0"
  philosophy: "structured design + iterative evaluation + production governance"
  skill_type: "Library"
  mode: "Production"
---

# Skill Forge

Build reusable skill packages, not long prompts.

## Quick Start

**I want to create a skill** → Start at [Phase 1: Capture & Design](#phase-1-capture--design). Verify Go/No-Go signals before proceeding.

**I want to evaluate a skill** → Jump to [Phase 3: Evaluate & Iterate](#phase-3-evaluate--iterate). Set up eval workspace first.

**I want to package a skill** → Go to [Phase 4: Harden & Gate](#phase-4-harden--gate), then [Phase 5: Package & Ship](#phase-5-package--ship).

**I want to retire a skill** → Run [Retirement Criteria](#phase-3-evaluate--iterate) in Phase 3.

## Skill Types

Skills fall into two categories with different lifecycles. See [Skill Types](references/skill-types.md) for details.

- **Capability skills**: Help the agent do something the base model can't do consistently (e.g., PDF form filling). May become unnecessary as models improve — evals will tell you when.
- **Preference skills**: Encode your specific workflow (e.g., your team's code review steps). Durable but need to stay in sync with your actual process.

## Router Rules

- Route by frontmatter `description` first.
- Keep `SKILL.md` to routing plus the minimal execution skeleton.
- Push long guidance to `references/`, deterministic logic to `scripts/`.
- Use the lightest process that still makes the skill reliable.

## Modes

- `Scaffold`: exploratory or personal — quick drafts, minimal gates.
- `Production`: team reuse with focused gates and evals.
- `Library`: shared infrastructure or meta skill — full governance.

Mode rules: [Operating Modes](references/operating-modes.md), [QA Ladder](references/qa-ladder.md).

## Phase Progression Constraints

Any phase may abort if the user says "stop" or intent changes fundamentally.

| Transition | Requirement |
|------------|-------------|
| Phase 1 → 2 | Intent captured AND Go/No-Go evaluated (Go − NoGo ≥ 4) |
| Phase 2 → 3 | SKILL.md draft + evals.json + workspace ready |
| Phase 3 → 4 | Eval iteration converged (feedback empty or user satisfied) |
| Phase 4 → 5 | ALL gates pass. If any gate fails, return to Phase 3 or 2. |

---

### Phase 1: Capture & Design

**Outcome**: Clear intent + completed Go/No-Go assessment + selected mode and archetype.

**Constraints**:
- Go − NoGo ≥ 4 before entering Phase 2.
- Go − NoGo < 2 → suggest alternatives (script, alias, or prompt).
- 2 ≤ Go − NoGo < 4 → flag as marginal, recommend Scaffold mode with minimal scope.
- Never select Production/Library for marginal skills.
- Write the `description` early and verify route quality before expanding.

**Signals**:

Go (+1 each, target ≥ 4):
- [ ] Repeated workflow across sessions, not one-off
- [ ] Benefits from structured approach (templates, rules, constraints)
- [ ] Has clear trigger phrases for discovery
- [ ] Would be useful to share with team or reuse
- [ ] Combines multiple tools/steps or wraps an external API
- [ ] Has identifiable Gotchas — specific errors Claude makes in this domain without guidance
- [ ] Needs to retain state across invocations (history, user config, execution log)

No-Go (−2 each, hard stop if ≥ 2):
- [ ] One-off task, never repeated
- [ ] Simple enough for a single instruction or alias
- [ ] Changes every time (no reusable pattern)
- [ ] Better suited as a script or external tool
- [ ] Just a reference file or prompt template

**References**: [Non-Skill Decision Tree](references/non-skill-decision-tree.md), [Reference Scan](references/reference-scan.md), [Skill Archetypes](references/skill-archetypes.md), [Skill Types](references/skill-types.md), [Description Craft](references/description-craft.md)

---

### Phase 2: Draft & Scaffold

**Outcome**: SKILL.md draft + `evals/evals.json` + eval workspace aligned to mode.

**Constraints**:
- Minimum 2 test cases covering realistic scenarios.
- Workspace structure must match the template in `references/iteration-workflow.md`.
- Gate selection must match mode:
  - **Scaffold**: description lint + basic trigger eval only.
  - **Production**: add resource boundary + blind eval.
  - **Library**: add governance check + full QA ladder.

**Workspace template**:
```
<skill-name>-workspace/
└── iteration-1/
    ├── eval-1-<scenario>/
    │   ├── with_skill/outputs/
    │   └── without_skill/outputs/
    ├── eval-2-<scenario>/
    └── benchmark.json
```

**References**: [Gate Selection](references/gate-selection.md), [Iteration Workflow](references/iteration-workflow.md)

---

### Phase 3: Evaluate & Iterate

**Outcome**: Iterated skill + `benchmark.json` + empty or addressed `feedback.json`.

**Constraints**:
- Spawn with-skill AND baseline runs in parallel.
- Draft assertions while runs complete, then grade and aggregate.
- Launch eval viewer for human review before proceeding.
- Repeat iteration until user is satisfied or feedback is empty.

**Gotchas 提炼** (run after each eval iteration):

From failed cases in `benchmark.json`, extract structured Gotchas into `references/gotchas.md`:

```markdown
## Known Failure Modes

- [Scenario]: Claude defaults to [wrong behavior]. Correct: [expected behavior].
  - Found in: iteration-N / eval-X
  - Fixed by: [instruction added to SKILL.md]
  - Status: OPEN | RESOLVED in vX.X
```

Gotchas.md is append-only. Mark resolved entries — never delete them. This file accumulates institutional knowledge across all versions.

Load `references/anthropic-content-quality.md` for content quality rules to apply during extraction.

**Retirement criteria** (Capability skills only):
- Run evals without the skill. If outputs are equivalent, the model has absorbed the skill's value.
- **Retirement signals** (≥2 required to recommend retirement):
  - [ ] Baseline output quality ≥ with-skill output quality
  - [ ] Model version upgrade since skill creation
  - [ ] Skill has not been invoked in 30+ days
  - [ ] The wrapped API/tool has changed significantly
- **Decision rule**: If ≥2 signals match, present evidence and recommend retirement. Default to **keep** unless evidence is strong. For Preference skills, skip retirement check but flag if workflow is outdated.

**References**: [Iteration Workflow](references/iteration-workflow.md), [Skill Types](references/skill-types.md)

---

### Phase 4: Harden & Gate

**Outcome**: Skill that passes all gates appropriate to its mode.

**Constraints**:
- Run gates in order. **If any gate fails, stop and report — do not proceed to packaging.**
- Gate failure path: Report which gate failed and why → suggest fix → return to relevant phase → re-run gate.

**Gate checklist**:
| Gate | Script | Fail action |
|------|--------|-------------|
| Resource boundary | `scripts/resource_boundary_check.py` | List oversized files, suggest splitting or compression |
| Governance | `scripts/governance_check.py` | List violations (secrets, hardcoded paths, missing licenses) |
| Description optimization | `scripts/optimize_description.py` | Flag ambiguous trigger words, suggest alternatives |
| Blind eval | `scripts/judge_blind_eval.py` | Skill performs worse than baseline; return to Phase 3 |
| Gotchas completeness | `scripts/gotchas_check.py` | SKILL.md contains NOT-instructions with no corresponding gotchas.md entry; OR benchmark has failed cases but gotchas.md is empty or missing |

---

### Phase 5: Package & Ship

**Outcome**: Packaged `.skill` file + valid `manifest.json`.

**Constraints**:
- `manifest.json` must include all required fields:

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "trigger-aware description",
  "dependencies": {
    "scripts": ["python3", "node"],
    "mcp": [],
    "tools": []
  },
  "mode": "Scaffold|Production|Library",
  "skill_type": "Capability|Preference",
  "author": "...",
  "license": "MIT"
}
```

- Present `.skill` file and installation command to user:
```bash
npx skills add <author>/<repo>
# or copy to ~/.claude/skills/custom/<skill-name>/
```

---

## Communicating with the User

Pay attention to context cues. Briefly explain terms if uncertain. See [Communication Guide](references/communication-guide.md).

## Writing Style

- Use imperative form in instructions. Prefer `"Always use X"` over `"X is the recommended approach."` Directives beat trivia.
- Explain the **why** behind requirements — don't just say MUST. `"Use model X, model Y is deprecated and will return errors"` helps the agent generalize.
- Lead with examples: a 5-line code snippet beats a 5-paragraph explanation.
- Keep SKILL.md under 500 lines; push details to references. If a reference exceeds 500 lines, add a table of contents with line hints.
- Start with a draft, then improve with fresh eyes.
- Describe **goals and constraints**, not step-by-step procedures. See [Goal vs Procedure](references/goal-vs-procedure.md).
- Avoid overfitting: don't add "fiddly" changes that only pass your three test prompts. Write skills that work across millions of invocations.
- Research shows longer, more comprehensive instructions with too much context actually hurt performance. Keep it lean.

## Boundary Conditions & Fallbacks

| Scenario | Trigger | Fallback Action |
|---|---|---|
| User intent unclear / contradictory | Phase 1 capture fails | Ask clarifying questions (max 2 rounds). If still unclear, suggest Scaffold mode with minimal scope. |
| Skill already exists (name collision) | Phase 1 or 2 | Alert user, offer to iterate existing skill instead of creating new. |
| Reference file missing or unreadable | Phase 1 scan | Skip scan, warn user, continue with reduced context. Do NOT fail silently. |
| Eval workspace already exists | Phase 2 scaffold | Reuse and warn, or ask user to delete/backup. |
| Eval run fails / timeouts | Phase 3 iteration | Mark as `failed` in benchmark, explain to user, suggest retry with simpler prompts or manual review. |
| Gate script missing or errors | Phase 4 harden | Report script failure, skip gate, flag in summary. Do NOT claim gate passed. |
| Retirement check inconclusive | Phase 3 retirement criteria | Present ambiguous evidence, recommend human judgment. Default to **keep** unless evidence is strong. |
| User rejects all mode suggestions | Phase 1 Go/NoGo < 2 or user disagrees with assessment | Present alternatives (script, alias, prompt template). Do NOT force Scaffold as fallback — respect user's choice to not build a skill. |
| Manifest packaging fails | Phase 5 `manifest.json` invalid or `.skill` build errors | Report specific validation errors, suggest fixes, remain in Phase 4 until resolved. Do NOT ship broken package. |

## Output Contract

Unless the user asks otherwise, produce:

1. A working skill directory
2. A trigger-aware `SKILL.md`
3. Aligned `agents/interface.yaml`
4. Optional `references/`, `scripts/`, `evals/`, `reports/`, `manifest.json`
5. A short summary of boundary, exclusions, gates, and next steps

## Reference Map

- [Iteration Workflow](references/iteration-workflow.md)
- [Operating Modes](references/operating-modes.md)
- [QA Ladder](references/qa-ladder.md)
- [Resource Boundaries](references/resource-boundaries.md)
- [Governance Model](references/governance.md)
- [Skill Archetypes](references/skill-archetypes.md)
- [Skill Types](references/skill-types.md) — Capability vs Preference classification
- [Description Craft](references/description-craft.md) — Writing descriptions that trigger accurately
- [Goal vs Procedure](references/goal-vs-procedure.md) — Designing for outcomes, not steps
- [Gate Selection](references/gate-selection.md)
- [Non-Skill Decision Tree](references/non-skill-decision-tree.md)
- [Trigger & Eval Playbook](references/eval-playbook.md)
- [Skill Engineering Method](references/skill-engineering-method.md)
- [Communication Guide](references/communication-guide.md)
- [Reference Scan Strategy](references/reference-scan.md)
- [Gotchas Template](references/gotchas-template.md) — Template for recording failure modes
- [Content Quality](references/anthropic-content-quality.md) — Anthropic content quality checklist

## Scripts Map

| Script | Phase | Purpose |
|--------|-------|---------|
| `scripts/init_skill.py` | 2 | Scaffold a new skill directory from archetype |
| `scripts/run_eval_suite.py` | 3 | Execute with-skill and baseline evals in parallel |
| `scripts/validate_skill.py` | 4 | Pre-gate structural validation |
| `scripts/trigger_eval.py` | 4 | Measure description trigger accuracy |
| `scripts/diff_eval.py` | 3 | Compare with-skill vs baseline outputs |
| `scripts/build_confusion_matrix.py` | 3 | Aggregate eval results across iterations |
| `scripts/gotchas_check.py` | 4 | Verify gotchas.md exists, is non-empty, and every NOT-instruction in SKILL.md has a corresponding gotcha entry |
