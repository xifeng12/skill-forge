# Skill Types: Capability vs Preference

Skills fall into two fundamental categories with different lifecycles, design priorities, and retirement criteria.

## Capability Skills

**Definition**: Help the agent do something the base model can't do consistently or at all.

**Characteristics**:
- Bridge a capability gap (e.g., PDF form filling, complex data transformations)
- Often wrap external tools or APIs
- Become unnecessary as models improve
- Require evals to detect when the gap narrows

**Examples**:
- PDF manipulation (base models can't reliably edit PDFs)
- Video/audio processing (requires external tools)
- Complex spreadsheet calculations (requires formula execution)

**Lifecycle**:
```
Create → Heavy evals → Active use → Model improves → Re-eval → Retire if base model catches up
```

**Design Priority**:
- Exact tool usage instructions
- Error recovery patterns
- Output format specifications

**Retirement Condition**:
Run evals **without** the skill. If they pass, the model has absorbed the skill's value and the skill is no longer necessary. Retire it — especially true for capability skills.

## Preference Skills

**Definition**: Encode your specific workflow, style, or organizational conventions.

**Characteristics**:
- Capture team-specific processes (e.g., code review steps, document templates)
- Durable — don't become obsolete when models improve
- Need to stay in sync with actual processes
- Often higher maintenance in terms of content updates

**Examples**:
- Team code review checklist and style guide
- Company-specific document templates
- Personal note-taking conventions
- Brand voice guidelines for marketing copy

**Lifecycle**:
```
Create → Light evals → Active use → Process changes → Update skill → Continue
```

**Design Priority**:
- Clear constraints and boundaries
- Explain the **why** behind requirements
- Easy to update when process changes

**Retirement Condition**:
Retire when the encoded workflow is no longer used by the team. This is an organizational decision, not a model-capability decision.

## Quick Decision Tree

```
Is the skill doing something the base model fundamentally cannot do?
├─ Yes (needs tools, external APIs, deterministic execution)
│   → Capability Skill
│   → Plan for retirement as models improve
│   → Heavy evals to detect capability shifts
└─ No (organizing work, enforcing conventions, encoding preferences)
    → Preference Skill
    → Plan for maintenance as process evolves
    → Light evals, focus on constraint accuracy
```

## Implications for Design

### Capability Skills
- Invest heavily in **exact instructions** and **error handling**
- Monitor model releases for capability improvements
- Keep descriptions focused on the **technical gap**
- Design with retirement in mind — don't over-engineer durability

### Preference Skills
- Invest heavily in **explaining the why** behind conventions
- Make updates easy — use references/ for volatile content
- Keep descriptions focused on **workflow context**
- Design for longevity — these should outlast model versions

## Mixed Skills

Some skills blend both types. For example, a "deploy to AWS" skill is:
- **Capability** (needs AWS CLI, can't be done purely by reasoning)
- **Preference** (encodes your team's specific deployment conventions)

For mixed skills:
- Separate the capability layer (tool usage) from the preference layer (conventions)
- Put capability instructions in SKILL.md body
- Put preference conventions in references/
- Evaluate both aspects independently
