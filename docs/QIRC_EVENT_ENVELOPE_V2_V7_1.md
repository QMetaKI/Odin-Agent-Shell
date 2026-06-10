# QIRC Event Envelope v2 v7.1

## Objective

Define the event envelope used by Odin QIRC Gold Spine. Version 2 extends the earlier semantic event envelope with centerline references, ring data, authority scope, payload indirection, cost/risk fields and why-trace linkage.

## Envelope Shape

```json
{
  "artifact_kind": "odin_qirc_event",
  "protocol_version": "7.1",
  "event_id": "QIRC-EVT-001",
  "channel": "#seed.activate",
  "event_type": "seed_activation_completed",
  "work_id": "WORK-001",
  "trace_id": "TRACE-001",
  "centerline_id": "CENTER-001",
  "ring": "R3",
  "source_module": "seed_archetype_economy",
  "authority_scope": "odin_internal_only",
  "privacy_class": "local_only",
  "state_digest": "sha256...",
  "payload_ref": "obj://qirc/payloads/...",
  "payload_summary": {"active_seed_count": 12},
  "cost": {"tokens_saved_estimate": 320, "latency_ms": 4},
  "risk": {"authority_drift": "low", "privacy": "low"},
  "requires_receipt": false,
  "created_at": "timestamp"
}
```

## Required Fields

Every QIRC event requires `event_id`, `channel`, `event_type`, `trace_id`, `authority_scope`, `privacy_class`, `created_at`. Work-related events also require `work_id`. Centerline-related events require `centerline_id`. Ring events require `ring`.

## Payload Policy

Large payloads must use `payload_ref`. The `payload_summary` must be small, redacted and safe to display in traces. Raw secrets must never enter channel names, topics or summaries.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.
