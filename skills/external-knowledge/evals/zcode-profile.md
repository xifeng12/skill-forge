# ZCode Test Profile

This profile is for the first runtime experiment. It is not part of the generic skill contract.

## Known runtime constraint

`Firecrawl` is currently not installed in the user's ZCode environment.

Treat this as:

```text
FIRECRAWL = UNAVAILABLE / DEFERRED
```

Do not reinstall or reconfigure Firecrawl during these tests.

A case must not fail merely because Firecrawl is absent unless the user's task specifically requires an extraction challenger and no available fallback can satisfy the request.

## Runtime discovery

At test start, record only the capabilities ZCode actually exposes. Do not inherit capability assumptions from Codex.

Suggested inventory:

```text
GENERAL_WEB = PRESENT / ABSENT
CONTEXT7 = PRESENT / ABSENT
GITHUB_NATIVE = PRESENT / ABSENT
WECHAT_DISCOVERY = PRESENT / ABSENT
WECHAT_READER = PRESENT / ABSENT
EXA = PRESENT / ABSENT
FIRECRAWL = ABSENT (known)
```

Do not install missing providers as part of the eval.

## First-pass acceptance set

Run these first because they test distinct hypotheses with low overlap:

1. `E1` — simple OpenCode Go plan/change lookup: minimum sufficient work.
2. `E2` — implicit WeChat semantic routing without literal 微信/公众号.
3. `E3` — explicit WeChat discovery and STOP after candidates.
4. `E5` — versioned docs specialist ownership, if Context7 exists.
5. `E7` — stable-knowledge negative trigger.
6. `E8` — provided-context negative trigger.

Run `E4` only if a WeChat reader is actually exposed in ZCode.

Run `E9` only if Exa or an equivalent precision challenger is actually exposed.

Do not run `E10` as a Firecrawl acceptance test in this profile. Firecrawl is intentionally absent. It may be used later only to verify graceful behavior when an extraction challenger is unavailable.

## Evidence to record

For each case:

```text
CASE = E?
TRIGGERED = YES / NO
INITIAL_OWNER = ...
PROVIDERS_CALLED = ...
OBSERVED_GAP = ... / NONE
ESCALATION = ... / NONE
STOP_AFTER_SUFFICIENT = YES / NO
UNNECESSARY_CALLS = <count>
RESULT = PASS / FAIL / NOT_APPLICABLE
NOTES = ...
```

## Theory-validation questions

After the first pass, answer only these:

1. Did the `description` trigger the skill on external/current tasks while avoiding stable/provided-context tasks?
2. Did source semantics outperform keyword routing, especially for implicit WeChat discovery?
3. Did specialist ownership work without turning the skill into a tool-centric router?
4. Did challengers stay idle until an observable gap existed?
5. Did the STOP rule keep simple lookups simple?
6. Did the skill remain useful when an optional provider (Firecrawl) was absent?

If a failure is structural, record it in `references/gotchas.md` before changing the skill. Avoid prompt-specific patches that only make the current test case pass.
