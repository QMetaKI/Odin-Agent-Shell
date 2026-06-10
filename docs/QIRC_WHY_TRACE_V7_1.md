# QIRC Why Trace v7.1

## Objective

Make Odin entblackboxend. Every important route decision should have a compact, redacted, machine-readable reason chain.

## Why Trace Fields

- centerline
- active seeds
- active archetype roles
- route score
- blocked routes
- model choice
- final gate result
- candidate DNA reference
- privacy/redaction note

## Example

```json
{
  "summary": "3B micro route selected because context was small, schema strict, and quality gain from 7B was below threshold.",
  "active_seeds": ["claim_boundary", "schema_adherence"],
  "route_score": {"3b_micro": 0.84, "7b_quality": 0.61},
  "blocked_routes": [{"route": "remote", "reason": "remote_not_allowed"}]
}
```

## Boundary

Why Trace must explain without leaking raw private app state or secrets.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
