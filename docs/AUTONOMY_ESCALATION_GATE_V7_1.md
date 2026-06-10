# Autonomy Escalation Gate v7.1

## Purpose

The Autonomy Escalation Gate prevents Odin from drifting from candidate production into autonomous action.

## Escalation Levels

```text
A0 Observe / digest only
A1 Candidate text or data artifact
A2 Candidate action card
A3 App-owned preview / apply request
A4 App-owned apply after explicit user/app decision
A5 Forbidden for Odin: direct apply, direct send, hidden tool execution
```

Odin may operate in A0-A2. Odin may prepare A3 candidate structures. Odin may never perform A4 itself. A5 is blocked.

## Gate Inputs

- Universal Work Object
- Caller Manifest
- Output Contract
- Candidate Actions
- Semantic Bus Events
- Runtime Pack Policy
- Model Route Plan
- Why Trace

## Decision Outputs

```text
allow_candidate
reduce_to_preview
ask_app_confirmation
ask_context
block
```

## Block Conditions

Block if:

- output contract requests direct apply,
- candidate action implies external send by Odin,
- model response claims completed execution,
- runtime pack attempts to enable app mutation,
- semantic bus event requests app-state write,
- Fairy/Y* node tries to execute prose,
- provider adapter tries a non-declared side effect.

## Autonomy Score

```text
autonomy_score = tool_access + state_write + external_send + persistence + hidden_loop + self_modification
```

If autonomy_score exceeds the caller manifest threshold, Odin must block or reduce to candidate preview.

## Why it matters

This gate is the technical boundary against the Skynet-like escalation pattern:

```text
model -> tool -> hidden state change -> loop -> network -> authority
```

Odin must keep every step visible, candidate-only and app-owned.
