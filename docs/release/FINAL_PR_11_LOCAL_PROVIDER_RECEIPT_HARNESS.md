# FINAL-PR-11 Local Provider Receipt Harness

**Claim boundary:** `local_provider_receipt_harness_scoped_local_receipts_not_quality_benchmark`
**candidate_only:** true

## How the Harness Works

The local provider receipt harness provides a safe, structured way to:
1. Record that a provider is structurally recognized (`structural_evidence`)
2. Record that a provider was unavailable on a specific host (`structural_evidence`)
3. Optionally record that a provider executed on a specific host (`host_scoped_local_receipt`)

## Provider Execution Gate

Execution requires ALL of:
- `allow_local_provider_execution=True` (explicit flag)
- `ODIN_ENABLE_LOCAL_PROVIDER_EXECUTION=1` (environment variable)
- provider_id in `{ollama_candidate, llama_cpp_candidate}`
- `timeout_seconds <= 60`
- `max_input_chars <= 8000`

Default behavior (all gates off):
- `execution_allowed: false`
- `execution_performed: false`
- `model_inference: false`
- `provider_execution: false`
- `evidence_class: structural_evidence`

## Unavailable Provider Receipts

When gates pass but provider binary not found:
- `status: provider_unavailable`
- `execution_performed: false`
- `evidence_class: structural_evidence`

## Scoped Local Provider Receipts

When provider executes successfully:
- `status: scoped_local_provider_receipt`
- `execution_performed: true`
- `evidence_class: host_scoped_local_receipt`
- `scope_note: "This receipt is host-scoped. Does not generalize."`

## Evidence Class Definitions

- `structural_evidence`: Repo-local deterministic proof. Does not prove live execution.
- `host_scoped_local_receipt`: Generated on one host. Does not generalize. Does not prove model quality.
- `external_receipt_required`: Cannot be satisfied by repo-local proof alone.

## Not Proven

Even with `host_scoped_local_receipt`:
- real_model_benchmark
- model_quality_superiority
- production_readiness
- security_certification
- release_certification

## CI Safety

CI must pass without Ollama or llama.cpp installed.
Tests use skip-if-unavailable for actual provider execution.
