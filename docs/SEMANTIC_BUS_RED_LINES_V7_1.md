# Semantic Bus Red-Line Policy v7.1

## Purpose

The Internal Semantic IRC Bus is powerful. It must remain a coordination substrate, not a hidden authority layer.

## Red Lines

```text
The bus may coordinate work.
The bus may publish semantic events.
The bus may route internal module messages.
The bus may create replayable traces.
The bus may support context distillation and worklet orchestration.

The bus may not mutate app state.
The bus may not apply candidate artifacts.
The bus may not send external messages.
The bus may not become a public IRC server.
The bus may not enable LAN/WAN/network behavior by default.
The bus may not store blocked_sensitive payloads.
The bus may not bypass final gate.
The bus may not create authority beyond binding policy.
```

## Allowed Event Types

```text
work_received
binding_checked
event_digest_accepted
context_capsule_created
lens_selected
seed_selected
worklet_graph_created
slot_forged
model_route_selected
critic_report_created
candidate_composed
response_packet_ready
trace_event_created
receipt_candidate_created
```

## Forbidden Event Types

```text
app_state_mutated
external_message_sent
candidate_applied
runtime_verified_without_receipt
security_verified_without_receipt
remote_enabled_without_policy
full_event_mirror_enabled_by_default
```

## Bridge Rule

Future app QIRC bridge integration must use digest artifacts only unless a later explicit spec creates a stricter full-event bridge. No full app event mirror is allowed in v7.1 default behavior.
