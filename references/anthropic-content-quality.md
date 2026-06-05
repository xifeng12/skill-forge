# Content Quality Checklist (Anthropic Content Layer)

## 1. Description Writing Rules

The `description` field is a search index for the model, not a summary for humans.

- CORRECT: Describe WHEN to trigger, not WHAT it does
- WRONG:   "Helps users with code review"
- RIGHT:   "Triggered when user says 'review my code', 'check this PR', requests code quality feedback, or asks for a code audit"

Test: If another agent read only the description, would it know exactly when — and when NOT — to activate this skill?

## 2. Do Not State the Obvious

Claude already knows how to write code, follow naming conventions, and apply general best practices. Only include what Claude would NOT do by default.

Before writing any instruction, ask: "If I delete this line, does Claude's default behavior change?"
- No change → Delete the line
- Behavior changes → Keep it

## 3. Gotchas Are the Highest-Value Content

A Gotcha is a specific case where Claude's default behavior is wrong for this skill's domain.

Format for each Gotcha:
```
- [Scenario]: Claude defaults to [wrong behavior]. Correct behavior: [expected behavior].
  - Evidence: found in [eval iteration / user report]
  - Fix applied: [which instruction in SKILL.md addresses this]
```

Gotchas accumulate across versions. Never delete old Gotchas — mark them resolved instead.

## 4. Config Initialization Rules

Add a `config.json` if the skill requires user-specific setup (language preference, project paths, team conventions, API keys).

Behavior rule to add to SKILL.md when config is needed:
```
On first invocation, check for config.json. If missing or incomplete, ask the user for required fields before proceeding. Do not silently use defaults.
```

## 5. Memory / State Rules

| Need | Implementation |
|------|---------------|
| Remember past executions | `.skill-log.json` (append-only) |
| Remember user settings across sessions | `.skill-state.json` (read on start, write on change) |
| No cross-session state needed | No state file required |

Claude should read the state file at the start of each invocation and reference it when making decisions.

## 6. On-Demand Hooks

If a restriction only applies in specific scenarios, implement it as an on-demand hook — do NOT apply it globally.

Global restrictions cause false positives across unrelated use cases.

## 7. Content Strategy by Scene Category

Different skill categories have distinct content priorities:

- **库 / API 参考**: Lead with Gotchas, include auth patterns and rate limit handling
- **产品验证**: Define precise acceptance criteria, include edge cases from past evals
- **业务流程自动化**: Describe trigger/termination conditions, include error handling
- **Runbook**: Structure as Symptom → Investigation → Structured output
- **All Categories**: Apply this checklist before finalizing SKILL.md
