# Boundary Conditions & Fallbacks

Defensive behaviors for edge cases and failure modes across all phases.

| Scenario | Trigger | Fallback Action |
|---|---|---|
| User intent unclear / contradictory | Phase 1 capture fails | Ask clarifying questions (max 2 rounds). If still unclear, suggest Scaffold mode with minimal scope. |
| Skill already exists (name collision) | Phase 1 or 2 | Alert user, offer to iterate existing skill instead of creating new. |
| Reference file missing or unreadable | Phase 1 scan | Skip scan, warn user, continue with reduced context. Do NOT fail silently. |
| Eval workspace already exists | Phase 2 scaffold | Reuse and warn, or ask user to delete/backup. |
| Eval run fails / timeouts | Phase 3 iteration | Mark as `failed` in benchmark, explain to user, suggest retry with simpler prompts or manual review. |
| Gate script missing or errors | Phase 4 harden | Report script failure, skip gate, flag in summary. Do NOT claim gate passed. |
| Retirement check inconclusive | Phase 3 retirement criteria | Present ambiguous evidence, recommend human judgment. Default to **keep** unless evidence is strong. |
| User rejects all mode suggestions | Phase 1 Go/NoGo < 2 or user disagrees with assessment | Present alternatives (script, alias, prompt template). Do NOT force Scaffold as fallback — respect user's choice to not build a skill. |
| Manifest packaging fails | Phase 5 `manifest.json` invalid or `.skill` build errors | Report specific validation errors, suggest fixes, remain in Phase 4 until resolved. Do NOT ship broken package. |
