# Reference Host App

**Claim boundary:** `reference_host_app_candidate_only_no_apply_no_external_send_no_state_mutation`

This is a neutral reference host app for generic app bridge demonstration.

## What This Is

A neutral fake host app that demonstrates the Odin / host app boundary:

- Host app receives Candidate Artifacts from Odin
- Host app inspects candidates using its own apply policy
- Host app decides independently whether to use candidates
- **Host app owns apply, state, and external send**
- Odin produces candidates only — does not apply, mutate state, or send externally

## What This Is Not

- Not a concrete product integration
- Not a production-ready app
- Not proof of any real app integration
- Not a hosted bridge
- Not a public gateway
- Does not include concrete app or product names

## Files

- `reference_host_app.py` — neutral host app demonstration
- `reference_host_policy.json` — host-owned apply policy fixture

## Running

```bash
python examples/reference_host_app/reference_host_app.py
```

## Proof Boundaries

- `not_production_readiness_certification`
- `not_security_certification`
- `not_hosted_bridge_proof`
- `not_public_gateway_proof`
- `not_specific_external_app_integration_proof`
- `not_app_apply_proof`
- `not_host_state_mutation_proof`
- `not_external_send_authority_proof`
- `candidate_artifact_not_applied_truth`
- `host_app_owns_apply_state_external_send`
