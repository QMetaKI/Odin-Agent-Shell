# Universal Work Playground V1

**Claim boundary:** uwp_candidate_only_local_only_no_apply_no_external_send_no_shell_no_provider_no_credentials

**LRH-PR-11** — Part of the Local Runtime Hub Road-to-100 ladder.

---

## Purpose

The Universal Work Playground is a local-only, candidate-only demonstration surface that lets users submit a safe demo Universal Work packet and see it produce a Candidate Artifact with visible proof boundaries.

The Playground exists to make Odin's bounded workflow visible:

```
Safe local input
→ Universal Work packet
→ Candidate Artifact
→ Proof boundary panel
→ No app apply
→ No external send
→ No hidden execution
```

**This is a playground for demonstration only.** It does not execute work, apply candidates, send data externally, run shell commands, call providers, or claim production readiness.

---

## What This Provides

### Local-Only Universal Work Form

A bounded HTML form with safe fields only:

- `work_kind` — constrained to `safe_demo` only
- `title` — text, max 200 chars
- `intent` — text, max 500 chars
- `input_text` — textarea, max 1000 chars, no shell commands
- `constraints` — fixed checkboxes (all safety boundaries enforced, not user-editable)
- `expected_output_kind` — constrained to `candidate_artifact`

The form does not submit to remote networks. The form does not execute shell or code. The form does not call model/provider execution.

### Safe Demo Work Packet Fixtures

Located at `examples/universal_work_playground/`:

- `safe_demo_work_packet.valid.json` — a valid safe demo Universal Work packet
- `safe_demo_candidate_result.valid.json` — a valid safe demo candidate result

Both fixtures enforce:
- `candidate_only: true`
- `local_only: true`
- `app_apply: false`
- `external_send: false`
- `arbitrary_shell_execution: false`
- `provider_execution: false`
- `credential_required: false`

### Candidate Result Panel

Displays the candidate artifact result with:

- `candidate_artifact_id`
- `candidate_kind`
- `source_work_packet_id`
- `candidate_status`
- `candidate_summary`
- `claim_boundary`
- Candidate-only badge
- Not-applied-truth warning
- Proof boundaries
- Known non-proofs

The candidate result is not applied truth. No Apply button exists.

### Proof Boundary Panel

Displays all proof boundaries and known non-proofs. Displaying them does not close the gaps.

### Validation / Status Panel

Displays local validation receipt — whether safe demo work validated, candidate generated, known gaps. This is a local receipt only.

### Provider / Worker Boundary Context

Reuses PR-10 concepts:
- Providers are workers, not authority
- Disabled by default
- No credentials by default
- No live inference without receipt
- No provider execution from playground

---

## What This Does Not Prove

- **This does not apply candidate artifacts.** App owns apply. Odin does not apply.
- **This does not mutate app state.** No app-state mutation occurs.
- **This does not send externally.** No network sends, uploads, webhooks, or callbacks.
- **This does not execute arbitrary shell commands.** No shell, no command runner, no script executor.
- **This does not execute providers.** Provider execution is disabled from the playground.
- **This does not call live models unless separately receipted.** No live inference is performed.
- **This does not store or request credentials.** No credential fields exist.
- **This does not prove model quality.** No model quality claim is made.
- **This does not prove production readiness.** Not a production readiness certification.
- **This does not prove security certification.** Not a security certification.
- **This does not implement the External App Bridge.** That is LRH-PR-12.
- **Candidate result is not applied truth.** The candidate panel shows a candidate only.

---

## What This Proves

The validator `validate_universal_work_playground()` confirms:

- `universal_work_playground_static_files_exist`
- `local_only_form_present`
- `safe_demo_work_fixture_present`
- `safe_demo_candidate_result_fixture_present`
- `candidate_result_panel_present`
- `proof_boundary_panel_present`
- `validation_status_panel_present`
- `provider_worker_boundary_context_present`
- `no_app_apply_controls`
- `no_external_send_controls`
- `no_arbitrary_shell_execution_controls`
- `no_provider_execution_controls`
- `no_credential_controls`
- `candidate_result_not_applied_truth`

---

## Proof Boundaries

```
not_production_readiness_certification
not_security_certification
not_live_model_inference_proof
not_model_quality_proof
not_app_apply_proof
not_app_state_mutation_proof
not_external_send_authority_proof
not_arbitrary_shell_execution_proof
not_provider_execution_proof
not_credential_handling_proof
not_full_live_universal_work_backend_coverage
not_external_app_bridge_proof
candidate_result_not_applied_truth
```

---

## Forbidden Scope

The Playground must not contain:

- App apply controls
- External send controls
- Arbitrary shell execution
- Free-form code execution
- Provider execution controls
- Live model calls
- Credential input fields
- Raw sensitive payload display
- Candidate-as-truth claim
- Production readiness claim
- Security certification claim
- Model quality claim
- External App Bridge behavior
- WAN/LAN API default
- Signed release packaging

---

## CLI Commands

```bash
python -m odin.cli validate-universal-work-playground
python -m odin.cli prove-browser-hub --playground
```

---

## Files

| Path | Purpose |
|------|---------|
| `odin/hub/static/universal_work_playground.js` | JS implementation of playground surfaces |
| `odin/hub/static/index.html` | HTML playground section (replaces PR-10 placeholder) |
| `odin/hub/shell.py` | `validate_universal_work_playground()` + proof packet builder |
| `examples/universal_work_playground/safe_demo_work_packet.valid.json` | Safe demo work packet fixture |
| `examples/universal_work_playground/safe_demo_candidate_result.valid.json` | Safe demo candidate result fixture |
| `docs/UNIVERSAL_WORK_PLAYGROUND_V1.md` | This document |
| `tests/test_lrh_pr_11_universal_work_playground.py` | Tests |

---

## API Usage

The Playground uses existing local surfaces where available:

- `POST /v1/universal-work` — if present and safe, used for live safe demo submission
- `GET /v1/proof-gaps` — for proof gap surface

If the live call is not safe or unavailable, the playground renders fixture-backed local demo results. The missing live backend coverage is documented as a proof gap.

Default API base: `http://127.0.0.1:8877`

No browser automation. No npm. No CDN. No external network.

---

## Boundary Notice

This playground is a local static surface only.

Not a hosted cloud UI. Not a public network API. Does not grant app apply authority.
Does not send externally. Does not execute providers. Does not prove production readiness.
Does not prove security certification. Does not prove model quality.
Candidate result is not applied truth. App-owned apply.
