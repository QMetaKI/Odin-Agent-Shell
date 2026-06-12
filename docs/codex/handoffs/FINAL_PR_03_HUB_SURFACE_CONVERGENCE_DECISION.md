# FINAL-PR-03 Hub Surface Convergence Decision

**Claim boundary:** hub_surface_registry_local_only_no_app_apply_no_external_send
**candidate_only:** true

## Decision

FINAL-PR-03 introduces a canonical surface registry for the three local hub surfaces.

## Surface assignments

| Port | Role | Owner | Canonical Entry |
|------|------|-------|----------------|
| 8765 | canonical_normal_user_entry | odin.local_hub.server | YES |
| 8877 | local_api_daemon | odin.daemon.local_api | no |
| 8878 | browser_hub_shell | odin.hub.shell | no |

## Non-destructive approach

This registry DOCUMENTS ownership only. It does NOT:
- Redirect traffic between ports
- Shut down any existing server
- Merge functionality between surfaces

## Conflict check result

Status: ok — no duplicate ports, no public bind risk.

## Not proven (required list)

- production_readiness
- live_model_inference
- app_state_mutation
- external_send_authority
