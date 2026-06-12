# PR-31 B5 Thor Receipt Bridge Prompts

claim_boundary: thor_reference_is_external_candidate_handoff_guidance_not_runtime_proof

## Future THOR_RETURN to Odin prompt

Map returned candidate work into Odin Response Packet and Trace Record fields:

- `THOR_RETURN.files_changed` -> Odin Response Packet `evidence_refs` and Trace Record `evidence_refs`.
- `THOR_RETURN.commands_run` -> Odin Response Packet `commands_run`.
- `THOR_RETURN.commands_not_run` -> Odin Response Packet `commands_not_run`.
- `THOR_RETURN.evidence_refs` -> Odin Trace Record `evidence_refs`.
- `THOR_RETURN.gaps` -> Odin Response Packet `claims_not_made` and `tests_not_run` when applicable.

## Future THOR_REVIEW to Odin prompt

Map review findings into scoped receipt evidence:

- `THOR_REVIEW.claim_findings` -> Odin Receipt Ledger `ledger_entries`.
- `THOR_REVIEW.required_fixes` -> Odin Receipt Ledger pending/deferred entries.
- `THOR_REVIEW.decision_recommendation` -> Odin Receipt Ledger review reference, not app apply authority.

## Future THOR_RECEIPT to Odin prompt

Map receipt partitions without upgrading truth:

- `THOR_RECEIPT.accepted_claim_refs` -> Odin Receipt Boundary + Receipt Ledger accepted claim refs.
- `THOR_RECEIPT.denied_claim_refs` -> Odin Receipt Boundary + Receipt Ledger denied claim refs.
- `THOR_RECEIPT.pending_claim_refs` -> Odin Receipt Boundary + Receipt Ledger pending claim refs.

No bridge prompt authorizes apply, external send, provider execution, or app state mutation.
