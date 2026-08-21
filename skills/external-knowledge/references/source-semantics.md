# Source Semantics

Use this reference only when source ownership is ambiguous. The main `SKILL.md` should remain sufficient for ordinary cases.

## Principle

Route from **information need → source semantics → provider**, not from keywords → provider.

The provider is an implementation detail. The source semantic is the durable concept.

## Source Classes

### Authoritative current state

Use for:

- pricing
- subscription plans
- product availability
- current feature sets
- release announcements
- current policies

Prefer first-party product pages, official announcements, changelogs, release notes, or vendor documentation.

A low-risk current-state question may stop after one authoritative source.

### Historical change

Use when the user asks what changed over time.

A current page proves the current state, not the historical delta. Look for dated announcements, archived release notes, changelogs, prior documentation, or other dated evidence.

Do not infer a before/after comparison from a current-only page.

### Versioned technical documentation

Use Context7 or an equivalent version-aware specialist when available. Fall back to official versioned docs when the specialist is absent or lacks the requested version.

### GitHub-native evidence

Use a GitHub-native connector/plugin for claims whose meaning depends on repository structure or history:

- why a PR changed something
- issue discussion
- review comments
- commit history
- release metadata
- repository state

A normal web search result that points at GitHub is not equivalent to GitHub-native semantic access.

### WeChat article discovery

Use when WeChat Official Account content is explicitly requested or is a high-fit source for the user's remembered/discovery task.

Examples:

- “找一下公众号里关于 Agent Skill 的文章。”
- “我记得前段时间有人写过一篇中文长文，比较 OpenCode Go 和其他编码套餐，帮我找出来。”
- “国内有没有公众号长文分析这次套餐变化？”

The user does not need to name the WeChat tool.

Do not equate Chinese language with WeChat intent. A Chinese question about an official current price still belongs to authoritative current sources.

### WeChat article reading

When the user already supplies a canonical `https://mp.weixin.qq.com/s/<id>` URL, or discovery yields one and article content is needed, use the WeChat reader when available.

If the user asked only for candidate articles, discovery is sufficient; do not read every result.

### General Web

Use the runtime-native Web search/fetch path when no specialist source clearly owns the task.

Examples:

- product changes
- company announcements
- current events
- public webpages
- cross-vendor comparisons

### Precision challenger

Use Exa or an equivalent precision search provider only after normal search exhibits an observable precision gap, such as:

- repeatedly irrelevant results;
- exact niche fact not located;
- known relevant entity/page not discoverable through general search.

Do not use a challenger merely because it is installed.

### Extraction challenger

Use Firecrawl or an equivalent extraction provider only after a known URL cannot be read adequately through the ordinary fetch path.

Observable extraction gaps include:

- empty shell;
- required body missing;
- client-rendered content absent from fetched text.

A JavaScript-heavy reputation alone is not evidence of an extraction gap.

## Runtime Portability

Provider names above describe expected capabilities, not mandatory dependencies.

At runtime:

1. discover what is actually available;
2. choose the best available owner;
3. fall back only when the fallback can still satisfy the evidence need;
4. never install or reconfigure a provider as an implicit fallback.

This keeps the skill portable across Codex, ZCode, and other agent runtimes.
