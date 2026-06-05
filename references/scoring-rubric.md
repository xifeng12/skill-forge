# Scoring Rubric

Unified 8-dimension scoring with archetype-specific applicability.

## Principle

All archetypes use the same 8 dimensions. Dimensions are marked as applicable (✅) or not applicable (❌) per archetype. The max_possible varies by archetype.

## Dimension Definitions

### Core Dimensions (All Archetypes)

| Dimension | Max | Description |
|-----------|-----|-------------|
| trigger_accuracy | 15 | Does description match actual triggers? Precision and recall. |
| execution_reliability | 20 | Does the skill produce correct outputs on test prompts? |
| boundary_clarity | 10 | Are exclusions and scope clearly defined? |
| context_efficiency | 10 | Is the skill appropriately sized? No bloat. |

### Extended Dimensions (Production / Library)

| Dimension | Max | Description |
|-----------|-----|-------------|
| documentation | 10 | Are references, examples, and guides complete? |
| error_handling | 10 | Does the skill handle edge cases gracefully? |

### Governance Dimensions (Library Only)

| Dimension | Max | Description |
|-----------|-----|-------------|
| portability | 10 | Can the skill work across different environments? |
| governance_maturity | 15 | Ownership, versioning, regression history. |

## Weight by Archetype

### Scaffold (Personal)

```
Total: 55 points (core only)

trigger_accuracy:     15
execution_reliability: 20
boundary_clarity:      10
context_efficiency:    10

Pass threshold: 35/55 (64%)
```

### Production (Team)

```
Total: 75 points (core + extended)

trigger_accuracy:     15
execution_reliability: 20
boundary_clarity:      10
context_efficiency:    10
documentation:         10
error_handling:        10

Pass threshold: 52/75 (69%)
```

### Library (Infrastructure)

```
Total: 100 points (all dimensions)

trigger_accuracy:     15
execution_reliability: 20
boundary_clarity:      10
context_efficiency:    10
documentation:         10
error_handling:        10
portability:           10
governance_maturity:   15

Pass threshold: 75/100 (75%)
```

## Scoring Criteria per Dimension

### trigger_accuracy (15)

| Score | Criteria |
|-------|----------|
| 13-15 | Description triggers on all relevant prompts, rejects all irrelevant. No confusion. |
| 10-12 | Triggers correctly on most prompts. Minor false positives or false negatives. |
| 7-9 | Some routing confusion. Needs description tuning. |
| 0-6 | Frequent misrouting. Description does not match behavior. |

### execution_reliability (20)

| Score | Criteria |
|-------|----------|
| 18-20 | All test prompts produce correct, complete outputs. |
| 14-17 | Most outputs correct. Minor issues on edge cases. |
| 10-13 | Inconsistent outputs. Needs workflow fixes. |
| 0-9 | Outputs frequently wrong or incomplete. |

### boundary_clarity (10)

| Score | Criteria |
|-------|----------|
| 9-10 | Exclusions explicitly listed. Scope unambiguous. |
| 7-8 | Boundaries mostly clear. Minor ambiguity. |
| 4-6 | Boundaries implied but not explicit. |
| 0-3 | No boundary definition. Unclear when to use. |

### context_efficiency (10)

| Score | Criteria |
|-------|----------|
| 9-10 | Minimal context for the job. No bloat. References used well. |
| 7-8 | Slightly verbose but acceptable. |
| 4-6 | Bloated. Could be trimmed significantly. |
| 0-3 | Excessive context. Major optimization needed. |

### documentation (10)

| Score | Criteria |
|-------|----------|
| 9-10 | Complete references, examples, and usage guide. SOURCES.md present for Library skills. |
| 7-8 | Good documentation with minor gaps. SOURCES.md present for Production (optional but nice). |
| 4-6 | Basic documentation. Needs expansion. |
| 0-3 | Missing or inadequate documentation. |

**Note:** SOURCES.md is required for Library, recommended for Production, optional for Scaffold.

### error_handling (10)

| Score | Criteria |
|-------|----------|
| 9-10 | Graceful handling of all edge cases. Clear error messages. |
| 7-8 | Handles most edge cases. Minor gaps. |
| 4-6 | Basic error handling. Needs improvement. |
| 0-3 | No error handling. Fails on edge cases. |

### portability (10)

| Score | Criteria |
|-------|----------|
| 9-10 | Works across environments. No hardcoded paths. Clean dependencies. |
| 7-8 | Mostly portable. Minor environment assumptions. |
| 4-6 | Some portability issues. Needs adaptation. |
| 0-3 | Hardcoded for single environment. |

### governance_maturity (15)

| Score | Criteria |
|-------|----------|
| 13-15 | Owner defined, version history, regression tests, promotion policy. |
| 10-12 | Good governance with minor gaps. |
| 6-9 | Basic governance. Needs structure. |
| 0-5 | No governance. Ad-hoc. |

## Output Format

```json
{
  "archetype": "Production",
  "scores": {
    "trigger_accuracy": 14,
    "execution_reliability": 16,
    "boundary_clarity": 9,
    "context_efficiency": 8,
    "documentation": 8,
    "error_handling": 9,
    "portability": null,
    "governance_maturity": null
  },
  "raw_total": 64,
  "max_possible": 75,
  "percentage": 85,
  "pass": true,
  "lowest_dimension": "context_efficiency",
  "improvement_suggestion": "Trim redundant sections in SKILL.md. Move long examples to references/."
}
```

**Notes:**
- Dimensions not applicable to the archetype are scored as `null`
- `raw_total` is the sum of applicable dimension scores
- `max_possible` is the sum of max points for applicable dimensions
- `percentage` = raw_total / max_possible * 100
- `pass` is true if percentage meets the archetype's threshold
