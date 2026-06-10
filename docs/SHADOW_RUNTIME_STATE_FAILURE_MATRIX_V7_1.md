# Shadow Runtime State and Failure Matrix v7.1

## Canonical Success States

1. WORK_RECEIVED
2. BINDING_CHECKED
3. POLICY_CHECKED
4. EVENT_DIGEST_ACCEPTED
5. UNIVERSAL_WORK_VALIDATED
6. SEMANTIC_BUS_BATCH_STARTED
7. CONTEXT_CAPSULE_CREATED
8. SYSTEM_PROFILE_SELECTED
9. PRECOMPUTE_DONE
10. WORKLET_GRAPH_BUILT
11. SLOT_FORGED
12. MODEL_ROUTE_SELECTED
13. MODEL_WORK_PACKET_BUILT
14. MODEL_RESPONSE_PROJECTED
15. CRITIC_CASCADE_DONE
16. CANDIDATE_COMPOSED
17. FINAL_GATE_DONE
18. RESPONSE_PACKET_READY

## Canonical Failure States

- BINDING_INVALID
- PRIVACY_DENIED
- ARTIFACT_BLOCKED
- VERB_FORBIDDEN
- OUTPUT_CONTRACT_INVALID
- CONTEXT_TOO_BROAD
- MODEL_ROUTE_BLOCKED
- CLAIM_BOUNDARY_HIT
- SCHEMA_INVALID
- NEEDS_CONTEXT
- CANNOT_SAFELY_COMPLETE

## Recovery Discipline

Repair is allowed only before authority is changed. Since Odin never owns app state, recovery is always candidate-only.

Examples:

- `CONTEXT_TOO_BROAD` → split work, ask context, reduce output scope.
- `MODEL_ROUTE_BLOCKED` → lower route or return cannot-safely-complete.
- `CLAIM_BOUNDARY_HIT` → downgrade language, remove claim, request receipt.
- `SCHEMA_INVALID` → schema repair once, then block or ask context.

## Codex Conversion

Real targets:

- `odin/core/state_machine.py`
- `odin/core/failure_recovery.py`
- `odin/core/final_gate.py`

The real implementation must log terminal failure reasons in trace entries.
