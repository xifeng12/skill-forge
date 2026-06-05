# Synthesis Path

Source synthesis ensures the skill is built from sufficient inputs rather than guessed assumptions. Runs between Reference Scan and Scaffold.

## Two Tiers

| Archetype | Synthesis Level | What's Required |
|-----------|----------------|-----------------|
| Scaffold | None | Optional, skip freely |
| Production | Lightweight | 3+ sources, simple list in SOURCES.md |
| Library / Integration | Strict | Coverage matrix, depth gates, source-backed decisions |

## Lightweight Synthesis (Production)

For most Production skills — Tool Wrappers, Generators, simple Reviewers.

**3 steps:**

1. **Collect 3+ sources** — pick from: workspace docs, official docs, source code, public examples, test files. Don't overthink trust tiers — just prefer official over community, code over prose.

2. **Write SOURCES.md** — a simple list:

```markdown
# Sources

| Source | What It Provides | Retrieved |
|--------|-----------------|-----------|
| README.md | API surface, usage examples | 2026-04-20 |
| src/index.ts | Public API definitions | 2026-04-20 |
| tests/basic.test.ts | Expected behavior patterns | 2026-04-20 |

## Open Gaps
- Error handling docs not found — check issues/ or CHANGELOG next
```

3. **Check you're ready** — can you describe the skill's behavior based only on what you collected? If not, get one more source.

That's it. No coverage matrix, no trust tiers, no depth gates.

## Strict Synthesis (Library / Integration)

For shared infrastructure skills and integration/documentation skills where incomplete inputs produce dangerous outputs.

**5 steps:**

1. **Collect sources with trust tiers**

| Channel | Trust |
|---------|-------|
| Local docs, official docs, source code | High — use directly |
| Public benchmarks, test suites | High — flag version |
| Community posts, blog summaries | Medium — cross-reference before relying on |
| AI-generated analysis | Low — hypothesis only, never sole source |

2. **Record provenance in SOURCES.md**

```markdown
# Sources

| Source | Type | Trust | Retrieved | Contribution | Notes |
|--------|------|-------|-----------|--------------|-------|
| src/core/api.ts | source-code | high | 2026-04-20 | API surface | Primary reference |
| CHANGELOG.md | official-doc | high | 2026-04-20 | Version variance | v2 breaking changes |
```

3. **Build coverage matrix**

```markdown
## Coverage Matrix

| Area | Sources | Status | Gap Action |
|------|---------|--------|------------|
| API surface | api.ts, README | ✅ | — |
| Failure modes | tests/ | ⚠️ Partial | Need 5+ error patterns |
| Version variance | CHANGELOG | ❌ Missing | Must retrieve |
```

4. **Pass depth gates before authoring**

| Gate | Condition |
|------|-----------|
| source_minimum | 3+ high-trust sources |
| coverage_complete | No ❌ in critical areas |
| gaps_planned | Every ⚠️/❌ has a next action |

5. **Anchor design decisions to sources**

When making architectural choices, note which source supports the decision. Flag decisions without source backing as "assumption" for later validation.

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Writing a Library skill from memory alone | High risk of gaps in API surface or failure modes |
| Using only AI-generated summaries | No provenance, easy to hallucinate |
| Skipping SOURCES.md for Production+ | Can't revisit or verify what informed the skill |
