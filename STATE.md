# STATE.md — Skill-Forge Optimization State

> Persistent task state for skill-forge. New sessions should read this file before taking any action in this directory.
> Location: `.opencode/skills/custom/skill-forge/STATE.md`

---

## Current Task

Upgrade skill-forge from v1.1.0 to v1.2.0+

## Progress

- [x] **P0: Core Self-Coherence Fix**
  - [x] Darwin-skill baseline assessment: 78.0 (dim7 weakest at 4.0)
  - [x] SKILL.md refactor: numbered steps → Outcome/Constraints/Signals
  - [x] Commit: `eaf2820` on branch `auto-optimize/20260502-skill-forge`
  - [x] Darwin-skill re-assessment: 86.7 (dim7 improved to 7.5)
  - [x] Ratchet rule: PASSED (86.7 > 78.0)

- [x] **P1: AI Behavior Constraint Enhancement**
  - [x] Update root AGENTS.md (Rule 11–13)
  - [x] Update skill-forge/AGENTS.md (self-check output format)

- [x] **P2: State Persistence Mechanism**
  - [x] Create this STATE.md file
  - [x] Update skill-forge/AGENTS.md to reference STATE.md

- [x] **P3: AGENTS.md Mechanism Optimization**
  - [x] Plan Mode constraints in root AGENTS.md (Rule 12)
  - [x] Uncertainty escalation meta-rule (Rule 13)
  - [x] Adapted Karpathy guidelines (Rule 14 + Rule 5 surgical precision)

## Blockers

None.

## Next Step

**优化循环已完成，当前分数 85.2。**

6 轮实验：4 keep + 1 revert + 1 基线。

可选方向：
- **继续 Round 7**: 冲击 86+（dim4 检查点主观性改进，或 dim8 实测再验证）
- **Finalize**: 合并分支 `auto-optimize/20260504-skill-forge` 到 master

历史峰值参考：89.5 (commit `41f2f3a`, 2026-05-02, 但不在当前 git 历史中)

## History

| Date | Event | Score | Commit |
|------|-------|-------|--------|
| 2026-05-02 | Baseline assessment (dry_run) | 78.0 | `b493d9b` |
| 2026-05-02 | SKILL.md Goal-vs-Procedure fix (dry_run) | 86.7 | `eaf2820` |
| 2026-05-02 | Full_test dim8 verification | **89.5** | `41f2f3a` |
| 2026-05-02 | dim8: baseline 7.0 (dry_run) → 8.5 (full_test), with-skill avg 8.3 vs baseline 4.7 | | |
| 2026-05-04 | Darwin-skill baseline (v1.2.0 working tree, dry_run) | 77.1 | `working-tree` |
| 2026-05-04 | Round 1: manifest.json dependencies 对齐 governance.md | 78.6 | `ed3f66b` |
| 2026-05-04 | Round 2: Phase 4→5 增加人在回路确认约束 | 79.6 → **revert** | `15c51be` → `50c15df` |
| 2026-05-04 | Round 3: 添加 Scripts Map 消除脚本幽灵 | **79.4** | `cf0ed78` |
| 2026-05-04 | **Full_test 完整测试** (dim8 子 agent 实测) | **83.6** | `6f7d2be` |
| 2026-05-04 | dim8: 8.7/10 (p1:9, p2:8, p3:9), dim7:9.0, dim6:8.0 | | |
| 2026-05-04 | Round 4: 补充 eval 执行具体命令 | **84.4** | `ba83b65` |
| 2026-05-04 | Round 5: 扩展边界条件（manifest 失败 + 用户拒绝） | **84.9** | `ed069c0` |
| 2026-05-04 | Round 6: 为 6 个核心脚本补充 docstring | **85.2** | `554bcdf` |

## Lessons Learned (2026-05-04)

1. **元 skill 评估必须扫描自身设计哲学**：Round 2 被 revert 的根因是未在优化前重读 v2 改进总结中"不加检查点"的明确决策。优化者（agent）与评估者应为不同上下文。
2. **Constraint 形式 ≠ 设计意图合规**：即使使用 Constraint 语言写 "must not proceed without confirmation"，如果 skill 的设计哲学是 "不加检查点、agent 自主决策"，该约束仍属违规。
3. **基线评估的扣分理由需复核**：dim4 基线 7.0 的扣分理由 "缺少人在回路" 与 v2 设计意图冲突，不应作为缺陷。

## Design Decisions (Non-Negotiable)

以下决策经 v2 改进验证，**任何后续优化不得违背**。agent 在提出改动前必须逐项核对。

| 决策 | 来源 | 效果层面的禁止行为 | 允许替代 |
|------|------|-------------------|---------|
| 不加检查点 | v2 改进总结 2026-05-02 | 任何导致 agent "暂停等用户确认" 的约束、信号或步骤 | 条件清单（Go/No-Go 计分、模式标准、退役信号），agent 满足条件后自主流转 |
| Procedure → Constraint | goal-vs-procedure.md | 微步骤指令（Step 1/2/3、先X后Y） | 目标描述 + 约束边界 + 反模式清单 |
| 与 skill-architect 分工 | v2 触发词调整 | 在 description 中抢夺架构咨询触发词 | skill-forge 聚焦生命周期动词：forge/evaluate/iterate/package/retire |
| Skill Types 区分 | skill-types.md | 混淆 Capability 与 Preference 的退役逻辑 | Capability：无 skill 测试通过 → 退役；Preference：组织决策 → 退役 |
| 反触发测试同等重要 | eval-playbook.md | 只测试正触发、忽略 should-not-trigger | 正触发 + 反触发双测，防止 hijacking |

> **否决清单使用方式**：每次提出改动时，回答——"这个改动的**效果**是什么？它是否触发了上表中的任何'禁止行为'？"

## References

- Root constraints: `E:/cs1/AGENTS.md`
- Skill-forge constraints: `E:/cs1/.opencode/skills/custom/skill-forge/AGENTS.md`
- Skill-forge SKILL.md: `E:/cs1/.opencode/skills/custom/skill-forge/SKILL.md`
- Darwin-skill results: `E:/cs1/.opencode/skills/custom/darwin-skill/results.tsv`
