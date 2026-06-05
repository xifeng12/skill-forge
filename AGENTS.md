# AGENTS.md — Skill-Forge Directory Constraints

> These rules apply specifically to `.opencode/skills/custom/skill-forge/`.
> They supplement and override the root `AGENTS.md` when there is conflict.
> Read this file before editing anything in this directory.

---

## Constraint 1: Meta-Skill Self-Coherence is Non-Negotiable

Skill-forge is a meta-skill: it teaches other skills how to be built. Therefore its own SKILL.md must **exemplify** the principles it preaches.

### Specific Checklist (Run Before Any Edit)

1. Read `references/goal-vs-procedure.md`. Extract its core constraint:
   - **"Provide Constraints, Not Procedures"**
   - **"Numbered steps for everything" is an Anti-Pattern**
   - The SKILL.md workflow should be read as **outcomes**, not rigid steps

2. Verify that any change to `SKILL.md` does **not** introduce:
   - Heavy numbered step sequences where goal-oriented constraints would suffice
   - "Step 1 / Step 2 / Step 3" language that prevents agent adaptation
   - Dictation of tool usage order where the agent should choose

3. If the change requires procedural precision (e.g., exact script invocation order), move it to `scripts/`, not `SKILL.md`.

**Blocker rule**: If a proposed edit violates Goal vs Procedure, the edit is blocked. Do not proceed. Report the conflict to the user.

### Self-Check Output Format

Before any edit to this directory, the agent must output a checklist in its response:

```
[AGENTS.md Self-Check for skill-forge]
[x] Read references/goal-vs-procedure.md
[x] Read STATE.md Design Decisions (Non-Negotiable) — verify proposed change does not trigger any forbidden effect
[x] Verified no numbered-step sequences introduced
[x] Verified no "Step 1 / Step 2 / Step 3" language
[x] Procedural precision moved to scripts/ (if applicable)
[x] Entrypoint size ≤ 300 lines (if SKILL.md changed)
[ ] Blockers found: <none or list>
```

**新增检查项说明**：`STATE.md Design Decisions` 包含经 v2 验证的否决清单（如"不加检查点"）。agent 必须确认：本次改动的**效果**（agent 会被如何约束）是否触发了清单中的任何"禁止行为"——而不仅仅是检查形式是否用了 Constraint 语言。

> Rationale: Makes the Self-Coherence check observable and verifiable by the user, not just an internal mental step. `[skill-forge/Constraint 1]`

---

## Constraint 2: No Blind Import of External Meta-Skills

When evaluating external repositories (e.g., `yao-meta-skill`):

1. Do **not** copy their structure wholesale into local skill-forge.
2. External skills have different design philosophies (e.g., "rigor grows faster than context cost" vs local "lightweight execution").
3. Any borrowed pattern must pass the Four-Gate Test from `references/pattern-extraction-doctrine.md` (if present) or be manually evaluated for:
   - Recurrence: does the pattern appear in multiple sources?
   - Generativity: can it guide a new case, not just explain the original?
   - Distinctiveness: is it more specific than generic advice?
   - Boundary: does it have a known limit / when not to apply?

4. After identifying a desirable pattern, produce a **read-only adoption report** first. Wait for user "do it" before touching files.

---

## Constraint 3: Baseline Evaluation Required for Structural Changes

Any structural change to skill-forge (workflow reorganization, new Phase, new gate) must be preceded by:

1. Running `darwin-skill` baseline assessment (if available) on current state.
2. Documenting the baseline score and weakest dimension.
3. Making only one dimension change per iteration.
4. Re-running assessment after the change.
5. **Ratchet rule**: only keep the change if the new score is strictly higher.

If darwin-skill is unavailable, use `scripts/self_assess.py` or manual rubric scoring against:
- Method Depth, Context Discipline, Toolchain, Eval Rigor, Governance, Onboarding, Local Reliability

---

## Constraint 4: Entrypoint Size Budget

- `SKILL.md` must stay under **300 lines**.
- If adding new sections (e.g., First-Turn Style, Intent Dialogue), something else must be pushed to `references/` to stay within budget.
- Exception: only if the new section is critical for routing accuracy.

---

## Constraint 5: Chinese Language Sensitivity

If adding Chinese-language content (e.g., opening patterns, tone guidance):

1. It must feel natural, not translated-from-English.
2. Avoid mechanical terms like "archetype", "gate", "package" in the first breath.
3. Reference `references/intent-dialogue.md` (if present) for tone templates.
4. Do **not** add Chinese content if the rest of the skill is English-only — inconsistency hurts routing.

---

## Constraint 6: Script Addition Rules

New scripts in `scripts/` are allowed only when:

1. They perform deterministic logic that repeats across skill creations.
2. They are invoked by name in `SKILL.md` or `references/`.
3. They do not duplicate functionality of existing scripts (check before adding).
4. They include a docstring explaining when and why to use them.

Forbidden: scripts that are "nice to have" but never referenced by the skill's workflow.

---

## Constraint 7: State File Awareness

Before taking any action in this directory, read `STATE.md` to understand the current task state:

- If `STATE.md` exists and shows an **incomplete** task, resume from the listed "Next Step".
- If `STATE.md` is missing or shows **no active task**, proceed normally.
- After completing a significant step, update `STATE.md` to reflect progress.

> Rationale: Ensures session continuity without relying on agent memory. `[Rule 10]`

---

## Session Continuity Note

If you are a new agent reading this file:

- This skill was last evaluated by darwin-skill with baseline score **86.7** (commit `eaf2820`).
- The previous weakest dimension was **Self-Coherence (dim7)** at 4.0, now improved to 7.5.
- Do not attempt to "fix" remaining issues by rewriting references/ — fix the SKILL.md body to align with references/.
- Previous failed experiment: merging 6 external reference files + 3 scripts without user confirmation. Result: user requested revert. Do not repeat.
- Active optimization branch: `auto-optimize/20260502-skill-forge`. Check `STATE.md` for current progress.
