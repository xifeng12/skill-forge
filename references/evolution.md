# Darwin-Style Skill Evolution

After a skill passes gates and initial evaluation, use the darwin-style evolution loop to continuously improve it.

## Evolution Loop Overview

The evolution loop implements a ratchet mechanism: score can only go up, each round either improves the skill or cleanly reverts.

## Evolution Process


1. **Score Current Skill**
- Run baseline scoring using 8-dimension weighted evaluation
- Use sub-agent blind evaluation to avoid bias
- Record score in evolution history

2. **Identify Improvement Target**
- Find lowest-scoring dimension
- Generate one targeted improvement suggestion

3. **Apply Improvement**
- Edit SKILL.md with targeted change
- Git commit the change

4. **Re-score and Decide**
- Spawn sub-agent for blind re-scoring
- If score improved: keep commit
- If score decreased: git revert

5. **Repeat Until Target**
- Continue until target score reached or max rounds hit
- Pause every N rounds for human confirmation

## Example-Driven Mode

When the user provides positive, negative, or fix examples, run example-driven iteration before the score-driven loop. See [Example-Driven Iteration](iteration-examples.md).

**Combined flow:**

```
Examples available?
  ├─ Yes → Extract behavior deltas → Apply one delta per commit
  │         → Validate against holdout slice → Then run score-driven evolution
  └─ No  → Run score-driven evolution directly
```

**Priority rule:** Example-driven changes take precedence because they represent real observed behavior. Score-driven changes are general quality improvements.

## Evolution Scripts

- `scripts/evolve_loop.py` - Main evolution loop orchestrator
- `scripts/score_skill.py` - 8-dimension scoring with sub-agent
- `scripts/ratchet.py` - Keep/revert mechanism

## Evolution Configuration

See `agents/interface.yaml` for evolution settings:
- `auto_rounds`: Rounds to run automatically before pause
- `target_score`: Target score percentage (default: 80%)
- `max_rounds`: Maximum rounds before stopping
- `confirm_mode`: "batch" | "each" | "auto"
- `stagnation_limit`: Stop if no improvement for N rounds

## 8-Dimension Scoring

All dimensions use the same max points. Archetypes differ by which dimensions apply.

| Dimension | Max | Scaffold | Production | Library | Description |
|-----------|-----|----------|------------|---------|-------------|
| trigger_accuracy | 15 | ✅ | ✅ | ✅ | Description matches actual triggers |
| execution_reliability | 20 | ✅ | ✅ | ✅ | Correct outputs on test prompts |
| boundary_clarity | 10 | ✅ | ✅ | ✅ | Clear exclusions and scope |
| context_efficiency | 10 | ✅ | ✅ | ✅ | Appropriate size, no bloat |
| documentation | 10 | ❌ | ✅ | ✅ | Complete references and examples |
| error_handling | 10 | ❌ | ✅ | ✅ | Graceful edge case handling |
| portability | 10 | ❌ | ❌ | ✅ | Cross-environment compatibility |
| governance_maturity | 15 | ❌ | ❌ | ✅ | Ownership, versioning, regression tests |
| **Max Total** | 100 | **55** | **75** | **100** |

**Pass Thresholds:**
- Scaffold: 35/55 (64%)
- Production: 52/75 (69%)
- Library: 75/100 (75%)

See [Scoring Rubric](scoring-rubric.md) for detailed criteria per dimension.

## Ratchet Mechanism

The ratchet ensures:
- Score can only increase
- Each round either improves or reverts cleanly
- No accumulation of partial regressions

## Usage

```bash
# Run evolution loop on a skill
python scripts/evolve_loop.py /path/to/skill

# Check ratchet status
python scripts/ratchet.py status --skill-dir /path/to/skill

# Manual keep/revert
python scripts/ratchet.py keep --skill-dir /path/to/skill --score 75
python scripts/ratchet.py revert --skill-dir /path/to/skill
```

## Evolution Output

- `reports/evolution_history.json` - Full evolution history with scores
- `reports/.ratchet_state.json` - Current ratchet state
- Git commits with "evolve:" prefix for each change
