# PR-34 / B8 Static Security Review Track Audit

## Scope

B8 records a static security review track for Odin-Agent-Shell v7.1.1. The review is limited to tracked source files, canon docs, schemas, registries, examples, reports, validators, tests, and CLI integration.

## What was reviewed

- Security review scope: `examples/v7_1_1/b8_security_review_scope.example.json`.
- Static surface inventory: `examples/v7_1_1/static_security_surface_inventory.example.json`.
- Trust boundary matrix: `examples/v7_1_1/trust_boundary_matrix.example.json`.
- Static security flow map: `examples/v7_1_1/static_security_flow_map.example.json`.
- Static threat model: `examples/v7_1_1/static_threat_model.example.json`.
- Security risk register: `examples/v7_1_1/security_risk_register.example.json`.
- Security control coverage: `examples/v7_1_1/security_control_coverage_matrix.example.json`.
- Static sensitive pattern review: `examples/v7_1_1/static_sensitive_pattern_review.example.json`.
- Thor/Odin effectiveness audit: `examples/v7_1_1/thor_odin_effectiveness_audit.example.json`.

## Surface inventory

The B8 inventory classifies CLI, tools, schemas, registries, reports, docs, examples, provider-policy surfaces, bridge surfaces, app-authority surfaces, receipt surfaces, and Thor-intake surfaces. It excludes `.git/`, `.thor/`, virtual environments, cache folders, build/dist folders, and generated pack artifacts.

## Trust boundary matrix

B8 records static boundary categories for app authority, provider runtime, receipt truth, Final Gate advisory posture, Thor intake, Thor pack artifacts, SDK/app bridge, storage/trace privacy, security review, target host, and release boundaries. Allowed crossings are limited to tracked-source-to-static-report style movements with explicit evidence references. Forbidden crossings include environment-to-report, provider-runtime-to-report, model-execution-to-report, network-scan-to-report, app apply, external send, Final Gate elevation, Receipt truth elevation, and Thor pack artifact commit.

## Static security flow map

B8 maps candidate input, schema validation, registry reference, report generation, receipt evidence, provider policy, Thor intake, CLI validation, and deferred external runtime flows. Runtime, provider, network, dependency-tool, and target-host flows remain deferred.

## Threat model

The static threat model records claim overreach, authority leak, provider runtime leak, sensitive term leak, path leak, unsafe file write, network or remote leak, Receipt truth elevation, Final Gate elevation, Thor pack artifact commit, security certification overclaim, target-host overclaim, release overclaim, audit-theater risk, and process-overhead risk.

## Risk register

Top static risks are claim overreach, provider runtime boundary confusion, sensitive term false confidence, Thor pack artifact commit, and runtime-only issues missed by a static track. Mitigations are explicit non-claims, candidate-only boundaries, validator checks, manifest hygiene, and deferred future tracks.

## Control coverage

Covered controls include claim boundary controls, non-claim controls, provider boundary controls, network boundary controls, API-key boundary controls, receipt boundary controls, app authority controls, file manifest hygiene, Thor artifact hygiene, security review separation controls, release boundary controls, and audit effectiveness controls. Target-host separation is partial. Dynamic runtime, dependency vulnerability tooling, and penetration-test controls are uncovered in B8.

## Sensitive pattern review

The sensitive-pattern review is source-only and pattern-based. It separates documentation terms, schema field names, possible false positives, and requires-human-review items. It does not read environment variables, does not contact external secret scanning services, and does not certify absence of secrets.

## Thor/Odin effectiveness audit

### What Thor brought

Thor brought handoff-packet discipline, repo-cognition framing, source-truth intake cues, pack-shape vocabulary, and review checklist pressure.

### Where Thor helped most

Thor helped most in handoff structure, source-truth intake, and process review prompts where task ambiguity could otherwise cause claim drift.

### Where Thor helped least

Thor helped least in deterministic local validation and repo-specific schema details, where Odin-side implementation and tests were the primary mechanism.

### Why Thor helped or did not help

Thor helped by creating repeatable review posture and reducing handoff ambiguity. It helped less where the work required direct repository edits, deterministic validators, and local test integration.

### How much Thor helped

Conservative proxy scoring places repo cognition helpfulness at 3/5 and prompt quality improvement at 4/5. These are subjective process proxies, not scientific measurements.

### What Odin brought

Odin brought deterministic schema/registry/example structure, claim-bound validators, candidate-only architecture boundaries, receipt and Final Gate separation, and Road-to-100 traceability.

### Where Odin helped most

Odin helped most in static evidence structure, report generation, validator checks, and claim boundaries.

### Where Odin helped least

Odin helped least in external repo cognition freshness and subjective process scoring.

### How much Odin helped

Conservative proxy scoring places claim boundary control at 5/5, evidence traceability at 4/5, and maintainer clarity at 4/5. These scores are process proxies only.

### Combined effect

The Thor+Odin combination improved handoff clarity, non-claim discipline, deferred-track separation, and review consistency.

### What became too heavy or redundant

The process became heavy around repeated non-claim lists, schema/registry/example multiplication, and repeated boundary wording.

### What should stay

Keep explicit non-claims, deterministic validators, small bundle identity, and source-truth intake summaries.

### What should be simplified

Simplify repeated boilerplate, centralize shared non-claim vocabulary, and separate subjective scoring from hard validation.

### What should be deferred

Defer dynamic/runtime security review, target-host security review, local provider runtime probes, and dependency vulnerability tooling to explicit future tracks with receipts.

## What was not run and why

B8 did not run penetration testing, dynamic runtime security testing, target-host testing, network scans, external security services, external secret scans, dependency vulnerability tooling, SAST tooling, provider execution, model execution, QIRC server runtime, app apply, app state mutation, external sends, Final Gate elevation, or Receipt truth elevation. Those activities are outside the B8 static scope.

## Known security gaps

- No penetration test performed.
- No dynamic runtime security test performed.
- No target-host security test performed.
- No external secret scan performed.
- No dependency vulnerability tool proof.
- No provider runtime security review.
- No network runtime security review.
- No security certification.

## Next security recommendations

Run B9 dynamic/runtime security review, target-host security review, or a local provider runtime probe only after explicit policy and receipt requirements are in place.
