# Iteration Workflow

The core loop of skill creation — combining structured design with human-in-the-loop review.

## Step 1: Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow to capture.

1. What should this skill enable the agent to do?
2. When should this skill trigger? (user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases? Skills with objectively verifiable outputs benefit from test cases. Subjective outputs (writing, art) often don't.

## Step 2: Interview and Research

Ask about edge cases, input/output formats, example files, success criteria, dependencies. Don't write test prompts until this is ironed out.

Check available MCPs — research via subagents if possible.

## Step 3: Write the SKILL.md

Based on the interview, fill in:

- **name**: Skill identifier
- **description**: When to trigger, what it does. Include both what the skill does AND specific contexts. Be "pushy" — e.g., "Make sure to use this skill whenever the user mentions X, even if they don't explicitly ask for Y."
- **the rest of the skill**: instructions, patterns, references.

## Step 4: Create Test Cases

Save to `evals/evals.json`. Don't write assertions yet — just the prompts.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

## Step 5: Run Test Cases

Spawn two subagents per test case in the same turn — one with the skill, one without (baseline).

**With-skill run:**
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Save outputs to: <workspace>/iteration-N/eval-ID/with_skill/outputs/

**Baseline run:**
- New skill: no skill at all. Save to `without_skill/outputs/`.
- Improving existing: snapshot old version, point baseline at it. Save to `old_skill/outputs/`.

Write `eval_metadata.json` for each test case.

## Step 6: While Runs Complete, Draft Assertions

Draft quantitative assertions. Explain them to the user. Good assertions are objectively verifiable with descriptive names. Subjective skills are better evaluated qualitatively.

Update `eval_metadata.json` and `evals/evals.json` with assertions.

## Step 7: Grade, Aggregate, Launch Viewer

1. **Grade** — read `agents/grader.md`, evaluate each assertion. Save to `grading.json`.
2. **Aggregate** — run benchmark aggregation.
3. **Analyst pass** — surface patterns the aggregate might hide.
4. **Launch viewer** with qualitative outputs and quantitative data:
   ```bash
   python <skill-forge-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N --skill-name <name> \
     --benchmark <workspace>/iteration-N/benchmark.json
   ```
   For iteration 2+, pass `--previous-workspace <workspace>/iteration-N-1`.
5. **Tell the user** — two tabs: Outputs (per-case feedback) and Benchmark (quantitative stats).

## Step 8: Read Feedback & Improve

When user says they're done, read `feedback.json`. Empty feedback = looks fine. Focus improvements on cases with specific complaints.

### How to Think About Improvements

1. **Generalize from feedback.** These examples will be used across many prompts. Don't overfit.
2. **Keep the prompt lean.** Remove things not pulling their weight.
3. **Explain the why.** Use theory of mind. Reframe rigid MUSTs into reasoning.
4. **Look for repeated work.** If all test cases write similar scripts, bundle them.

## Step 9: Repeat

1. Apply improvements
2. Rerun all test cases into new iteration directory
3. Launch viewer with `--previous-workspace`
4. Wait for feedback
5. Repeat until happy, feedback empty, or no more progress

## Blind Comparison (Optional)

For rigorous A/B between two versions: read `agents/comparator.md`.

## Description Optimization

After the skill is done, optimize the description for better triggering:

1. Generate 20 eval queries (8-10 should-trigger, 8-10 should-not-trigger)
2. Review with user using eval template
3. Run optimization loop:
   ```bash
   python scripts/optimize_description.py --eval-set <path> --skill-path <path> --max-iterations 5
   ```
4. Apply `best_description` to SKILL.md frontmatter
