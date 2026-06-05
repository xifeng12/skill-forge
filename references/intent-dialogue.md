# Intent Dialogue

Use a short intent dialogue before deep authoring so the first version of the skill is anchored in the real job rather than in a guessed prompt shape.

## Opening Patterns

### English

**Good**:
> "What's the job you're trying to automate? Tell me about the work first."

**Avoid**:
> "Please provide: Name / Capability / Inputs / Outputs / Exclusions"

### Chinese

**Good**:
> "你想解决什么问题？先说说你的工作场景吧。"

**Avoid**:
> "请提供：名称 / 能力 / 输入 / 输出 / 排除项"

### Opening Style

- Start from the user's work, not from a form
- Ask 2-3 high-leverage questions first
- Let the user answer naturally before offering a scaffold
- Sound like a design partner, not a form processor

## Why This Step Exists

- raw workflow material is often incomplete, mixed, or ambiguous
- the wrong boundary chosen early is expensive to repair later
- good trigger design depends on knowing what should not route here
- execution assets should follow confirmed outputs, not assumptions

## What To Capture

Ask only the questions that change the package design.

1. What recurring job should this skill own?
2. What inputs will people actually hand to it?
3. What outputs should it produce every time?
4. What near-neighbor requests should stay out of scope?
5. What quality bar matters most: speed, consistency, auditability, portability, or governance?
6. What assets already exist: docs, scripts, templates, examples, or prior prompts?
7. What constraints matter: privacy, naming, local library fit, or target environments?
8. **What design pattern fits best?** (see Design Patterns below)
9. **Where should output files be stored?** (see Output Directory below)

## Output Directory Configuration

**必须询问用户**：

> "新 Skill 的输出文件放在哪里？"
>
> 选项：
> - 默认位置：`F:/agent2/.opencode/skills-output/{skill-name}/`
> - 用户指定：________________
> - 无输出文件：不创建输出目录

**处理逻辑**：

| 用户响应 | 处理方式 |
|---------|---------|
| 不指定 / 选择默认 | 自动设置 `output_dir`，创建 `{tmp,output}/` 目录 |
| 指定位置 | 使用用户指定的位置，记录在 frontmatter |
| 无输出文件 | 不设置 `output_dir`，标注 `output: none` |

**SKILL.md frontmatter 示例**：

```yaml
---
name: my-skill
description: ...
output_dir: F:/agent2/.opencode/skills-output/my-skill
---
```

## Design Pattern Selection

After capturing the core requirements, select the appropriate design pattern:

| Pattern | Use When | Example |
|---------|----------|---------|
| **Tool Wrapper** | Need to call external tools/APIs | yt-dlp, OCR, REST API |
| **Generator** | Need to generate structured output | PR descriptions, config files |
| **Reviewer** | Need to review/check content | Code review, security audit |
| **Pipeline** | Need multi-step coordination | File processing workflows |
| **Inversion** | Need deep information gathering | Requirements analysis |

**Quick Decision Rules:**

```
Need to call external tools/APIs? → Tool Wrapper
Need to generate structured content? → Generator
Need to review/check? → Reviewer
Need multi-step coordination? → Pipeline
Need deep information gathering? → Inversion

Complex scenarios can combine patterns (e.g., Pipeline + Generator)
```

See [Design Patterns](design-patterns.md) for detailed templates.

## Interview Rule

- prefer `5-7` sharp questions over a long discovery questionnaire
- ask boundary questions early
- ask output questions before architecture questions
- **ask design pattern question after understanding the core job**
- stop once the skill can be described clearly in one sentence

## Output

The dialogue should produce:

- one clear capability sentence
- a list of real inputs
- a list of required outputs
- a short exclusion list
- one recommended archetype (Scaffold/Production/Library)
- **one design pattern (Tool Wrapper/Generator/Reviewer/Pipeline/Inversion)**
- **output directory setting (default / user-specified / none)**
- one recommended first evaluation target

## Failure Pattern

Do not continue into full authoring when the dialogue still leaves these unresolved:

- whether the request is really reusable
- which near-neighbor requests should not trigger
- what concrete deliverable the skill must return
- **which design pattern applies**
