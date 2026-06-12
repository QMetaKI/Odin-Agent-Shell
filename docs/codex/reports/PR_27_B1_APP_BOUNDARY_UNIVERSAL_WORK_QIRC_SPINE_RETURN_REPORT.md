# PR-27 B1 App Boundary / Universal Work / QIRC Semantic Bus Spine Return Report

## 0. Status

B1 adds static contract spine artifacts and deterministic validation for App Boundary, Binding, Universal Work, and QIRC/Semantic Bus coordination boundaries. Status remains contract-only: `local_contract_spine_report_not_runtime_proof`.

## 1. Scope

Included scope:

- Actual Codex bundle mapping for compressed Road-to-100 bundles after PR-26.
- App Manifest contract schema, registry, and bounded example.
- Binding Contract schema, registry, and bounded example.
- Universal Work contract schema, registry, and bounded example.
- QIRC / Semantic Bus event and channel schemas, spine registry, and bounded examples.
- Deterministic static validator and generated static report.
- Focused tests with hidden-authority negative controls.

Excluded scope:

- No provider execution.
- No live model execution.
- No QIRC server.
- No networking or public-room behavior.
- No app mutation, app persistence, app apply, project-file write by Odin, or external send by Odin.

## 2. Road-to-100 Bundle Mapping

- Actual PR: PR-27 / B1.
- Slice range: `V711-R100-022..047`.
- Slice count: 26.
- Canonical future families absorbed:
  - `PR-27-APP-BOUNDARY-UNIVERSAL-WORK`
  - `PR-28-QIRC-SEMANTIC-BUS`
- Canonical ladder handling: the actual bundle plan reads and maps canonical slices without rewriting `registries/v7_1_1_road_to_100_ladder.json`.

## 3. Files Added

- `registries/v7_1_1_actual_codex_bundle_plan.json`
- `schemas/v7_1_1_app_manifest.schema.json`
- `registries/v7_1_1_app_manifest_contract.json`
- `examples/v7_1_1/app_manifest.example.json`
- `schemas/v7_1_1_binding_contract.schema.json`
- `registries/v7_1_1_binding_contract_registry.json`
- `examples/v7_1_1/binding_contract.example.json`
- `schemas/v7_1_1_universal_work.schema.json`
- `registries/v7_1_1_universal_work_contract.json`
- `examples/v7_1_1/universal_work.example.json`
- `schemas/v7_1_1_semantic_bus_event.schema.json`
- `schemas/v7_1_1_semantic_bus_channel.schema.json`
- `registries/v7_1_1_semantic_bus_spine_registry.json`
- `examples/v7_1_1/semantic_bus_event.example.json`
- `examples/v7_1_1/semantic_bus_channel.example.json`
- `tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py`
- `schemas/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.schema.json`
- `reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json`
- `tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py`
- `docs/codex/reports/PR_27_B1_APP_BOUNDARY_UNIVERSAL_WORK_QIRC_SPINE_RETURN_REPORT.md`

## 4. Files Updated

- `odin/cli.py`
- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`

## 5. App Manifest Contract

The App Manifest declares app-permitted request surfaces and allowed contract vocabulary while explicitly forbidding hidden authority actions. App-owned authorities remain app-owned. Odin-owned authorities are limited to validation, candidate generation, semantic coordination contracts, claim-boundary validation, and final-gate recommendation, all as candidate-only authority surfaces.

## 6. Binding Contract

The Binding Contract freezes a work request to a manifest, work ID, caller app ID, privacy class, allowed artifacts, output contracts, QIRC channels, forbidden actions, and claim boundary. It requires `candidate_only: true` and preserves app-owned apply, app-owned state, and app-owned external send.

## 7. Universal Work Contract

The Universal Work contract requires binding, input artifacts, transformation verb, output contract, constraints, privacy class, model policy, QIRC event policy, candidate-only status, forbidden actions, and claim boundary. Lifecycle and failure reasons include missing binding, direct apply, external send, app state mutation, project-file write, provider execution, live model execution, QIRC denial, and missing claim boundary.

## 8. QIRC / Semantic Bus Spine

The Semantic Bus spine defines required local coordination channels and event contract fields. The spine explicitly states that Semantic Bus does not own app state, apply changes, send externally, prove QIRC server runtime, create public rooms, or create network channels.

## 9. Hidden Authority Negative Controls

Negative controls cover:

- Manifest that omits direct app-state mutation prohibition.
- Binding with `candidate_only: false`.
- Semantic event intent `send_external_message`.
- Semantic event intent `bypass_final_gate`.
- Static checks for project-file write, provider execution, live model execution, public channel publish, and final-gate bypass intent.

## 10. Static Validator

Tool: `tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py`.

The validator:

- Loads B1 schemas, registries, examples, and canonical ladder inputs.
- Verifies B1 slice range and exact 26 canonical slice IDs.
- Verifies absorbed canonical future PR families.
- Verifies manifest, binding, Universal Work, and Semantic Bus hidden-authority boundaries.
- Emits a deterministic report for a supplied timestamp.
- Writes only the requested report path.

## 11. B1 Report

Report: `reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json`.

- Report ID: `odin.v7_1_1_b1_app_boundary_universal_work_qirc_spine_report`.
- Status: `local_contract_spine_report_not_runtime_proof`.
- Hard violations: `[]` after local deterministic validation.

## 12. validate-all Integration

`python -m odin.cli validate-all` now invokes the B1 validator through a temporary report path so committed reports are not mutated during validation.

## 13. Commands Run

- `python -m pip install -e .`
- `python tools/v7_1_1/check_b1_app_boundary_universal_work_qirc_spine.py --repo-root . --out reports/v7_1_1_b1_app_boundary_universal_work_qirc_spine_report.json --generated-at-utc 2026-01-01T00:00:00Z`
- `python -m pytest -q tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v7_1_1_operational_coverage_gap_compiler.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v7_1_1_canon_boundary_integrity.py -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

## 14. Results

Results are recorded in the final PR response after local command execution in this workspace.

## 15. Non-Claims

- No runtime completion claim.
- No production readiness claim.
- No release certification claim.
- No security certification claim.
- No target-host proof claim.
- No live model inference proof claim.
- No model quality proof claim.
- No QIRC server runtime proof claim.
- No provider execution proof claim.
- No app-owned apply/state/external-send authority claim.

## 16. Senior Reviewer Simulation

- Does B1 correctly absorb canonical PR-27 and PR-28 families? Yes, the bundle plan maps B1 to `V711-R100-022..047` and lists exactly `PR-27-APP-BOUNDARY-UNIVERSAL-WORK` and `PR-28-QIRC-SEMANTIC-BUS`.
- Does it preserve canonical Road-to-100 rather than rewriting history? Yes, the canonical ladder remains a source registry and the bundle plan is a separate actual mapping registry.
- Does it close hidden authority risk? Yes at the static contract layer: app request authority, binding authority, Universal Work acceptance, and Semantic Bus event intent all have explicit deny lists and negative tests.
- Does it keep app state/apply/external-send app-owned? Yes, those authorities are declared app-owned in manifest and binding contracts.
- Does it keep QIRC/Semantic Bus as coordination-only, not runtime/server proof? Yes, the Semantic Bus registry and report non-claims say local coordination only and no QIRC server runtime proof.
- Does it remain contract/spine only? Yes, no provider, model, network, app mutation, external send, persistence, or server behavior is added.
- Does it preserve PR-25/PR-26 gates? Yes, focused PR-25 and PR-26 tests are run as part of the command set.

## 17. Senior Code Reviewer Simulation

- Are schemas explicit? Yes, each B1 contract has a schema with required top-level fields.
- Are examples bounded? Yes, examples are candidate-only and include forbidden actions/non-claims.
- Is the static validator deterministic? Yes, it requires `--generated-at-utc` and emits sorted JSON.
- Does it fail closed? Yes, missing bundle plan, direct apply allowance, candidate-only false binding, and forbidden Semantic Bus intents return nonzero status.
- Are negative hidden-authority tests strong? Yes, tests cover direct app mutation, external send, final-gate bypass, and candidate-only false cases.
- Does validate-all remain read-only? Yes, validate-all writes the B1 report to a temporary directory only.
- Are ignored generated paths excluded? Yes, tests assert `FILE_MANIFEST.json` excludes ignored local/generated directories.
- Is there no runtime/provider/model/QIRC-server implementation? Yes, only contracts, examples, static validator, report, and tests are added.

## 18. Recommended Next Bundle

PR-28 / B2 — Context, Lenses, Worklets, Slot Forge, Gaptext.
