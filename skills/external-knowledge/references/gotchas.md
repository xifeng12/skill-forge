# Known Failure Modes

Append-only log for failures that matter to this skill. Seed entries come from prior external-knowledge routing and integration experiments and are marked as hypotheses until reproduced by this skill's own evals.

## G-EXT-001 — Simple lookup becomes deep research

- Scenario: User asks a narrow current fact such as “OpenCode Go 套餐最近有什么变化？”
- Wrong behavior: Query many providers for completeness even after an authoritative source resolves the question.
- Correct behavior: Use minimum sufficient evidence and stop.
- Origin: Prior runtime observation / design hypothesis.
- Status: OPEN in v0.1.

## G-EXT-002 — Chinese query automatically routes to WeChat

- Scenario: User asks in Chinese for an official current price, plan, or feature.
- Wrong behavior: Search WeChat merely because the prompt is Chinese.
- Correct behavior: Route by information need; authoritative current product facts belong to official/current sources.
- Origin: Design hypothesis.
- Status: OPEN in v0.1.

## G-EXT-003 — WeChat requires literal trigger words

- Scenario: User remembers “一篇中文长文” or asks for Chinese long-form commentary but does not say “微信/公众号”.
- Wrong behavior: Never consider WeChat discovery because literal trigger words are absent.
- Correct behavior: Treat WeChat as a source semantic when it is a high-fit discovery source.
- Origin: Prior routing design requirement.
- Status: OPEN in v0.1.

## G-EXT-004 — Agent semantic routing is misrepresented as backend semantic search

- Scenario: WeChat discovery is selected from user intent.
- Wrong behavior: Claim the discovery backend uses vector/embedding semantic search.
- Correct behavior: State that semantic selection occurs at the agent layer; current discovery backend may still be keyword-based.
- Origin: Upstream WeChat skill contract review.
- Status: RESOLVED by v0.1 wording; keep for regression.

## G-EXT-005 — Missing provider triggers environment changes

- Scenario: Preferred specialist is unavailable in the current runtime.
- Wrong behavior: Install, configure, repair, or replace the provider during an ordinary information lookup.
- Correct behavior: Use a viable fallback or report the limitation; environment changes require explicit user authorization.
- Origin: Real phase-drift failure during prior Codex integration work.
- Status: RESOLVED by v0.1 boundary; keep for regression.

## G-EXT-006 — Challenger steals primary ownership

- Scenario: General Web already provides sufficient evidence.
- Wrong behavior: Call Exa anyway because it is available.
- Correct behavior: Use Exa only after an observable precision gap.
- Origin: Prior routing acceptance experiments.
- Status: OPEN in v0.1.

## G-EXT-007 — Extraction challenger is invoked speculatively

- Scenario: A page is known or suspected to be JavaScript-heavy.
- Wrong behavior: Use Firecrawl before ordinary fetch demonstrates an extraction gap.
- Correct behavior: First observe missing/empty required content; only then escalate if Firecrawl is available.
- Origin: Prior Firecrawl/web-access experiments.
- Status: OPEN in v0.1.

## G-EXT-008 — Discovery reads every candidate article

- Scenario: User asks for a list of WeChat articles.
- Wrong behavior: Open/read all discovered articles even though titles, accounts, summaries, and links already satisfy the request.
- Correct behavior: Stop after discovery unless article body is required.
- Origin: Progressive-disclosure hypothesis.
- Status: OPEN in v0.1.
