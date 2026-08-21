# External Knowledge — Experimental Skill v0.1

`external-knowledge` is an experimental agent skill for obtaining current or external information with the **minimum sufficient retrieval effort**.

It is designed to validate a set of skill-design hypotheses derived from prior Agent Skill article reviews and real routing experiments:

- trigger from user intent rather than tool names;
- route by **information need → source semantics → provider**;
- prefer specialist owners when they clearly own the claim;
- escalate challengers only after an observable gap;
- stop when more retrieval would not change the answer, confidence, risk, or next action;
- keep runtime capability differences outside the generic skill contract.

## What this skill is not

It is not:

- a WebSearch wrapper;
- a mega-router whose goal is to dispatch tools;
- a requirement to query every available provider;
- an installer or environment-repair workflow;
- a deep-research workflow for every lookup.

A request such as “查询一下 OpenCode Go 套餐最近有什么变化” should remain a small task when official/current sources are sufficient.

## WeChat as a source semantic

WeChat article retrieval is intentionally first-class.

The user does not need to say “call the WeChat tool”. If the task is to find a remembered Chinese long-form article or public-account commentary, the agent may infer that WeChat discovery is a high-fit source.

This does **not** mean the discovery backend itself is vector semantic search. Current WeChat discovery may still use keyword search; semantic routing happens at the agent layer.

## Layout

```text
skills/external-knowledge/
├── SKILL.md
├── README.md
├── manifest.json
├── agents/
│   └── openai.yaml
├── references/
│   ├── source-semantics.md
│   └── gotchas.md
└── evals/
    ├── evals.json
    └── zcode-profile.md
```

## First runtime target: ZCode

The first experiment is intentionally run in ZCode before further Codex iteration.

Current ZCode-specific fact:

- Firecrawl has been removed and is treated as optional/unavailable for the first test pass.

That fact lives only in `evals/zcode-profile.md`; the generic skill does not assume Firecrawl is absent in other runtimes.

Start with cases `E1`, `E2`, `E3`, `E5`, `E7`, and `E8` from `evals/evals.json`.

The most important early checks are:

1. Does a simple OpenCode Go lookup stay simple?
2. Can a remembered Chinese long-form article trigger WeChat discovery without literal 微信/公众号 keywords?
3. Does explicit WeChat discovery stop after useful candidates rather than reading everything?
4. Do stable-knowledge and provided-context questions avoid unnecessary external retrieval?

## Installation / testing

This skill currently lives inside the public `xifeng12/skill-forge` repository as an experimental sample.

If your skill manager supports selecting nested skills, select `external-knowledge` from this repository. Otherwise copy the `skills/external-knowledge/` directory into the runtime's local skill root for the experiment.

Do not install missing optional providers merely to make an eval case executable. Mark capability-dependent cases `NOT_APPLICABLE` when the runtime does not expose the required provider.

## Status

`v0.1.0` — Scaffold / experimental.

The goal of the first iteration is not to prove the theory correct. It is to produce runtime evidence strong enough to keep, revise, or reject the design hypotheses.
