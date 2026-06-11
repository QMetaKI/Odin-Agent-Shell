# Portable Package and Release ZIP — V1

**LRH-PR-15**
**Claim boundary:** `portable_package_candidate_only_not_signed_not_production_not_target_host_proof`

---

## 1. What this is

A deterministic, local-only, candidate-only portable package builder for Odin Local Runtime Hub.

This PR adds a portable package candidate path that:

- Collects repo files using a deterministic sorted scan
- Excludes junk and sensitive local files
- Computes stable SHA256 checksums
- Emits a package manifest JSON
- Emits a local verification report JSON
- Optionally creates a deterministic ZIP archive
- Records start/check script inclusion status
- Exposes the support bundle command path

This is a portable package candidate. Generated artifacts are not committed to the repo.

---

## 2. What this is not

- **Not production readiness** — no deployment proof claimed
- **Not security certification** — no security audit performed
- **Not signed distribution proof** — no code signing, no certificate
- **Not release certification** — no release authority asserted
- **Not Windows service/tray/installer proof** — no Windows service, tray, or installer
- **Not target-host proof** — no target-host validation
- **Not app store readiness** — no app store submission
- **No app apply** — Odin does not apply app state
- **No external send** — no network transmission
- **No live model inference** — no model execution in packaging
- **No model quality proof** — no model quality certification

---

## 3. Portable package builder

**Script:** `scripts/build_portable_package.py`

**Requirements:**
- stdlib-only
- deterministic
- local-only
- no network
- no provider/model calls
- no app apply
- no external send
- no destructive operations
- output goes to caller-specified paths (default: `/tmp/...`)
- safe to run repeatedly
- stable sorted file order
- stable SHA256 checksums
- stable POSIX-style `/` path separators in manifest
- generated artifacts not committed

**Basic usage:**

```bash
python scripts/build_portable_package.py \
  --out /tmp/odin_lrh_pr15_package \
  --manifest-out /tmp/odin_lrh_pr15_manifest.json \
  --report-out /tmp/odin_lrh_pr15_release_verification.json
```

**With optional ZIP:**

```bash
python scripts/build_portable_package.py \
  --out /tmp/odin_lrh_pr15_package \
  --manifest-out /tmp/odin_lrh_pr15_manifest.json \
  --report-out /tmp/odin_lrh_pr15_release_verification.json \
  --zip-out /tmp/odin_lrh_pr15_portable_package.zip
```

**Dry-run (no files written):**

```bash
python scripts/build_portable_package.py --dry-run
```

---

## 4. Manifest contract

The manifest JSON shape:

```json
{
  "artifact_kind": "odin_portable_package_manifest",
  "lrh_pr": "LRH-PR-15",
  "package_kind": "portable_package_candidate",
  "candidate_only": true,
  "local_only": true,
  "claim_boundary": "portable_package_candidate_only_not_signed_not_production_not_target_host_proof",
  "included_files": [],
  "excluded_patterns": [],
  "required_entries": [],
  "missing_required_entries": [],
  "start_check_scripts": {},
  "support_bundle_command": "",
  "support_bundle_claim": "",
  "checksums": {},
  "proof_boundaries": [],
  "not_proven": []
}
```

**Rules:**
- `included_files`: sorted list, relative POSIX paths, no absolute paths, no backslash separators
- `checksums`: `{relative_path: lowercase_hex_sha256_64_chars}`, stable across repeated runs
- `not_proven`: must include all required known non-proofs
- `proof_boundaries`: must include all required boundaries

See `dist_manifest/portable_package_manifest.example.json` for a full example.

---

## 5. Checksum policy

- Algorithm: SHA256
- Format: lowercase hex, 64 characters
- Stability: same file contents → same checksum across repeated runs
- Scope: all included files in sorted order
- No nondeterministic timestamp fields in checksums

Checksums are a local receipt only. Not a signed distribution proof. Not a release certification.

---

## 6. ZIP determinism policy

If `--zip-out` is used:

- All paths sorted
- Normalized archive names (POSIX-style, no absolute paths)
- Deterministic timestamp for each ZIP entry: `(1980, 1, 1, 0, 0, 0)`
- No host-dependent permissions
- No `.git/`, caches, `.env`, or previous ZIPs included
- ZIP checksum is a local receipt only, not signed distribution proof

ZIP generation is implemented using Python `zipfile` (stdlib-only, no network).

---

## 7. Included start/check scripts

The builder records which start/check scripts are present in the repo:

| Script | Role |
|--------|------|
| `scripts/start_odin.sh` | POSIX start |
| `scripts/check_odin.sh` | POSIX health check |
| `scripts/stop_odin.sh` | POSIX stop |
| `scripts/start_odin.bat` | Windows start |
| `scripts/check_odin.bat` | Windows health check |
| `scripts/stop_odin.bat` | Windows stop |

If a script is absent from the repo, it is listed in `missing_required_entries` and does not fail the build, but is recorded.

---

## 8. Support bundle command / path visibility

The support bundle command is exposed in the manifest as path visibility only.

**Repo-real command:**

```
python -m odin.cli emit-support-bundle --diagnostics-only
```

This command exists in the repo CLI. It is recorded in the manifest as:

```json
"support_bundle_command": "python -m odin.cli emit-support-bundle --diagnostics-only",
"support_bundle_claim": "support_bundle_command_path_visible_not_support_organization_readiness"
```

**What this is not:**
- Not support organization readiness
- Not security certification
- Not production readiness

---

## 9. Junk exclusion policy

The following are excluded from the portable package:

**Excluded directories:**
- `.git`
- `.pytest_cache`
- `__pycache__`
- `.mypy_cache`
- `.ruff_cache`
- `.cache`
- `node_modules`
- `.venv`
- `venv`
- `dist`
- `build`

**Excluded files:**
- `.env`, `.env.*` (local secret files)
- `.DS_Store`, `Thumbs.db` (OS metadata)

**Excluded extensions:**
- `.pyc`, `.pyo` (compiled bytecode)
- `.egg-info` (package metadata)

Safe example fixture files are not excluded solely because they contain placeholder names.

See `dist_manifest/portable_package_exclusions_v1.json` for the static exclusion policy spec.

---

## 10. Local verification report

The local release verification report shape:

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
  "claim_boundary": "portable_release_verification_local_receipt_not_release_certification",
  "proof_boundaries": [],
  "not_proven": []
}
```

This is a **local verification report only**, not a release certification.

See `dist_manifest/portable_package_release_verification.example.json` for a full example.

---

## 11. Proof boundaries

- `not_production_readiness_certification`
- `not_security_certification`
- `not_signed_distribution_proof`
- `not_release_certification`
- `not_windows_service_tray_installer_proof`
- `not_target_host_proof`
- `not_app_store_readiness_proof`
- `not_public_network_api_proof`
- `not_live_model_inference_proof`
- `not_model_quality_proof`
- `not_app_apply_proof`
- `not_app_state_mutation_proof`
- `not_external_send_authority_proof`
- `candidate_artifact_not_applied_truth`
- `host_app_owns_apply_state_external_send`

---

## 12. Known non-proofs

| Not proven | Notes |
|------------|-------|
| `production_readiness` | Not a production deployment |
| `security_certification` | No security audit |
| `signed_distribution` | No code signing |
| `release_certification` | No release authority |
| `windows_service_tray_installer` | No Windows service, tray, or installer |
| `target_host_validation` | No target-host test |
| `app_store_readiness` | No app store submission |
| `public_network_api` | No WAN/LAN API |
| `live_model_inference` | No model execution |
| `model_quality` | No model quality proof |
| `app_apply_authority` | App owns apply |
| `app_state_mutation` | App owns state |
| `external_send_authority` | App owns external send |

---

## 13. Claim discipline

Allowed scoped wording:
- portable package candidate
- candidate-only
- local-only
- local verification report
- not_proven
- known non-proof
- not certification
- not production readiness
- not signed distribution proof

Positive overclaim wording must not appear. Wording that asserts this artifact represents
a deployment-grade, security-audited, or signed output is not allowed.
Use negated or scoped forms only: "not proven", "candidate-only", "local receipt".

---

## 14. PR-18+ carry-forward

The following remain for later PRs:

- **LRH-PR-18** — Agent Proof Boundary Closure Pack
- **LRH-PR-19** — Thor Toolchain Hermetic Install and CI Artifact Pack
- **LRH-PR-25** — Packaging / Distribution / Signed Release Readiness
- **LRH-PR-26** — Windows Target-Host Installer / Service / Tray Proof Pack

Specifically deferred from LRH-PR-15:
- Signed distribution (later)
- Target-host proof (later)
- Windows service/tray/installer (later)
- App store readiness (later)
- Hermetic Thor CI artifact (later)
- Agent proof token closure (later unless tiny safe fix)
