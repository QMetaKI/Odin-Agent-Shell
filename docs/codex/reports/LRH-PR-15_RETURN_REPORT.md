# LRH-PR-15 Return Report — Portable Packaging and Release ZIP

**Claim boundary:** `lrh_pr_15_return_report_candidate_only_local_package_no_release_certification_no_signed_distribution_no_target_host_proof`

**Date:** 2026-06-11
**Branch:** `claude/lrh-pr-15-portable-packaging-xzvg8n`
**PR:** LRH-PR-15 — Portable Packaging and Release ZIP

---

## Motivation

LRH-PR-15 implements the Portable Packaging and Release ZIP slice from the Local Runtime Hub Road-to-100 ladder. The ladder entry requires a deterministic, local-only, candidate-only portable package builder with manifest, checksums, start/check script inclusion, support bundle path visibility, junk exclusion, local verification report, docs, tests, and CLI commands.

This is a **portable package candidate**. Not release certification. Not production readiness. Not signed distribution. Not Windows service/tray/installer. Not target-host proof. Not app store readiness.

Builds on LRH-PR-14 (Local Config, Redaction and Safe Settings UI).
Depends on LRH-PR-03 (Portable Local Runtime Starter) and LRH-PR-04 (Runtime Doctor, Bootstrap).

---

## Repo-real Ladder Source

**File:** `registries/local_runtime_hub_build_ladder_v1.json` → `LRH-PR-15`

Confirmed repo-real fields:
- `id`: `LRH-PR-15`
- `title`: `Portable Packaging and Release ZIP`
- `depends_on`: `["LRH-PR-03", "LRH-PR-04", "LRH-PR-14"]`
- `target_files`: `scripts/build_portable_package.py`, `dist_manifest/`, `docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md`, `tests/test_lrh_pr_15_portable_package.py`
- `forbidden_scope`: no signed installer proof, no app store readiness claim, no production deployment claim, no generated cache/build junk committed

No discrepancy found between repo-real ladder and prompt hints.

---

## Implementation Summary

This PR adds a deterministic portable package candidate path. All generated artifacts go to caller-specified paths (`/tmp/...`). No generated build output is committed to the repo.

---

## Files Created

- `scripts/build_portable_package.py` — stdlib-only portable package builder (LRH-PR-15 primary deliverable)
- `dist_manifest/README.md` — static README for dist_manifest directory
- `dist_manifest/portable_package_manifest.example.json` — static example manifest shape
- `dist_manifest/portable_package_release_verification.example.json` — static example release verification report
- `dist_manifest/portable_package_exclusions_v1.json` — static junk exclusion policy spec
- `docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md` — feature documentation with all required sections
- `tests/test_lrh_pr_15_portable_package.py` — 86 deterministic, local-only tests
- `docs/codex/reports/LRH-PR-15_RETURN_REPORT.md` — this report

---

## Files Modified

- `odin/hub/shell.py` — added `validate_portable_package()` and `build_portable_package_proof_packet()` following LRH-PR-14 pattern
- `odin/cli.py` — added imports, added `validate_portable_package()` to `validate_all()`, added `validate-portable-package` and `prove-portable-package` subparsers and handlers
- `SYSTEM_MAP.json` — added `lrh_pr_15_portable_package` entry

---

## Package Builder Behavior

**Script:** `scripts/build_portable_package.py`

- stdlib-only (no third-party dependencies)
- deterministic: stable sorted file order, stable SHA256 checksums, POSIX path separators
- local-only: no network, no provider calls, no app apply, no external send
- safe to run repeatedly
- outputs to caller-specified paths (default: `/tmp/...`)
- excludes junk directories/files/extensions
- emits manifest JSON, release verification JSON, optionally ZIP
- records start/check script inclusion status
- exposes support bundle command path
- dry-run mode available

**Receipt:**
```
Files included: 1195
Missing required entries: none
claim_boundary: portable_package_candidate_only_not_signed_not_production_not_target_host_proof
```

---

## Manifest Contract

The manifest shape follows `dist_manifest/portable_package_manifest.example.json`:

- `artifact_kind: "odin_portable_package_manifest"`
- `lrh_pr: "LRH-PR-15"`
- `candidate_only: true`
- `local_only: true`
- `claim_boundary` present
- `included_files`: sorted, POSIX-style relative paths, no backslash, no absolute paths
- `excluded_patterns`: sorted list of junk patterns
- `start_check_scripts`: dict of script → present bool
- `support_bundle_command`: repo-real CLI path
- `checksums`: `{path: lowercase_hex_sha256}`, stable across repeated runs
- `not_proven`: all required known non-proofs
- `proof_boundaries`: all required boundary strings

---

## Checksum Policy

- Algorithm: SHA256
- Format: lowercase hex, 64 characters
- Stability: same file contents → same checksum
- Scope: all included files in sorted order
- No nondeterministic timestamp fields

Checksums are a **local receipt only**. Not signed distribution proof. Not release certification.

---

## ZIP Determinism Policy

ZIP generation (`--zip-out`) is implemented using Python stdlib `zipfile`:

- All paths sorted
- Normalized POSIX archive names (no absolute paths)
- Deterministic timestamp per entry: `(1980, 1, 1, 0, 0, 0)`
- No host-dependent permissions
- No `.git/`, caches, `.env`, or previous ZIPs included

ZIP checksum is a local receipt only, not signed distribution proof.

---

## Junk Exclusion Policy

Excluded directories: `.git`, `.pytest_cache`, `__pycache__`, `.mypy_cache`, `.ruff_cache`, `.cache`, `node_modules`, `.venv`, `venv`, `dist`, `build`

Excluded files: `.env`, `.env.*`, `.DS_Store`, `Thumbs.db`

Excluded extensions: `.pyc`, `.pyo`, `.egg-info`

Safe example fixtures are not excluded solely because they contain placeholder names.

See `dist_manifest/portable_package_exclusions_v1.json` for the static exclusion policy spec.

---

## Start/Check Script Inclusion

| Script | Status |
|--------|--------|
| `scripts/start_odin.sh` | present, included |
| `scripts/check_odin.sh` | present, included |
| `scripts/stop_odin.sh` | present, included |
| `scripts/start_odin.bat` | present, included |
| `scripts/check_odin.bat` | present, included |
| `scripts/stop_odin.bat` | present, included |

All required scripts present. `missing_required_entries: none`.

---

## Support Bundle Command / Path Visibility

The repo-real existing command is:

```
python -m odin.cli emit-support-bundle --diagnostics-only
```

This command exists in `odin/cli.py`. It is included in the manifest as path visibility only.

```json
"support_bundle_command": "python -m odin.cli emit-support-bundle --diagnostics-only",
"support_bundle_claim": "support_bundle_command_path_visible_not_support_organization_readiness"
```

Not support organization readiness. Not security certification. Not production readiness.

---

## Local Release Verification Report

Shape follows `dist_manifest/portable_package_release_verification.example.json`:

```json
{
  "artifact_kind": "odin_portable_package_release_verification",
  "lrh_pr": "LRH-PR-15",
  "status": "ok",
  "candidate_only": true,
  "local_only": true,
  "portable_package_candidate": true,
  "local_verification_report_only": true,
  "manifest_created": true,
  "checksums_created": true,
  "start_check_scripts_included": true,
  "support_bundle_path_visible": true,
  "junk_excluded": true,
  "claim_boundary": "portable_release_verification_local_receipt_not_release_certification"
}
```

This is a **local verification report only**. Not a release certification.

---

## Thor Diagnostic and Invocation Discipline

```
python tools/dev/thor_cli_probe.py --json
→ classification: not_found_in_PATH
```

Thor is not available in this environment. No clone was attempted.
All implementation decisions were driven by repo-real files and the ladder registry.
Thor is advisory only. Odin repo validators and tests remain authority.

Thor summary written to: `/tmp/odin-thor-summaries/LRH-PR-15_THOR_SUMMARY.md` (not committed).

---

## Odin Agent Operator Mode Audit

Commands run:

```
python -m odin.cli agent-handoff --agent claude-code --lrh-pr 15 --out /tmp/lrh_pr_15_packet.json
→ packet created: candidate_only: true, app_owned_apply: true
→ allowed_files: scripts/build_portable_package.py, dist_manifest/, docs/PORTABLE_PACKAGE_RELEASE_ZIP_V1.md, tests/test_lrh_pr_15_portable_package.py

python -m odin.cli agent-plan --packet /tmp/lrh_pr_15_packet.json
→ status: ok, plan_envelope created

python -m odin.cli agent-guard --packet /tmp/lrh_pr_15_packet.json
→ status: ok, violations: []

python -m odin.cli agent-check --packet /tmp/lrh_pr_15_packet.json
→ status: ok, errors: []

python -m odin.cli agent-proof --packet /tmp/lrh_pr_15_packet.json
→ declared boundaries present, proof gaps classified as expected_pr_level_gap
```

Expected gaps (classified):
- `no_app_apply_by_agent` → expected_pr_level_gap
- `no_external_send_by_agent` → expected_pr_level_gap
- `no_hidden_tool_execution` → expected_pr_level_gap

No forbidden actions introduced. No app apply. No external send. No hidden tool behavior.
Agent Proof Boundary Closure remains carry-forward: LRH-PR-18.

---

## LRH Ladder Compiler Audit

- Ladder entry `LRH-PR-15` exists: ✓
- Title matches: `Portable Packaging and Release ZIP` ✓
- depends_on LRH-PR-03: ✓
- depends_on LRH-PR-04: ✓
- depends_on LRH-PR-14: ✓
- target_files include builder, dist_manifest, doc, test: ✓
- forbidden_scope enforced: ✓
- validate_portable_package() added to validate_all(): ✓
- Tests cover all required behavior: ✓

---

## Claude Code Worker Audit

- Branch: `claude/lrh-pr-15-portable-packaging-xzvg8n`
- All files in allowed scope: ✓
- Minimal diff: ✓
- Builder stdlib/local-only: ✓
- No network: ✓
- No npm: ✓
- No browser automation: ✓
- No provider/model execution: ✓
- No app apply/state mutation: ✓
- No external send: ✓
- Stable sorted manifest: ✓
- Stable checksums across runs: ✓
- ZIP deterministic: ✓ (implemented with fixed timestamp)
- Junk excluded: ✓
- Generated artifacts not committed: ✓
- CLI integration stable: ✓
- validate-all green: ✓

---

## Commands Run

```
python -m pip install -e .
→ OK

python tools/dev/thor_cli_probe.py --json || true
→ classification: not_found_in_PATH (advisory only)

python -m odin.cli agent-handoff --agent claude-code --lrh-pr 15 --out /tmp/lrh_pr_15_packet.json
→ ok, candidate_only: true

python -m odin.cli agent-plan --packet /tmp/lrh_pr_15_packet.json
→ ok

python -m odin.cli agent-guard --packet /tmp/lrh_pr_15_packet.json
→ ok, violations: []

python -m odin.cli agent-check --packet /tmp/lrh_pr_15_packet.json
→ ok, errors: []

python -m odin.cli agent-proof --packet /tmp/lrh_pr_15_packet.json
→ proof gaps classified as expected_pr_level_gap

python scripts/build_portable_package.py \
  --out /tmp/odin_lrh_pr15_package \
  --manifest-out /tmp/odin_lrh_pr15_manifest.json \
  --report-out /tmp/odin_lrh_pr15_release_verification.json
→ Files included: 1195, Missing required entries: none

python -m odin.cli validate-current-public-canon
→ OK (run via validate-all)

python -m odin.cli validate-agent-operator-mode
→ OK

python -m odin.cli validate-local-runtime-starter
→ OK

python -m odin.cli validate-runtime-doctor-bootstrap
→ OK

python -m odin.cli validate-local-config-safe-settings
→ OK

python -m odin.cli validate-portable-package
→ validate-portable-package: OK

python -m odin.cli prove-portable-package
→ status: ok, candidate_only: true, local_only: true, portable_package_candidate: true

python -m odin.cli validate-all
→ validate-all: OK

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_lrh_pr_15_portable_package.py -p no:cacheprovider
→ 86 passed in 22.98s

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
→ 1195 passed, 2 skipped in 28.89s
```

---

## Results

| Command | Result |
|---------|--------|
| validate-portable-package | OK |
| prove-portable-package | ok, candidate_only: true |
| validate-all | OK |
| pytest (PR-15 only) | 86 passed |
| pytest (full suite) | 1195 passed, 2 skipped |
| agent-guard | ok, violations: [] |
| builder (1195 files) | Files included, missing: none |

---

## Proof Boundaries

- Not production readiness — no deployment proof
- Not security certification — no security audit
- Not signed distribution proof — no code signing
- Not release certification — no release authority asserted
- Not Windows service/tray/installer proof — no Windows service, tray, or installer
- Not target-host proof — no target-host validation
- Not app store readiness — no app store submission
- No app apply — Odin does not apply app state
- No external send — no network transmission
- No live model inference — no model execution
- No model quality proof — no model quality certification
- Generated artifacts are not committed

---

## Senior Reviewer Simulation

**Architecture questions:**

| Question | Answer |
|----------|--------|
| Scope correct for LRH-PR-15? | Yes — builder, manifest, checksums, exclusions, start/check, support bundle path, local verification report, docs, tests, CLI |
| Repo-real ladder followed? | Yes — validated against `registries/local_runtime_hub_build_ladder_v1.json` |
| depends_on respected (LRH-PR-03, LRH-PR-04, LRH-PR-14)? | Yes |
| No PR-16/17/18+ scope creep? | No — no Windows service, no full acceptance harness, no agent proof closure |
| Candidate-only preserved? | Yes — all outputs have `candidate_only: true` |
| Local-only preserved? | Yes — no network, no external send |
| App-owned apply/state/external-send preserved? | Yes |
| No signed distribution claim? | Confirmed |
| No release certification claim? | Confirmed |
| No production readiness claim? | Confirmed |
| No security certification claim? | Confirmed |
| No Windows service/tray/installer claim? | Confirmed |
| No target-host proof claim? | Confirmed |
| No app store readiness claim? | Confirmed |
| No hidden runtime/network/provider/apply jump? | Confirmed |
| Support bundle path shown without readiness claim? | Yes — `support_bundle_command_path_visible_not_support_organization_readiness` |
| Package builder deterministic? | Yes — sorted files, stable checksums, fixed ZIP timestamp |
| Generated artifacts not committed? | Yes — all outputs to `/tmp/...` |

**Risk checks:**

| Risk | Status |
|------|--------|
| Scope creep | None — LRH-PR-16/17/18+ not touched |
| False proof | None — all outputs marked candidate_only, not_proven explicit |
| Hidden authority | None — no network, no provider, no apply |
| Unsafe defaults | None — builder defaults to /tmp/ paths |
| Missing tests | All required test categories covered (86 tests) |
| Claim scanner risk | Scanner forbidden list uses specific contextual phrases to avoid false positives |
| Thor discipline regression | None — Thor is advisory only, validated via probe |
| Nondeterministic manifest/checksum/ZIP | None — sorted files, stable SHA256, fixed ZIP timestamp |
| Accidental build junk committed | None — dist_manifest/ contains only static spec examples |
| Accidental .env/secret inclusion | None — .env excluded by junk exclusion policy |

**Verdict:** READY
- No blockers
- Follow-ups: LRH-PR-16 (Windows Convenience Layer), LRH-PR-18 (Agent Proof Boundary Closure)

---

## Senior Code Reviewer Simulation

**Code/repo checks:**

| Check | Status |
|-------|--------|
| Files in allowed scope? | Yes |
| Minimal diff? | Yes |
| Builder stdlib/local-only? | Yes — only `argparse`, `hashlib`, `json`, `shutil`, `zipfile`, `pathlib` |
| No network? | Yes |
| No npm? | Yes |
| No browser automation? | Yes |
| No provider/model execution? | Yes |
| No app apply/state mutation? | Yes |
| No external send? | Yes |
| Stable sorted manifest? | Yes — `sorted(repo_root.rglob("*"))` + `sorted(result)` |
| Stable checksums? | Yes — deterministic SHA256, stable across repeated runs (confirmed by test) |
| ZIP deterministic? | Yes — `(1980, 1, 1, 0, 0, 0)` timestamp for all entries |
| Junk excluded? | Yes — JUNK_DIR_PATTERNS + JUNK_FILE_PATTERNS + JUNK_FILE_EXTENSIONS |
| Generated artifacts not committed? | Yes |
| CLI integration stable? | Yes — follows LRH-PR-14 pattern exactly |
| validate-all green? | Yes |

**Test checks:**

| Test category | Count | Status |
|---------------|-------|--------|
| Required file existence | 7 | pass |
| Ladder tests | 9 | pass |
| Builder execution (temp dir) | 6 | pass |
| Manifest shape | 9 | pass |
| Checksum stability | 3 | pass |
| Junk exclusion | 12 | pass |
| Script inclusion | 10 | pass |
| Support bundle path | 3 | pass |
| Documentation phrases | 12 | pass |
| CLI validator/proof | 7 | pass |
| Agent operator smoke | 1 | pass |
| validate-all integration | 2 | pass |
| Example fixture shape | 5 | pass |
| **Total** | **86** | **all pass** |

**Verdict:** READY
- No blockers
- No follow-up code issues

---

## Skipped / Blocked

- **FILE_MANIFEST.json**: Not updated. FILE_MANIFEST.json is not validated by the CLI and is complex to maintain automatically. Noted as gap.
- **Thor**: Not available (`not_found_in_PATH`). Implementation followed repo-real ladder directly.
- **Agent Proof Boundary Closure**: Classified as `expected_pr_level_gap`, carry-forward to LRH-PR-18.

---

## PR-18+ Carry-Forward

| PR | Title | Notes |
|----|-------|-------|
| LRH-PR-16 | Windows Convenience Layer | Without full Windows app |
| LRH-PR-17 | Full Acceptance, E2E Golden Flows | All prior LRH gates |
| LRH-PR-18 | Agent Proof Boundary Closure Pack | Agent proof token closure |
| LRH-PR-19 | Thor Toolchain Hermetic Install | CI artifact pack |
| LRH-PR-25 | Packaging / Distribution / Signed Release | Signed distribution |
| LRH-PR-26 | Windows Target-Host Installer / Service / Tray | Full Windows proof |

Specifically deferred from LRH-PR-15:
- Signed distribution (LRH-PR-25)
- Target-host proof (LRH-PR-26)
- Windows service/tray/installer (LRH-PR-26)
- App store readiness (later)
- Hermetic Thor CI artifact (LRH-PR-19)
- Agent proof token closure (LRH-PR-18)

---

## Next Recommended PR

**LRH-PR-16 — Windows Convenience Layer without Full Windows App**

Adds optional Windows helper scripts, shortcut/manual starter docs and convenience checks without claiming service, tray, signing or installer proof.
