# ADK Skill Design Patterns

5 种核心设计模式，用于构建高质量 Agent Skills。

---

## 1. Tool Wrapper（工具封装模式）

**用途**：封装外部库、CLI 工具或 API，使其对 Agent 可用。

```
skill-name/
├── SKILL.md           # 调用规则、参数说明、触发条件
├── references/
│   └── api-docs.md    # API 文档摘要、参数说明
└── assets/
    └── examples/      # 示例文件（可选）
```

**设计要点**：
- `SKILL.md` 只写"怎么调用"，不写"API 细节"
- API 文档、参数表放在 `references/`
- 提供明确的触发短语（triggers）

**示例**：封装 yt-dlp、paddleocr、REST API

---

## 2. Generator（生成器模式）

**用途**：根据模板生成结构化输出（代码、文档、配置文件等）。

```
skill-name/
├── SKILL.md           # 生成流程、字段要求
├── references/
│   └── conventions.md # 编码规范、命名约定
└── assets/
    └── template.md    # 输出模板
```

**设计要点**：
- 使用 `assets/` 存放模板文件
- `SKILL.md` 定义必需字段和生成逻辑
- 分离"模板"与"填充规则"

**示例**：生成 PR Description、README.md、配置文件

---

## 3. Reviewer（评审模式）

**用途**：对代码、文档、配置等进行评审，输出结构化评审报告。

```
skill-name/
├── SKILL.md           # 评审流程、输出格式
├── references/
│   └── checklist.md   # 评审准则清单
└── assets/
    └── report-template.md  # 评审报告模板
```

**设计要点**：
- **关键**：分离 Checklist 与评审协议
- Checklist 放在 `references/`，可独立更新
- 评审流程写在 `SKILL.md`

**示例**：代码评审、安全审计、文档质量检查

---

## 4. Inversion（反转模式）

**用途**：通过多轮访谈采集信息，确保输入完整后再行动。

```
skill-name/
├── SKILL.md           # 访谈流程、Phase 定义
├── references/
│   └── questions.md   # 问题库（可选）
└── assets/
    └── form.md        # 信息采集表（可选）
```

**设计要点**：
- **Phase-based**：定义清晰的访谈阶段
- **禁止提前行动**：未完成采集前不生成输出
- **Gate 条件**：每个 Phase 有明确的完成条件

**示例**：需求分析、项目规划、技术选型咨询

---

## 5. Pipeline（流水线模式）

**用途**：协调多步骤任务，确保每个步骤按条件执行。

```
skill-name/
├── SKILL.md           # Step 定义、Gate 条件、流转规则
├── references/
│   └── rules.md       # 业务规则（可选）
└── assets/
    └── templates/     # 各步骤的模板（可选）
```

**设计要点**：
- **显式 Step**：每个步骤有明确输入输出
- **Gate 条件**：定义步骤间的准入条件
- **状态追踪**：记录当前执行状态

**示例**：复杂文件处理、多阶段代码生成、端到端工作流

---

## 模式组合

复杂 Skill 可以组合多种模式：

| 组合 | 适用场景 |
|------|----------|
| Pipeline + Inversion | 需要信息采集的多步任务 |
| Pipeline + Generator | 多阶段内容生成 |
| Inversion + Reviewer | 带信息核对的评审 |
| Tool Wrapper + Pipeline | 多工具协调工作流 |

---

## 模式选择决策树

```
需要调用外部工具/API？ → Tool Wrapper
需要生成结构化内容？ → Generator
需要评审/检查？ → Reviewer
需要多步骤协调？ → Pipeline
需要深度信息采集？ → Inversion

复杂场景可组合多种模式（如 Pipeline + Generator）
```

---

## 最佳实践

1. **单一职责**：每个 Skill 专注一个核心功能
2. **分离关注点**：逻辑、规则、模板分开存放
3. **明确触发**：提供清晰的 triggers 描述
4. **可测试性**：设计时可考虑如何验证效果
5. **保持精简**：SKILL.md 控制在 500 行以内

---

## SKILL.md 模板

### 基础结构

```markdown
---
name: {skill-name}
description: |
  {功能描述}
  Triggers: "{触发短语1}", "{触发短语2}"
mode: {tool-wrapper|generator|reviewer|pipeline|inversion}
---

# {Skill 标题}

{简短说明}

## 核心功能

{主要功能点}

## 使用方法

{使用说明}
```

### 各模式模板示例

#### Tool Wrapper

```markdown
---
name: {tool-name}-wrapper
description: |
  封装 {tool-name} 工具，提供 {核心功能} 能力。
  Triggers: "调用{工具}", "使用{工具}", "{tool-cli-cmd}"
mode: tool-wrapper
---

# {Tool Name} Wrapper

封装 {tool-name} 的核心功能。

## 可用操作

| 操作 | 命令 | 说明 |
|------|------|------|
| {op1} | `{cmd1}` | {desc1} |

## 参数说明

见 `references/params.md`。
```

#### Generator

```markdown
---
name: {name}-generator
description: |
  生成 {输出类型}，遵循 {规范名称} 规范。
  Triggers: "生成{类型}", "创建{类型}", "write {type}"
mode: generator
---

# {Name} Generator

根据模板生成 {输出类型}。

## 必需字段

- {field1}: {说明}

## 模板

见 `assets/template.md`。
```

#### Reviewer

```markdown
---
name: {name}-reviewer
description: |
  评审 {评审对象}，输出结构化报告。
  Triggers: "评审{对象}", "review {object}", "检查{对象}"
mode: reviewer
---

# {Name} Reviewer

对 {评审对象} 进行评审。

## 评审准则

见 `references/checklist.md`。

## 评审流程

1. 读取目标文件
2. 逐项检查准则
3. 生成评审报告
```

#### Inversion

```markdown
---
name: {name}-collector
description: |
  通过多轮访谈采集 {信息类型} 信息。
  Triggers: "分析{类型}", "采集{信息}", "{领域}分析"
mode: inversion
---

# {Name} Collector

采集 {信息类型} 信息。

## 访谈阶段

### Phase 1: {阶段名}

**目标**: {阶段目标}
**问题**: {关键问题}
**Gate**: {完成条件}

## 禁止事项

- 信息不完整时禁止生成输出
- 禁止跳过任何 Phase
```

#### Pipeline

```markdown
---
name: {name}-pipeline
description: |
  执行 {任务名} 的多步流水线。
  Triggers: "{动词}{对象}", "run {name}"
mode: pipeline
---

# {Name} Pipeline

{任务描述}

## 流水线步骤

### Step 1: {步骤名}

**输入**: {输入说明}
**处理**: {处理逻辑}
**输出**: {输出说明}
**Gate**: {准入条件}
```
