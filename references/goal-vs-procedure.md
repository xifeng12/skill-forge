# Goal vs Procedure: Designing Skills for Outcomes

A common mistake in creating skills is turning them into step-by-step workflows. When you dictate every step, you take away the agent's ability to adapt, recover from errors, or find better approaches.

## The Problem with Procedures

**Example — Bad (Procedural)**:
```
Step 1: Read the config file
Step 2: Find the database URL
Step 3: Update the port number
Step 4: Write the file back
```

Problems:
- The agent can't skip steps if they're unnecessary
- Can't recover if step 2 fails (e.g., file doesn't exist)
- Can't apply the skill to similar but non-identical situations
- Wastes context on rigid sequencing

**Example — Good (Goal-Oriented)**:
```
Update the database port in the config file to the value specified by the user.
```

Advantages:
- Agent chooses the best path based on context
- Adapts to variations (different config formats, missing fields)
- Leaves room for error recovery
- Uses context efficiently

## Provide Constraints, Not Procedures

**Example — Bad (Procedural)**:
```
Step 1: Create a branch
Step 2: Make the change
Step 3: Run tests
Step 4: Open a PR
```

**Example — Good (Constraint-Based)**:
```
Always run tests before opening a PR. Never push directly to main.
```

Constraints tell the agent **what must be true** about the outcome. Procedures tell the agent **exactly how to move**. Constraints preserve flexibility; procedures remove it.

## When Procedures Are Actually Needed

If exact steps matter, and doing step 3 before step 2 breaks everything, that's not a skill problem — it's a **scripting problem**.

| Situation | Solution |
|-----------|----------|
| Order matters, skipping steps breaks things | Write a script in `scripts/`, call it from the skill |
| Need deterministic execution | Use a script or external tool |
| Complex multi-step with state | Use Pipeline archetype with explicit gates |
| Agent needs freedom to adapt | Use goal-oriented constraints in SKILL.md |

## Writing Goal-Oriented Instructions

### 1. Start with the Outcome

```
❌ "Step 1: Read the file. Step 2: Parse the JSON."
✅ "Extract the user email from the provided JSON file."
```

### 2. Provide Guardrails, Not Guard Posts

```
❌ "First check if the file exists. Then open it. Then read line by line."
✅ "Return an error if the file is missing or empty. Handle malformed JSON gracefully."
```

### 3. Explain the Why for Constraints

When a rule matters, say why. This helps the agent generalize:

```
✅ "Use model X for this task. Model Y is deprecated and will return errors as of v2.1."
```

### 4. Use Directives

Research shows longer, more comprehensive instructions with too much context actually hurt performance. Be concise:

```
❌ "The Interactions API is the recommended approach for handling user interactions in this system."
✅ "Always use interactions.create() for creating new interaction records."
```

The first is trivia the agent won't act on. The second is an instruction.

### 5. Lead with Examples

A 5-line code snippet beats a 5-paragraph explanation:

```markdown
## Example: Correct API Call

```python
response = client.interactions.create(
    user_id="123",
    action="click",
    target="button-submit"
)
```
```

## Applying This to Skill-Forge Itself

Even skill-forge's workflow should be read as **outcomes**, not rigid steps:

- **Capture intent** → Understand what the user needs, not fill a form
- **Draft the skill** → Produce a working skill, not follow a template
- **Evaluate** → Verify the skill works, not run a specific script

The references and scripts are tools. The agent decides when and how to use them based on the goal.

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Hurts |
|--------------|--------------|
| Numbered steps for everything | Prevents adaptation and error recovery |
| Overfitting to test cases | Works for 3 test prompts, fails on the 4th |
| Including trivia | "The API was introduced in v1.2" — agent won't act on this |
| Dictating tool usage order | If order matters, it's a script, not a skill |
| Fiddly micro-instructions | "Use exactly 2 spaces for indentation in generated code" — preference belongs in references/ |

## Checklist

- [ ] Can the agent achieve the goal through multiple valid paths?
- [ ] Are there explicit constraints for what must be true about the output?
- [ ] Is the "why" explained for non-obvious constraints?
- [ ] Are there examples for complex patterns?
- [ ] Would a script be better for any part of this workflow?
