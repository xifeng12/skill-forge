# Description Craft

How to write skill descriptions that trigger accurately — based on real-world eval data showing **up to 50% performance improvements** from description changes alone.

## The Trigger Mechanism

The description in your SKILL.md frontmatter is the **primary trigger mechanism**. The agent decides whether to load your skill based on this single field. Everything else — the body, references, scripts — only loads **after** the description triggers.

This means:
- A vague description → skill never fires → all your work is invisible
- A too-broad description → skill fires on every request → noise and context waste

## The When + Exclusions Rule

A good description answers two questions: **when should the agent load this skill, and when should it not.**

The "what" (what the skill does) matters less than the "when" (what triggers it) and the exclusions (what it must NOT hijack). A description that says "Helps with PDF editing" is ambiguous. A description that says "Load when filling PDF forms or extracting PDF text. Do NOT use for general document editing or spreadsheets." is precise.

### Bad Examples

- `"Helps with documents"` — When exactly? What kind?
- `"Code assistant"` — Will hijack every coding request
- `"Create, edit, and analyze .docx files."` — What + no exclusions; fires on any .docx mention even when not needed

### Good Examples

- `"Load when working with .docx files: tracked changes, comments, formatting, or text extraction. Do NOT use for spreadsheets or plain text."`
- `"Load when writing code that calls the Gemini API. Do NOT use for other cloud APIs or general coding tasks."`
- `"Load when deploying Python services to AWS Lambda or GCP Cloud Functions. Do NOT use for containerized or static hosting deployments."`

## Be Specific, Not Pushy

Specificity beats cleverness. The agent needs to pattern-match user intent against your description.

| Aspect | Vague | Specific |
|--------|-------|----------|
| Action | "Helps with" | "Create, edit, and analyze" |
| Domain | "documents" | ".docx files" |
| Triggers | "when needed" | "Use for tracked changes, comments, formatting, or text extraction" |
| Exclusions | (missing) | "Do NOT use for general document editing, spreadsheets, or plain text files" |

## Include Exclusions

Explicitly state when the skill should **not** fire. This prevents hijacking adjacent requests.

```
"Use when working with PDF files. Do NOT use for general document editing, spreadsheets, or plain text files."
```

Without exclusions, a description like `"Use for any coding task"` will hijack every request.

## Use Directives, Not Descriptions

The agent responds better to instructions than to trivia:

- ❌ `"The Interactions API is the recommended approach."` — Trivia the agent won't act on
- ✅ `"Always use interactions.create() for creating new interaction records."` — Direct instruction

## Lead with Examples

A 5-line code snippet beats a 5-paragraph explanation. When the skill involves code or structured output, include a minimal example in the description or early in the body.

## Test Both Directions

For every skill, you need **both**:

- **Should-trigger cases** (8-10): Different phrasings of the same intent
- **Should-not-trigger cases** (8-10): Near-misses that share keywords but need something different

Without testing the negative cases, you'll optimize the skill in one direction and create a hijacking problem.

## Optimization Workflow

1. Draft description with what + when + exclusions
2. Generate 20 eval queries (mixed should/should-not)
3. Run trigger eval: `scripts/trigger_eval.py`
4. If accuracy < 90%, iterate description
5. Run description optimization suite: `scripts/optimize_description.py` (up to 5 iterations)
6. Apply `best_description` to SKILL.md

## Key Metrics

- **Trigger precision**: % of should-trigger cases that actually trigger
- **Trigger recall**: % of should-not-trigger cases that correctly do NOT trigger
- **Target**: Both >= 90% for Production/Library modes

## Gotcha: trigger_eval.py Limitations

`scripts/trigger_eval.py` uses lexical semantic matching, not actual LLM routing. This has concrete consequences:

- **Chinese text is unsupported.** The `normalize()` function strips non-ASCII characters, collapsing "优化skill" → "skill". All Chinese-only prompts score near zero.
- **Phrase matching is literal.** "build a skill" won't match "building a skill" unless both variants are registered as phrases.
- **The tool measures concept coverage, not routing.** A high score means the description's concepts overlap with the prompt's concepts — not that the LLM router would actually load the skill.

**When to trust it**: Relative comparisons on English-only prompt sets. A description that scores higher on the same test set likely has better concept coverage.

**When to distrust it**: Absolute precision/recall claims. A "90% recall" on this tool does not guarantee 90% recall from the actual router.

**When to bypass it**: Chinese-heavy environments. Instead, run actual LLM routing tests — send prompts to the router with and without the skill loaded, and measure whether it triggers correctly.
