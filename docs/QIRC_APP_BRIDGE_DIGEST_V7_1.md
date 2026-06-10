# QIRC App Bridge Digest v7.1

## Objective

Prepare Odin to consume future app-owned QIRC/Event systems via digest-only bridges. Odin must not become app QIRC.

## Bridge Direction

```text
App Event System → app-owned digest → Odin QIRC Hot Window → candidate response → app decides
```

## Allowed

Odin may receive redacted event summaries, active task states, claim boundary markers and context hints.

## Forbidden

Odin may not mirror full app state, mutate app state, publish app mutation events, consume secrets, or own the app event system.

## Review Rule

Any app bridge expansion beyond digest mode must be a separate explicit PR with security review.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.

## Required Phrase: Odin may not become app QIRC

Odin may not become app QIRC. Odin receives app-owned digests only, then returns candidate artifacts only.
