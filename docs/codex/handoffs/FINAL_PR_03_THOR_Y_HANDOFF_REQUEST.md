# FINAL-PR-03 Thor-Y Handoff Request

**Claim boundary:** final_pr_03_qirc_first_slice_local_only_not_public_network_not_runtime_completion
**candidate_only:** true

## Handoff Request

**From:** Odin Agent Operator
**To:** Thor-Y
**PR:** FINAL-PR-03 — QIRC Core Dev Mode

## Task

Implement FINAL-PR-03: QIRC Core first slice with local-only bus, surface registry, Dev Mode endpoints, and 40 tests.

## Scope

- Create `odin/qirc_core/` package (policy, channels, events, bus)
- Create `odin/local_hub/surface_registry.py`
- Update `odin/local_hub/server.py` with new endpoints
- Update `odin/local_hub/ui.py` with new Dev Mode IDs
- Update `odin/local_hub/demo_universal_work.py` to emit bus events
- Create test file with 40 tests
- Create validator tool

## Forbidden actions

- No provider execution
- No model inference
- No app apply
- No external send
- No public network
- No federation
- No LAN/WAN bind

## Not proven (required in proof packet)

- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
