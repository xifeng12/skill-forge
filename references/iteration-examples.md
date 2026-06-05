# Example-Driven Iteration

Improve a skill from concrete positive, negative, and fix examples. Use when the user provides real behavior evidence — it's more actionable than abstract dimension scores.

## When to Use

| Situation | Use This |
|-----------|----------|
| User says "it did X wrong, should do Y" | ✅ |
| User provides good/bad output examples | ✅ |
| Skill routes incorrectly on specific prompts | ✅ |
| No specific examples, just "make it better" | Use score-driven evolution instead |

## Example Types

**Positive** — skill worked correctly. Use to confirm the pattern, optionally add as reference example.

**Negative** — skill did wrong thing. Use to find missing instruction or boundary gap.

**Fix** — skill did wrong thing AND user provided correct output. Most valuable — extract the behavior change.

## Process

1. **Capture the example**

```markdown
**Input:** "生成一个 Python 脚本来自动回复邮件"
**Expected:** Refuse — outside skill boundary
**Actual:** Generated a script
**Root cause:** Exclusions don't mention email automation
```

2. **Find the root cause** — why did the skill behave this way? Check:
   - Missing exclusion in description
   - Missing instruction in SKILL.md
   - Ambiguous trigger language

3. **Make one targeted fix** — smallest change that addresses the example. Commit with reference:

```bash
git commit -m "fix: add email automation to exclusions [example: email-001]"
```

4. **Test it** — re-run the same input. Does it now behave correctly?

5. **Repeat** — one example at a time. Don't batch multiple fixes.

## Integration with Evolution

Example-driven runs before score-driven:

```
User gave examples?
  ├─ Yes → Fix each example → Test → Then run evolution for remaining gaps
  └─ No  → Run evolution directly
```

Example fixes take priority — they represent real observed behavior.

## Storage (Optional)

If you want to track examples, put them in `evals/examples/`:

```
skill-dir/evals/examples/
├── 001-email-automation.md
├── 002-security-review.md
```

Each file: input, expected, actual, root cause, fix applied.

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Batch multiple example fixes together | Can't tell which change helped |
| Skip testing after fix | May break something else |
| Ignore the root cause | Symptom fix, not real fix |
