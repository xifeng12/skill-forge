# Skill Engineering Method

This doctrine defines the default method for turning messy workflow material into a reusable skill without bloating the entrypoint.

## Core Loop

1. Decide whether the request should become a skill at all.
2. Run a short intent dialogue to capture the real job, outputs, exclusions, and constraints.
3. Choose the smallest viable archetype.
4. Set one clear capability boundary.
5. Write and test the trigger description before expanding the body.
6. Write instructions that describe outcomes and constraints, not step-by-step procedures.
7. Add only the gates that match the risk.
8. Ship the first routeable package, then pick the three highest-value next iteration directions.
9. Package and govern the skill only as far as real reuse demands.

## Phase 1: Qualification

Promote a request into a skill only when at least one of these is true:

- the workflow will be reused
- the workflow is easy to route incorrectly
- deterministic scripts reduce repeated effort
- governance or portability matters

Reject skill creation when the request is only:

- explanation
- summary
- translation
- brainstorming
- documentation without agent execution
- a one-off answer with no reuse value

See [Non-Skill Decision Tree](non-skill-decision-tree.md).

## Phase 2: Intent Dialogue

Before deep authoring, ask only the questions that change the package design.

- what recurring job should the skill own
- what real inputs will users hand to it
- what outputs must it produce
- what near-neighbor requests should stay out of scope
- what constraints matter: privacy, naming, portability, governance, or local fit

See [Intent Dialogue](intent-dialogue.md).

## Phase 3: Archetype Selection

Choose the lightest archetype that fits the job.

- `Scaffold`: exploratory, personal, or short-lived
- `Production`: team-reused, quality-sensitive, but still compact
- `Library`: broad reuse, visible evidence, portability, and maintenance expectations
- `Governed`: organizationally sensitive or operationally critical; lifecycle and review are explicit

See [Skill Archetypes](skill-archetypes.md).

## Phase 4: Boundary Design

Every skill should answer four questions clearly:

- what recurring job does it own
- what outputs does it produce
- what near-neighbor requests should not route here
- what detail belongs outside `SKILL.md`

Boundary work comes before polishing prose.

## Phase 5: Reference Scan

Run a short benchmark pass before deep authoring.

- scan `3-5` reference objects at most
- prioritize external GitHub and official benchmark sources first
- use local files second, only for fit, privacy, and compatibility calibration
- choose from method, structure, execution, portability, and domain patterns
- extract only what improves reliability or clarity
- record what not to borrow so the new skill stays light

See [Reference Scan Strategy](reference-scan.md).

## Phase 6: Source Synthesis

For Production+ skills and integration/documentation skills, collect and verify input depth before authoring.

- gather sources from multiple channels with trust tiers
- record provenance in SOURCES.md
- build coverage matrix and identify gaps
- enforce depth gates before moving to authoring
- anchor design decisions to sources with evidence

See [Synthesis Path](synthesis-path.md).

## Phase 7: Trigger-First Authoring

Author the frontmatter `description` before expanding the body.

- start with the recurring job
- include the trigger actions that should route here
- include exclusions when confusion is plausible
- test the route before growing the file tree

Trigger quality is improved through:

- `trigger_eval.py`
- `optimize_description.py`
- blind holdout
- judge-backed blind holdout
- adversarial holdout
- route confusion

## Phase 8: Instruction Design

Write for outcomes, not procedures.

### The Principle

Agents are capable of planning, adapting, and recovering. When you dictate every step, you take away their ability to:

- adapt to unexpected inputs
- recover from errors
- find better approaches

### What To Do

**Describe the goal, not the path:**

- ❌ *"Step 1: Read the config file. Step 2: Find the database URL. Step 3: Update the port number. Step 4: Write the file back."*
- ✅ *"Update the database port in the config file to the value specified by the user."*

**Provide constraints, not workflows:**

- ❌ *"Step 1: Create a branch. Step 2: Make the change. Step 3: Run tests. Step 4: Open a PR."*
- ✅ *"Always run tests before opening a PR. Never push directly to main."*

### When To Write Scripts Instead

If the task is fragile — doing step 3 before step 2 breaks everything — that's not a skill problem. Write a script and wrap it with a Tool Wrapper skill.

### Decision Rule

| Situation | Approach |
|-----------|----------|
| Outcome matters, path can vary | Write constraints in skill |
| Exact sequence matters | Write a script |
| Both matter | Script for sequence, skill for constraints |

## Phase 9: Gate Selection

Add gates by risk, not by habit.

- low-risk scaffolds: validate structure and context size
- production skills: trigger eval plus resource-boundary checks
- library skills: description optimization, route confusion, packaging checks
- governed skills: governance scoring, lifecycle metadata, regression history

See [Gate Selection](gate-selection.md).

## Phase 10: First Iteration Philosophy

The first package is a routeable baseline, not the final answer.

- improve trigger and exclusions before growing prose
- add one execution asset before adding many documents
- surface the three highest-value next moves so authors do not expand in every direction at once
- prefer the smallest step that increases reliability more than context cost

See [Iteration Philosophy](iteration-philosophy.md).

## Phase 11: Promotion

A candidate route or package is promotable only when:

- visible holdout does not regress
- blind holdout does not regress
- judge-backed blind holdout does not regress
- adversarial holdout does not regress
- route confusion stays clean
- context and governance gates still pass

See [Promotion Policy](../evals/promotion_policy.md).

## Design Principle

The method is only correct if rigor grows faster than context cost. If a new check or document makes the skill heavier without making it more reliable, remove or relocate it.
