# PR-26 v7.1.1 Canon Boundary Integrity Return Report

## 0. Status

PR-26 adds a deterministic static claim-boundary integrity layer for v7.1.1. Status: local scanner, registries, schema, generated report, and focused tests added. This is not runtime proof.

## 1. Scope

In scope:

- v7.1.1 claim-boundary registry.
- v7.1.1 forbidden-claim registry.
- Claim Context Classifier for local claim-bearing files.
- Boundary-integrity report and schema.
- Focused tests for hard violations, false-positive controls, ignored paths, fail-closed behavior, and PR-25 preservation.
- SYSTEM_MAP and FILE_MANIFEST visibility updates.

Out of scope / non-claim:

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

## 2. Files Added

- `registries/v7_1_1_claim_boundary_registry.json`
- `registries/v7_1_1_forbidden_claim_registry.json`
- `tools/v7_1_1/check_canon_boundary_integrity.py`
- `schemas/v7_1_1_canon_boundary_integrity_report.schema.json`
- `reports/v7_1_1_canon_boundary_integrity_report.json`
- `docs/codex/reports/PR_26_V7_1_1_CANON_BOUNDARY_INTEGRITY_RETURN_REPORT.md`
- `tests/test_v7_1_1_canon_boundary_integrity.py`

## 3. Files Updated

- `SYSTEM_MAP.json`
- `FILE_MANIFEST.json`
- `odin/cli.py`

## 4. Boundary Registry

The boundary registry records required non-claims, explicit claim boundaries, external-receipt-required claim families, allowed static/local claims, claim-bearing file patterns, and ignored path families. The registry defines boundaries; it does not make any claim true.

## 5. Forbidden Claim Registry

The forbidden-claim registry lists positive claim patterns such as production-ready, release ready, security certified, target-host proven, live model proven, model quality proven, QIRC server implemented, provider execution implemented, Windows service implemented, Windows tray implemented, external app integration proven, app apply authority implemented, external send implemented, and network/public room implemented. These phrases are forbidden only as unsupported positive claims; they are allowed in explicit pattern-definition, non-claim, future-evidence, external-receipt-required, scanner-output, or test-fixture context.

## 6. Claim Context Classifier

The classifier scans only local claim-bearing files under docs, registries, reports, schemas, tools/v7_1_1, tests, SYSTEM_MAP, and FILE_MANIFEST. It classifies occurrences into explicit context types instead of treating phrases as automatic violations.

## 7. Boundary Integrity Report

The generated report is `reports/v7_1_1_canon_boundary_integrity_report.json`. It records source refs, ignored path families, scan scope, required non-claim checks, claim-boundary checks, allowed-context findings, pattern-definition findings, test-fixture findings, hard violations, recommendations, and reviewer notes. The report is a static local claim scan, not claim truth.

## 8. Hard Violation Model

Hard violations are limited to unsupported positive forbidden claims, missing required non-claims, missing claim boundaries, and ignored-path context used as evidence. The current generated report records zero hard violations.

## 9. False Positive Controls

False positives are controlled by explicit contexts:

- forbidden registry entries are pattern-definition context;
- test fixture phrases are test-fixture context;
- non-claim and not-claimed language is allowed context;
- future evidence and external receipt required language is separated;
- generated boundary report findings are not promoted into new hard violations;
- existing scanner and claim registries remain definitional context.

## 10. validate-all Integration

`python -m odin.cli validate-all` now includes a read-only in-memory canon boundary integrity check. The validation path calls the static scanner builder without writing a report. This preserves existing validate-all behavior while adding PR-26 boundary coverage.

## 11. Commands Run

- `python -m pytest -q tests/test_v7_1_1_canon_boundary_integrity.py -p no:cacheprovider`
- `python -m pip install -e .`
- `python tools/v7_1_1/check_canon_boundary_integrity.py --repo-root . --out reports/v7_1_1_canon_boundary_integrity_report.json --generated-at-utc 2026-01-01T00:00:00Z`
- `python -m pytest -q tests/test_v7_1_1_operational_coverage_gap_compiler.py -p no:cacheprovider`
- `python -m odin.cli validate-all`
- `python -m pytest -q -p no:cacheprovider`

## 12. Results

The focused PR-26 test run passed locally. The generated boundary report has zero hard violations. Remaining command results are recorded in the final PR-26 response after execution in this workspace.

## 13. Claim Boundaries

- Canon is not runtime proof.
- Roadmap is not implementation.
- Registry is not execution.
- Report is not runtime proof.
- Local receipt is not external proof.
- Green CI is not production readiness.
- Coverage/gap report is static analysis.
- QIRC coordination is not QIRC server runtime.
- Provider seam is not provider execution.
- ModelWorkPacket schema is not live model inference.
- Small-model target is not measured improvement.
- Final gate spec is not app apply authority.
- SDK bridge spec is not external app proof.
- Windows docs are not target-host proof.
- Security language is not security certification.
- Release language requires release receipts.

## 14. Non-Claims

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
- No external app integration proof claim.
- No measured small-model performance improvement proof claim.

## 15. Senior Reviewer Simulation

- Does this prevent canon/roadmap/report language from overclaiming? Yes, within local static scan scope, it flags unsupported positive claim language unless explicit boundary context is present.
- Does this avoid false positives from the forbidden registry itself? Yes, registry pattern entries are classified as pattern-definition context.
- Does this keep PR-26 narrow? Yes, it adds registries, static scanner, schema, report, tests, and map/manifest updates only.
- Does this preserve PR-25 evidence hygiene? Yes, ignored generated/local artifact families remain excluded and tested.
- Does this make PR-27+ safer? Yes, future PRs get a local gate against claim drift.
- Are external receipt claims properly separated? Yes, external-receipt-required findings are separated from unsupported hard violations.

## 16. Senior Code Reviewer Simulation

- Is the scanner deterministic? Yes, it uses local files and caller-supplied timestamps.
- Are registries explicit? Yes, claim-boundary and forbidden-claim registries are separate explicit JSON artifacts.
- Are hard violations testable? Yes, tests inject unsupported claims and assert non-zero exits.
- Are context classes explicit? Yes, findings include context type, severity, file path, line number, phrase, and excerpt.
- Are ignored paths excluded? Yes, ignored generated/local path families are excluded from scan scope and tested.
- Does the tool fail closed? Yes, missing required registries produce hard violations and a non-zero exit.
- Are tests strict enough? Yes, tests cover registry presence, deterministic report generation, false-positive controls, hard violations, ignored paths, report path hygiene, and PR-25 preservation.
- Is no runtime/provider/model/QIRC-server behavior added? Yes, only static local scanning and validation wiring were added.

## 17. Recommended Next PR

PR-27 — App Boundary / Universal Work Contract Closure, unless a future boundary report recommends otherwise.
