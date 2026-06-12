# PR-31 B5 Thor-Odin Bridge Prep Mapping

claim_boundary: thor_reference_is_external_candidate_handoff_guidance_not_runtime_proof

## Static mapping table

| Thor source | Odin target | B5 boundary |
|---|---|---|
| `THOR_HANDOFF.kernel_binding` | Odin Binding / Work Packet refs | future intake target only |
| `THOR_RETURN.files_changed` | Odin Response Packet evidence refs + Trace Record | evidence ref mapping only |
| `THOR_RETURN.commands_run` | Odin Response Packet `commands_run` | receipt metadata only |
| `THOR_RETURN.commands_not_run` | Odin Response Packet `commands_not_run` | gap metadata only |
| `THOR_RETURN.evidence_refs` | Odin Trace Record `evidence_refs` | static evidence refs only |
| `THOR_RETURN.gaps` | Odin Response Packet `claims_not_made` / `tests_not_run` | non-claim mapping only |
| `THOR_REVIEW.claim_findings` | Odin Receipt Review Record / Receipt Ledger entries | scoped review evidence only |
| `THOR_REVIEW.required_fixes` | Odin Receipt Ledger pending/deferred entries | no auto-fix |
| `THOR_REVIEW.decision_recommendation` | Odin Receipt Ledger review refs | not app acceptance |
| `THOR_RECEIPT.accepted_claim_refs` | Odin Receipt Boundary + Receipt Ledger accepted refs | not absolute truth |
| `THOR_RECEIPT.denied_claim_refs` | Odin Receipt Boundary + Receipt Ledger denied refs | denial metadata only |
| `THOR_RECEIPT.pending_claim_refs` | Odin Receipt Boundary + Receipt Ledger pending refs | pending metadata only |
| `HANDOFF.md` / `RETURN_CONTRACT.md` | Future Odin Work Packet intake target | not imported in B5 |

B5 keeps this as static mapping only and does not execute Thor or ingest `.thor/` artifacts.
