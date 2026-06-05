# Evolution Config

Configuration for the darwin-style optimization loop.

## Configuration File

Location: `agents/interface.yaml`

```yaml
evolution:
  # How many rounds to run automatically before pausing for confirmation
  auto_rounds: 3
  
  # Target score (percentage). Stop when reached.
  target_score: 80
  
  # Maximum rounds before forcing stop
  max_rounds: 10
  
  # Confirmation mode
  # - "batch": Pause every N rounds (auto_rounds)
  # - "each": Pause after every round
  # - "auto": Run fully autonomous until target or max_rounds
  confirm_mode: "batch"
  
  # Stop if no improvement for N consecutive rounds
  stagnation_limit: 2
  
  # Git commit message prefix
  commit_prefix: "evolve:"
```

## Modes Explained

### batch (Default)

Run N rounds automatically, then pause for human review.

```
Round 1 → Round 2 → Round 3 → [PAUSE: show diff + scores] → User confirms → Continue...
```

Best for: Most use cases. Balance between autonomy and control.

### each

Pause after every single round.

```
Round 1 → [PAUSE] → Round 2 → [PAUSE] → ...
```

Best for: Critical skills, early iterations, or when learning the system.

### auto

Run fully autonomous until target score or max_rounds reached.

```
Round 1 → Round 2 → ... → Round N → [DONE: final report]
```

Best for: Batch optimization of many skills, trusted workflows.

## Round Structure

Each round consists of:

```
1. Score current SKILL.md (sub-agent blind evaluation)
2. Identify lowest-scoring dimension
3. Generate one targeted improvement
4. Apply edit to SKILL.md
5. Git commit
6. Re-score (sub-agent blind evaluation)
7. If score improved: keep commit
8. Else: git revert
9. Record round result
```

## Stopping Conditions

| Condition | Action |
|-----------|--------|
| Target score reached | Stop, show final report |
| Max rounds reached | Stop, show final report |
| Stagnation limit hit | Stop, suggest manual review |
| User interrupts | Stop, preserve current state |

## Output Files

### reports/evolution_history.json

```json
{
  "skill_name": "my-skill",
  "archetype": "Production",
  "start_time": "2024-01-15T10:30:00Z",
  "end_time": "2024-01-15T10:45:00Z",
  "config": {
    "auto_rounds": 3,
    "target_score": 80,
    "confirm_mode": "batch"
  },
  "rounds": [
    {
      "round": 1,
      "score_before": 54,
      "score_after": 61,
      "dimension_targeted": "error_handling",
      "improvement": "Added try-catch for file operations",
      "kept": true
    },
    {
      "round": 2,
      "score_before": 61,
      "score_after": 58,
      "dimension_targeted": "documentation",
      "improvement": "Expanded reference section",
      "kept": false,
      "reason": "Score decreased, reverted"
    }
  ],
  "final_score": 72,
  "total_rounds": 5,
  "improvements_kept": 4,
  "improvements_reverted": 1
}
```

## Human-in-the-Loop Prompts

### Batch Mode Pause

```
=== Evolution Pause ===

Skill: my-skill
Rounds completed: 3

Round 1: 54 → 61 (+7) ✓ Kept
  - Targeted: error_handling
  - Change: Added try-catch for file operations

Round 2: 61 → 58 (-3) ✗ Reverted
  - Targeted: documentation
  - Change: Expanded reference section

Round 3: 61 → 67 (+6) ✓ Kept
  - Targeted: boundary_clarity
  - Change: Added explicit exclusions

Current score: 67/75 (89%)
Target: 80%

[1] Continue (3 more rounds)
[2] Stop and review
[3] Adjust target score
[4] Show full diff
```

### Final Report

```
=== Evolution Complete ===

Skill: my-skill
Archetype: Production

Initial score: 54/75 (72%)
Final score: 72/75 (96%)
Improvement: +18 points

Rounds: 7 total
  - Kept: 5
  - Reverted: 2

Key improvements:
  1. error_handling: 5 → 9 (+4)
  2. boundary_clarity: 8 → 10 (+2)
  3. documentation: 6 → 9 (+3)
  4. trigger_accuracy: 12 → 14 (+2)

Files changed:
  - SKILL.md
  - references/error-handling.md (new)

Evolution history saved to: reports/evolution_history.json
```

## Best Practices

1. **Start with batch mode** until you trust the system.
2. **Set realistic targets** (80% is usually sufficient).
3. **Review stagnation** - if stuck, the skill may need manual intervention.
4. **Check reverted rounds** - they reveal what didn't work.
5. **Commit history is preserved** - you can always rollback manually.
