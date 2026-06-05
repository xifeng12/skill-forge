# STATE.md — Skill-Forge Optimization State

> Persistent task state for skill-forge. New sessions should read this file before taking any action in this directory.
> Location: `.opencode/skills/custom/skill-forge/STATE.md`

---

## Current Task

v2.0 darwin-skill re-assessment and optimization (2026-06-05)

## Progress

- [x] **P0: Core Self-Coherence Fix** (2026-05-02)
  - [x] Darwin-skill baseline assessment: 78.0 (dim7 weakest at 4.0)
  - [x] SKILL.md refactor: numbered steps → Outcome/Constraints/Signals
  - [x] Commit: `eaf2820` on branch `auto-optimize/20260502-skill-forge`
  - [x] Darwin-skill re-assessment: 86.7 (dim7 improved to 7.5)
  - [x] Ratchet rule: PASSED (86.7 > 78.0)

- [x] **P1: AI Behavior Constraint Enhancement** (2026-05-02)
  - [x] Update root AGENTS.md (Rule 11–13)
  - [x] Update skill-forge/AGENTS.md (self-check output format)

- [x] **P2: State Persistence Mechanism** (2026-05-02)
  - [x] Create this STATE.md file
  - [x] Update skill-forge/AGENTS.md to reference STATE.md

- [x] **P3: AGENTS.md Mechanism Optimization** (2026-05-02)
  - [x] Plan Mode constraints in root AGENTS.md (Rule 12)
  - [x] Uncertainty escalation meta-rule (Rule 13)
  - [x] Adapted Karpathy guidelines (Rule 14 + Rule 5 surgical precision)

- [x] **P4: v2.0 darwin-skill re-assessment** (2026-06-05)
  - [x] git init in skill-forge (was non-git, v2.0 requires git)
  - [x] Baseline commit `2246b41` (v1.3.0 working tree snapshot)
  - [x] Branch: `auto-optimize/20260605-skill-forge-v2`
  - [x] v2.0 9-dim baseline: **83.0/99** (dim4=2 design conflict, dim8 single-agent sim)
  - [x] 元 skill 自洽性附加: 4.5/5 + 1 软警告 (L128 user-initiated 解释)
  - [x] Round 1 (`eabfd46`): dim9 +1.0 → 84.0
  - [x] Round 2 (`acbf9e4`): dim1 +0.5 → 84.5
  - [x] 触顶信号触发: 连续 2 轮 Δ<2 → 见好就收 break
  - [x] Result card 归档: `F:\tmp\darwin-archived-2026-06-05\result-cards\skill-forge-v2.0.html`
  - [x] 0 revert, 100% keep rate

## Blockers

None.

## Next Step

**v2.0 优化已完成，84.5/99 (v2.0 9-dim) + 触顶收工。**

剩余 4 维 (dim5/dim2/dim7/dim3) 留作下一轮评估，原因：
- SKILL.md 已 300 行 = Constraint 4 budget ceiling
- 继续需先将部分内容移到 references/ 才能给其他 dim 留空间
- 触顶信号表明已接近 v2.0 9-dim 框架下 skill-forge 的局部最优

可选方向：
- **继续 v2.0 优化**: Round 3+ 之前先把当前内容分块移到 references/ (释放 SKILL.md 空间)
- **Phase 2.5 探索性重写**: 从头重写 SKILL.md 而不是微调（解锁局部最优）
- **Finalize**: 合并分支 `auto-optimize/20260605-skill-forge-v2` 到 master

历史峰值参考：89.5 (commit `41f2f3a`, 2026-05-02, v1 darwin 8-dim, **rubric 不同不可直接比**)

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
| 2026-06-05 | **v2.0 darwin re-assess baseline (9-dim)** | **83.0** | `2246b41` |
| 2026-06-05 | Round 1: dim9 (anti-patterns) add dedicated section | 84.0 | `eabfd46` |
| 2026-06-05 | Round 2: dim1 (frontmatter) remove redundant summary | **84.5** | `acbf9e4` |

## Lessons Learned (2026-05-04)

1. **元 skill 评估必须扫描自身设计哲学**：Round 2 被 revert 的根因是未在优化前重读 v2 改进总结中"不加检查点"的明确决策。优化者（agent）与评估者应为不同上下文。
2. **Constraint 形式 ≠ 设计意图合规**：即使使用 Constraint 语言写 "must not proceed without confirmation"，如果 skill 的设计哲学是 "不加检查点、agent 自主决策"，该约束仍属违规。
3. **基线评估的扣分理由需复核**：dim4 基线 7.0 的扣分理由 "缺少人在回路" 与 v2 设计意图冲突，不应作为缺陷。

## Lessons Learned (2026-06-05 v2.0)

4. **v2.0 dim4 评估 skill-forge 必然低分**：skill-forge "不加检查点" 是非协商项；v2.0 dim4 强制要求 🔴/STOP/CHECKPOINT — 直接冲突。2/6 是诚实评分，不应作为改进方向。
5. **见好就收信号准确**：连续 2 轮 Δ<2.0 (R1=+1.0, R2=+0.5) → 触顶，表明已接近局部最优。继续调整风险 > 收益。
6. **SKILL.md 行数预算会先于 ROI 见顶**：v2.0 dim9 加 19 行让 SKILL.md 281→300，触及 Constraint 4 ceiling。剩余优化需先腾空间。
7. **v1 ↔ v2 分数不可直接比**：rubric 变了 (8→9 维, 权重不同, dim4 独立)，85.2 (v1) 和 84.5 (v2) 不是同一量度。v2 的实际进步是 +1.5 (83.0→84.5)。

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
- v2.0 result card (this run): `F:\tmp\darwin-archived-2026-06-05\result-cards\skill-forge-v2.0.html`
- v1 result card (archived): `F:\tmp\darwin-archived-2026-06-05\skill-forge-result-card.html`
