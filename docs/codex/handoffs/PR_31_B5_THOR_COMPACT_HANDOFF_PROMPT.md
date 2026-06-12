# PR-31 B5 Thor Compact Handoff Prompt

claim_boundary: thor_reference_is_external_candidate_handoff_guidance_not_runtime_proof

Use this compact prompt only as source-safe future handoff guidance:

> Implement Odin B5 static Storage / Trace / Receipt / Provider Policy / Local Provider Seam Prep / Thor-Odin Bridge Prep / SDK-App Bridge Prep. Preserve candidate-only boundaries, Final Gate Advisory as non-Apply-Gate, provider execution disabled by default, and app-owned apply/state/external-send authority. Return changed files, commands run, commands not run, evidence refs, gaps, and non-claims.

Required return fields for future intake:

- `files_changed`
- `commands_run`
- `commands_not_run`
- `evidence_refs`
- `gaps`
- `claim_boundary`
- `non_claims`

B5 does not treat this prompt as proof of correctness, runtime behavior, provider behavior, or app acceptance.
