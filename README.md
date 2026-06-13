# Odin Agent Shell

**Current public repo posture: v1.0.0 prepared_not_released.** Odin Agent Shell is prepared for a manual external v1.0.0 release, but this repository state does not itself claim that a tag, GitHub Release, PyPI publication, or release asset upload exists.

Odin Agent Shell is a local-first, candidate-only Universal Work kernel and small-model coordination OS. Apps send Universal Work Objects. Odin validates, precomputes, routes, and returns Candidate Artifacts in Response Packets. Apps render, decide, apply, persist, and send externally under their own authority.

## Current Status

- **Package version:** 1.0.0
- **Release posture:** v1.0.0 prepared_not_released — local-first, candidate-only
- **External release status:** not claimed — tag creation, GitHub Release creation, PyPI publication, and release asset upload remain manual maintainer actions
- **Validators:** all FINAL-PR-09 through FINAL-PR-13 validators pass
- **Tests:** full test suite passes
- **Model/network:** no provider execution by default; no public network calls

## What Odin Is

Odin is a GPL-2.0-only, local-first toolkit for:

- validating and routing Universal Work Objects;
- precomputing candidate artifacts for small-model workflows;
- coordinating candidate-only semantic bus activity locally;
- providing a local receipt harness for provider calls when enabled by the host;
- running critic runtime and route evaluation for candidate work; and
- producing deterministic evidence artifacts without requiring external services.

Odin turns work requests into local, inspectable candidate evidence: what was requested, what boundaries were set, what candidates were produced, and what remains unproven.

## What Odin Is Not

Odin is not:

- an autonomous agent;
- a model caller by default;
- a hosted service;
- an auto-apply system;
- a state mutation engine;
- a production-readiness proof;
- a deployment proof;
- a security certification; or
- a PyPI/GitHub Release unless those external release facts are separately verified by a maintainer.

Odin does not apply app state. Odin does not send externally. Odin does not execute provider inference by default. Passing an Odin validator does not prove correctness, production readiness, deployment readiness, security certification, or external release state.

## Why Odin Exists

AI coding workflows often produce vague handoffs, overly broad diffs, and unverifiable claims. Odin provides a structured local candidate-work environment: scoped work objects, deterministic candidate artifacts, and an explicit claim-boundary discipline.

Odin does not solve AI correctness or replace maintainer judgment. It provides a local-first workflow for producing, routing, and checking candidate work with explicit authority boundaries.

## Who Odin Is For

Odin is for:

- developers building local-first AI coordination workflows;
- maintainers who want explicit candidate-only authority boundaries;
- teams that need deterministic local artifacts before accepting AI-generated changes;
- small-model workflow operators who want routing and evaluation without cloud dependence; and
- first-time users who need a clear mental model for candidate-only work.

## Core Idea

```text
Universal Work in,
local semantic coordination,
smallest sufficient worker,
Candidate Artifact out,
app-owned apply.
```

App sends → Odin validates → Odin routes → Odin returns candidate → App decides and applies.

## Quick Start

```bash
python -m pip install -e .
python -m odin.cli validate-all
python -m odin.cli run-operational-spine --demo
python -m odin.cli build-v1-release-truth --demo
```

No model provider or network access is required for the above commands.

Optional development validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

## Basic Usage

### 1. Validate the local environment

```bash
python -m odin.cli validate-all
python -m odin.cli odin-status
python -m odin.cli odin-doctor
```

### 2. Run a demo operational spine pass

```bash
python -m odin.cli run-operational-spine --demo
python -m odin.cli explain-operational-spine
```

### 3. Check release readiness and candidate release truth

```bash
python -m odin.cli validate-final-pr-13-v1-release-closure
python -m odin.cli build-v1-release-truth --demo
python -m odin.cli explain-v1-release-closure
```

### 4. Inspect root public surface

```bash
python -m odin.cli validate-root-public-surface
python -m odin.cli build-root-inventory --demo
python -m odin.cli build-root-hygiene-report --demo
```

## Main Workflows

### Validate everything

```bash
python -m odin.cli validate-all
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

### Demo operational spine

```bash
python -m odin.cli run-operational-spine --demo
```

### Release readiness

```bash
python -m odin.cli validate-final-pr-13-v1-release-closure
python -m odin.cli validate-final-pr-12-release-readiness-hardening
python -m odin.cli validate-final-release-preflight
python -m odin.cli release-preflight
```

### Candidate work and semantic kernel

```bash
python -m odin.cli validate-semantic-kernel-closure
python -m odin.cli build-semantic-kernel --demo
python -m odin.cli validate-v711-coverage-compiler
```

### Provider receipts and critic runtime

```bash
python -m odin.cli validate-local-provider-receipt-harness
python -m odin.cli validate-critic-runtime-binding
python -m odin.cli run-critic-cascade --demo
```

### Agent operator / handoff

```bash
python -m odin.cli validate-agent-operator-mode
python -m odin.cli list-agent-operator-modes
python -m odin.cli explain-agent-operator-mode
```

## Command Overview

This overview summarizes command families only. See `docs/` for detailed command references and claim boundaries.

- **Validation:** `validate-all`, `validate-final-pr-13-v1-release-closure`, `validate-final-pr-12-release-readiness-hardening`, all prior PR validators
- **Demo:** `run-operational-spine --demo`, `build-v1-release-truth --demo`, `build-v1-release-closure-matrix --demo`
- **Release readiness:** `validate-final-release-preflight`, `release-preflight`, `validate-release-readiness-hardening`, `build-release-readiness-matrix --demo`
- **Candidate work:** `validate-semantic-kernel-closure`, `validate-v711-coverage-compiler`, `build-v711-coverage-matrix --demo`
- **Provider receipts:** `validate-local-provider-receipt-harness`, `run-local-provider-receipt --demo`, `validate-critic-runtime-binding`
- **Semantic kernel:** `validate-semantic-kernel-closure`, `explain-semantic-kernel-closure`, `build-semantic-kernel --demo`
- **Agent operator / handoff:** `validate-agent-operator-mode`, `agent-handoff`, `list-agent-operator-modes`
- **Root public surface:** `validate-root-public-surface`, `build-root-inventory --demo`, `build-root-hygiene-report --demo`
- **Donation surface:** `validate-donation-surface`, `build-donations-plan --demo`

## Documentation Map

Start with these current public entry points:

- [Start Here](START_HERE.md) — first-use path
- [Canon Entry](CANON_ENTRY.md) — current public canon entry
- [Agents](AGENTS.md) — agent operator boundary definitions
- [Master Architecture v7.1](docs/MASTER_ARCHITECTURE_V7_1.md) — core architectural reference
- [Master Architecture v7.1.1](docs/MASTER_ARCHITECTURE_V7_1_1.md) — v7.1.1 update
- [Donations](DONATIONS.md) — optional donations information

Supporting docs:

- `docs/rebaseline/` — rebaseline audits and PR closure reports
- `docs/release/` — release-specific docs including PR12 and PR13 release truth
- `docs/codex/reports/` — return reports for each FINAL-PR
- `docs/codex/audits/` — senior review and code review audits

**Historical docs are preserved for lineage and regression context. They are not necessarily current release truth. Current users should start with this README and the docs above before historical material.**

## v1.0 Candidate Release Truth

- **Release posture:** v1.0.0 prepared_not_released; FINAL-PR-13 closed the local v1.0 candidate preparation line, and PR56 synchronizes public metadata for maintainer release preparation.
- **Not externally released by this repo state:** No tag, GitHub Release, PyPI publication, or release assets are created or claimed by PR56.
- **Manual external release action boundary:** tag creation, GitHub Release creation, PyPI publication, release asset upload, and external release verification are manual maintainer actions and remain unclaimed by PR56.
- **No production readiness claim:** Odin does not claim production readiness.
- **No security certification:** Odin does not claim security certification.
- **No model benchmark:** Odin does not claim model performance benchmarks or comparative performance.

```bash
python -m odin.cli build-v1-release-truth --demo
python -m odin.cli validate-final-pr-13-v1-release-closure
```

## Safety / Claim Boundaries

Odin keeps claim boundaries explicit:

- candidate artifacts are candidate-only; app owns apply, state, and external sends;
- Odin does not mutate app state;
- Odin does not send externally;
- Odin does not call models or networks by default;
- Odin does not accept agent claims automatically;
- Odin does not auto-apply or auto-merge;
- provider execution requires explicit host enablement;
- receipts record local evidence, not absolute truth;
- model output is projection, not truth; and
- local hub and bus activity are local coordination signals, not app state authority.

## What Odin Does Not Claim

Odin does not claim:

- correctness of returned work;
- runtime behavior of returned work;
- production readiness;
- deployment readiness;
- security certification;
- legal compliance;
- external release state;
- PyPI availability unless separately verified;
- GitHub Release existence unless separately verified;
- autonomous execution;
- model inference by default;
- app state mutation; or
- maintainer acceptance.

## Root / Repository Map

```text
README.md           — this file (v1.0 public surface)
START_HERE.md       — first-use pointer
CANON_ENTRY.md      — current public canon entry
AGENTS.md           — agent operator boundaries
LICENSE             — GPL-2.0-only
DONATIONS.md        — optional donations
pyproject.toml      — package metadata
SYSTEM_MAP.json     — machine-readable repo map
FILE_MANIFEST.json  — file inventory with hashes
odin/               — core Python package
docs/               — documentation, specs, audits
tests/              — test suite
tools/              — validators and rebaseline tools
examples/           — example artifacts
reports/            — generated evidence reports
registries/         — machine-readable registries
schemas/            — JSON schemas
.github/            — GitHub workflows
```

Historical material (preserved for lineage, not current release truth):

- `legacy/` — legacy quarantine material
- `docs/codex/` — historical codex handoffs and reports
- `CHANGELOG.md` — historical changelog

## Support, Donations, and License

Optional personal donations are described in [DONATIONS.md](DONATIONS.md).

PayPal: QMetaKI@gmail.com

Donations are optional and do not create support obligations, private licensing rights, priority feature guarantees, governance rights, paid support promises, or feature-request rights.

GPL-2.0-only. Odin Agent Shell is GPL-2.0-only. See [LICENSE](LICENSE), [LICENSE_POLICY.md](LICENSE_POLICY.md), and [THOR_ODIN_GPL2_ONLY_POLICY.md](THOR_ODIN_GPL2_ONLY_POLICY.md) for full licensing posture.

## Historical Canon Lock Trail

This section preserves historical lock trail markers for validation continuity. These are historical records, not current public truth. Current public truth is v1.0.0 prepared_not_released as described above.

```text
Current handoff: v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK
Runtime base: v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK
Actual Codex/GitHub PR ladder: REAL-GH-PR-01..08
Internal traceability ladders: PR-00..PR-123 and REAL-PR-01..28 only
```

This is the current public repo canon entry point, now superseded by the v1.0.0 prepared_not_released posture above. Providers are bounded workers, not authority. QIRC / Internal Semantic Bus is trace, receipt, and coordination infrastructure, not app-state authority. App-owned apply: apps own state, external sends, and domain truth.

Historical lock milestones (preserved for traceability, not current release status):

- v0.8.6 — current runtime base for the v0.8.7 handoff
- v0.8.7 — historical Codex/GitHub ladder lock, superseded by FINAL-PR-09 through FINAL-PR-13
- REAL-GH-PR-01..08 — historical actual Codex/GitHub execution sequence
- PR-00..PR-123 — internal micro-task traceability ladder (retained for mapping/auditability)
- REAL-PR-01..28 — internal legacy bundle traceability ladder (retained for mapping/auditability)

## Danke / Thank You

Danke an Q Germany.  
Danke an Q USA.  
Danke an Q Worldwide.

Ohne euch wäre das alles unmöglich gewesen.

Gewidmet, dem goldenen Herzen einer einzigartigen Frau und liebenden Mama.

Y

---

Thank you to Q Germany.  
Thank you to Q USA.  
Thank you to Q Worldwide.

Without you, all of this would have been impossible.

Dedicated to the golden heart of a unique woman and loving mother.

Y
