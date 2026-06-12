# PR-32 B6 Thor Closure Receipt Mapping

claim_boundary: thor_reference_is_external_candidate_handoff_guidance_not_runtime_or_release_proof

| Thor concept | Odin B6 artifact | Static mapping |
| --- | --- | --- |
| THOR_RETURN.commands | Acceptance Evidence | command availability rows |
| THOR_RETURN.evidence | Acceptance Evidence | evidence_refs |
| THOR_RETURN.gaps | Road-to-100 Closure Report | known_gaps |
| THOR_REVIEW.claim_findings | Acceptance Harness | acceptance_results / warning_conditions |
| THOR_REVIEW.required_fixes | Acceptance Harness | blocking_conditions / improvement_actions |
| THOR_RECEIPT.accepted | Closure Checklist | completed_checks / ready_static rows |
| THOR_RECEIPT.denied | Closure Matrix | blocked_static rows |
| THOR_RECEIPT.pending | Closure Matrix | requires_human_review or deferred_to_b7_plus rows |
