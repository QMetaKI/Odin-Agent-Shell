# PR-25 v7.1.1 Operational Coverage / Gap Compiler Return Report

## 0. Status

PR-25 adds a deterministic static local evidence compiler for v7.1.1 operational coverage and gap classification. The report status is `local_coverage_gap_report_not_runtime_proof`.

## 1. Scope

In scope:

- Read v7.1.1 target, Road-to-100, coverage, absorption, SYSTEM_MAP, and FILE_MANIFEST inputs.
- Classify local repository evidence with explicit deterministic rules.
- Emit a stable JSON report with target-area coverage, slice coverage, gap buckets, unsupported-claim findings, and PR-26+ recommendations.
- Add structural tests for compiler determinism and fail-closed behavior.

Out of scope:

- Runtime behavior.
- Provider execution.
- Live model inference.
- QIRC server behavior.
- Windows app, tray, service, installer, or target-machine validation.
- External app integration.
- App-owned apply/state/external-send changes.

## 2. Files Added

- `tools/v7_1_1/build_operational_coverage_gap_report.py`
- `schemas/v7_1_1_operational_coverage_gap_report.schema.json`
- `reports/v7_1_1_operational_coverage_gap_report.json`
- `docs/codex/reports/PR_25_V7_1_1_OPERATIONAL_COVERAGE_GAP_COMPILER_RETURN_REPORT.md`
- `tests/test_v7_1_1_operational_coverage_gap_compiler.py`

## 3. Files Updated

- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`

## 4. Compiler Inputs

Required inputs:

- `registries/v7_1_1_operational_target_registry.json`
- `registries/v7_1_1_slice_absorption_map.json`
- `registries/v7_1_1_road_to_100_ladder.json`
- `registries/v7_1_1_road_to_100_coverage_matrix.json`
- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`

Reference inputs:

- `docs/MASTER_ARCHITECTURE_V7_1.md`
- `docs/MASTER_SPECS_V7_1.md`
- `docs/MASTER_ARCHITECTURE_V7_1_1.md`
- `docs/V7_1_1_OPERATIONAL_TARGET_SYNTHESIS.md`
- `docs/V7_1_1_ROAD_TO_100_BUILD_LADDER.md`
- `registries/real_pr_execution_registry.json`
- `registries/codex_task_registry.json`
- `registries/codex_pr_bundle_registry.json`
- `docs/rebaseline/FULL_SYSTEM_AUDIT_AFTER_LRH_PR_18.md`

## 5. Compiler Outputs

The compiler writes only the requested `--out` path. The committed generated output is:

- `reports/v7_1_1_operational_coverage_gap_report.json`

The output uses deterministic JSON ordering and the committed report was generated with:

```bash
python tools/v7_1_1/build_operational_coverage_gap_report.py --repo-root . --out reports/v7_1_1_operational_coverage_gap_report.json --generated-at-utc 2026-01-01T00:00:00Z
```

## 6. Evidence Rule Model

The compiler emits its active rule table under `evidence_rules`. The model includes:

- `missing`
- `documented_only`
- `registry_only`
- `schema_present`
- `test_present`
- `tool_present`
- `report_present`
- `receipt_present`
- `validator_present`
- `partial`
- `implemented_code_candidate`
- `external_receipt_required`
- `blocked`

Documentation, registry entries, Road-to-100 planning entries, reports, and future PR labels are not upgraded into implementation proof.

## 7. Coverage Model

Target-area records are derived from every entry in `v7_1_1_operational_target_registry.json`. Slice records are derived from every entry in `v7_1_1_road_to_100_ladder.json`.

Each target-area record includes declared status, computed status, evidence classes, evidence refs, Road-to-100 slice links, missing evidence, gap level, recommendation family, claim boundary, and non-claims.

Each slice record includes slice ID, phase ID, title, target area IDs, future PR family, dependency status, computed coverage status, evidence refs, missing evidence, claim boundary, and non-claims.

## 8. Gap Model

The report groups gaps into:

- `critical`
- `high`
- `medium`
- `low`
- `external_receipt_required`
- `blocked`

Required gap families are represented as local gap classifications rather than repository failures:

- Context Capsule builder
- Slot Forge compiler
- ModelWorkPacket enforcement
- Final Gate closure
- QIRC runtime receipts
- live model proof / model quality proof
- SDK external app proof
- target-host proof
- production/release/security certification

## 9. Unsupported Claim Scan

The compiler scans relevant docs, registries, and reports for configured affirmative claim phrases while allowing explicit non-claim, forbidden-scope, and future-evidence contexts. Findings are emitted under `unsupported_claims` for reviewer inspection.

Receipt/report convention detected in this repository:

- Reports are primarily under `reports/` and `docs/codex/reports/`.
- Proof-oriented local artifacts also exist under runtime/proof-governance naming conventions, but PR-25 does not treat those as target-host, model-quality, release, or security certification.

## 10. Next PR Recommendations

The compiler emits PR-26 through PR-39 recommendation records. Each recommendation includes the PR family, title, reason, target area IDs, slice IDs, blockers, and the `recommendation_not_implementation_proof` claim boundary.

## 11. Commands Run

Commands run locally for this PR:

```bash
python -m pip install -e .
python tools/v7_1_1/build_operational_coverage_gap_report.py --repo-root . --out reports/v7_1_1_operational_coverage_gap_report.json --generated-at-utc 2026-01-01T00:00:00Z
python -m pytest -q tests/test_v7_1_1_operational_coverage_gap_compiler.py -p no:cacheprovider
python -m odin.cli validate-all
python -m pytest -q -p no:cacheprovider
```

## 12. Results

Local result summary is recorded in the PR body and final response. The generated report covers all 33 v7.1.1 target areas and all 190 Road-to-100 slices.

## 13. Claim Boundaries

- The compiler is static local analysis only.
- The report is not runtime completion proof.
- Coverage classification is not slice completion proof.
- Recommendations are not implementation proof.
- Local reports and tests are not external receipts.

## 14. Non-Claims

- No production readiness claim.
- No release certification claim.
- No security certification claim.
- No target-host proof claim.
- No live model inference proof claim.
- No model quality proof claim.
- No QIRC server runtime proof claim.
- No provider execution claim.
- No external app integration proof claim.

## 15. Senior Reviewer Simulation

- Does this operationalize v7.1.1 without overclaiming? Yes. It converts target canon and Road-to-100 planning into static local evidence classification and repeats non-runtime claim boundaries.
- Does it read the target registries and Road-to-100 ladder? Yes. The compiler fails closed if required registries or maps are missing.
- Does it produce actionable gaps? Yes. It emits gap buckets, critical gap families, missing evidence, and next PR recommendations.
- Does it keep PR-25 narrow? Yes. The patch is limited to a compiler, report, schema, tests, and manifest/map metadata.
- Does it recommend PR-26+ clearly? Yes. The report emits PR-26 through PR-39 recommendations.
- Does it avoid false confidence? Yes. Documentation, registries, reports, and roadmap entries are never treated as runtime proof.

## 16. Senior Code Reviewer Simulation

- Is the compiler deterministic? Yes. It uses sorted file traversal, normalized string matching, stable JSON key ordering, and a caller-supplied timestamp.
- Are inputs explicit? Yes. Required and reference inputs are hard-coded and reported.
- Are outputs schema-like and testable? Yes. A schema artifact and structural tests are included.
- Does it fail closed? Yes. Missing required inputs produce a non-zero exit and no output file.
- Are evidence rules transparent? Yes. The active rule table is embedded in the output.
- Are tests strict enough? Yes. Tests check identity, shape, full target/slice coverage, references, non-claims, fail-closed behavior, and output path confinement.
- Is there no runtime/provider/model/QIRC-server execution? Yes. The compiler uses only local file reads and JSON output.
- Is there no claim-language leak? Yes. The report uses non-claim boundaries and routes scan findings to `unsupported_claims`.
