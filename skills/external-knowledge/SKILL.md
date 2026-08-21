---
name: external-knowledge
description: Retrieve current or external information when a reliable answer depends on sources beyond the model's stable knowledge. Use for product, pricing, plan, policy, release, or feature changes; versioned technical docs; GitHub-native facts; WeChat article discovery or reading; and other source-grounded lookups. Choose sources by information need, prefer specialist owners, escalate only for an observed gap, and stop when the evidence is sufficient. Do not use for tasks answerable from the user's provided context or stable general knowledge.
license: MIT
metadata:
  version: "0.1.0"
  mode: "Scaffold"
  skill_type: "Capability"
  status: "experimental"
---

# External Knowledge

Get enough reliable external evidence to answer the user's actual question — no less, and no more.

This skill is a behavioral policy over existing tools. It is not a search backend and not a mega-router. Source selection is part of completing the user's information goal.

## Core Loop

1. Identify the claim or decision the user actually needs.
2. Decide whether external information is necessary. If not, answer without retrieval.
3. Choose the best initial source class for that information need.
4. Retrieve the minimum evidence needed.
5. Name any remaining evidence gap precisely.
6. Escalate only to a provider that addresses that specific gap.
7. Stop when more retrieval is unlikely to change the answer, confidence, risk, or next action.

Do not turn a simple lookup into a research project.

## Source Semantics

Use information need, not keywords alone, to choose the source.

| Information need | Preferred owner | Notes |
|---|---|---|
| Current product, pricing, plan, policy, feature, announcement | Official/current Web source | A single authoritative source may be enough for a simple current-state question. |
| Version-specific library, framework, SDK, API behavior | Context7 when available; otherwise official docs | Prefer versioned documentation over generic web summaries. |
| Repository, commit, PR, issue, release, review, code-history semantics | GitHub-native connector/plugin | Treat ordinary GitHub-hosted webpages as Web only when repository semantics are not required. |
| Discover WeChat Official Account articles by topic | WeChat discovery specialist when available | Trigger from source semantics, not only from the literal words “微信/公众号”. |
| Read a known canonical `https://mp.weixin.qq.com/s/<id>` article | WeChat reader specialist when available | Read only when article body is needed. |
| General current/public information | Runtime-native Web search/fetch | This is the general default when no specialist source clearly owns the claim. |
| General Web search has an observable precision gap | Exa or equivalent precision challenger when available | Challenger only after the gap is observed. |
| A known URL cannot be read/extracted adequately | Firecrawl or equivalent extraction challenger when available | Never invoke merely because the page might be JavaScript-heavy. |

Read [references/source-semantics.md](references/source-semantics.md) when source ownership is ambiguous.

## WeChat Semantic Routing

WeChat is a first-class source semantic, not a keyword-only special case.

Use WeChat discovery when:

- the user explicitly asks for WeChat / Official Account articles; or
- the user is trying to recover or discover a Chinese long-form article and WeChat is a high-fit source; or
- the information need is specifically about Chinese public-account commentary, analysis, or article discovery.

Do **not** search WeChat for every Chinese-language query.

Current WeChat discovery backends may be keyword-based. The semantic behavior happens at the agent layer: infer that WeChat is an appropriate source, derive a useful search expression, then call the specialist. Do not claim vector or embedding-based semantic retrieval unless the backend actually provides it.

If discovery returns an article list and the user only asked for candidates, stop. If the user needs article content, resolve/select a canonical article and use the reader when available.

## Provider Availability

Treat provider availability as runtime-specific.

- Use an available specialist when it clearly owns the task.
- If a specialist is absent, use the nearest viable fallback only when it can still answer reliably.
- If absence materially reduces confidence or blocks the task, say so briefly.
- Missing capability is **not authorization to install, configure, repair, or replace tools**. Do that only when the user explicitly asks for environment changes.

Never assume a provider exists because it was available in another runtime.

## Evidence Depth

Match retrieval effort to the question.

A simple current-state lookup may need one authoritative source.

Increase evidence depth when the user asks for:

- historical change rather than current state;
- comparison across time, products, or vendors;
- disputed or community sentiment claims;
- a high-impact engineering or operational decision;
- a claim the primary source does not fully support.

Do not cross-check mechanically when the primary evidence already resolves a low-risk factual question.

## Escalation Rules

Escalation requires an observable gap.

Examples:

- Official page shows today's OpenCode Go plan but not what changed → the gap is historical comparison; search historical announcements or credible dated sources.
- General Web cannot locate an exact niche technical fact → precision gap; use Exa if available.
- Web fetch returns an empty shell and required text is absent → extraction gap; use Firecrawl if available.
- WeChat discovery finds candidates but the user asks what the article argues → content gap; use the WeChat reader.

Do not call multiple providers in parallel merely for coverage.

## Stop Rules

Stop when the answer is supported well enough for the user's actual request.

Continue only if another retrieval could materially change at least one of:

- the conclusion;
- confidence in the conclusion;
- a material risk;
- the user's next action.

If none would change, stop.

## Output Contract

Answer the user's question directly, then provide the minimum supporting context.

For changing products, plans, releases, or policies:

- separate the **current state** from **what changed**;
- use concrete dates when available;
- distinguish confirmed facts from inference;
- cite the sources that support each material claim.

Do not expose internal routing tables unless the user asks how the answer was obtained.

## Boundaries

- Do not install or configure providers during an information lookup unless explicitly requested.
- Do not force a specialist when general Web already answers the question adequately.
- Do not force General Web when a specialist clearly owns the claim.
- Do not invent historical change from a current-only page.
- Do not treat a provider's absence as a reason to redesign the environment.
- Do not keep searching after the stop condition is met.

Known failure modes are tracked in [references/gotchas.md](references/gotchas.md).
