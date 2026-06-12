# FINAL-PR-09 — Release Closure / Full Acceptance / Claim Boundary Lock

**Claim boundary:** `release_closure_records_evidence_not_production_certification`
**candidate_only:** true
**app_owned_apply:** true
**generated_at_utc:** 2026-01-01T00:00:00Z
**depends_on:** FINAL-PR-06, FINAL-PR-07, FINAL-PR-08 (all merged)

---

## Purpose

This prompt instructs a new Claude Code session to perform Release Closure only after
FINAL-PR-06, FINAL-PR-07, and FINAL-PR-08 have been merged and validated.

Release Closure records evidence of completion, locks claim boundaries, audits the
full system for not-proven items, and produces a final release evidence packet.
It does NOT certify production readiness. It does NOT certify security.
It does NOT introduce new runtime features unless required for closure.

---

## 0. Repo-Real Intake Steps (MANDATORY — do before any edit)

1. `git status` — confirm clean working tree.
2. `git log --oneline -15` — confirm FINAL-PR-06, PR-07, PR-08 merge commits present.
3. Run ALL of the following — all must pass:
   - `python -m odin.cli validate-operational-seed-spine`
   - `python -m odin.cli validate-field-selection-spine`
   - `python -m odin.cli validate-projection-candidate-spine`
   - `python -m odin.cli validate-y-pattern-spine`
   - `python -m odin.cli validate-all`
4. Run: `python -m pytest -q -p no:cacheprovider` — full suite must pass.
5. Inspect: all `reports/final_pr_0*.json` — confirm all exist.
6. Inspect: all `docs/codex/reports/FINAL_PR_0*_RETURN_REPORT.md` — confirm all exist.
7. Read: `registries/prep_final_pr_06_08_plan.v1.json` — confirm PR09 entry.
8. Read: `docs/codex/handoffs/PREP_FINAL_PR_06_08_REPO_REALITY_INTAKE.md`.

STOP and report if any validate command fails. Do NOT proceed with release closure.

---

## 1. Scope

Perform full release closure:

1. Complete release readiness matrix — survey all Odin surfaces for completion.
2. Final proof chain review — verify proof chain records for all ladder PRs.
3. Final `not_proven` lock — enumerate all system-wide not-proven items.
4. Claim boundary inventory — list all claim boundaries across all modules.
5. CLI validation inventory — verify all validate-* commands pass.
6. Local Hub acceptance inventory — verify all demo endpoints return valid JSON.
7. Docs/reports consistency check — verify all return reports and audit docs exist.
8. Release evidence packet — produce `reports/final_pr_09_release_closure_evidence.json`.

---

## 2. Non-Scope

- Do NOT introduce new runtime features unless required for closure plumbing.
- Do NOT overclaim production readiness.
- Do NOT overclaim security certification.
- Do NOT apply app state, send external messages, or execute providers.
- Do NOT renumber or rename merged historical PRs.
- Do NOT import Q Metamodell / cutk1 as runtime truth.
- Do NOT add new Q-style runtime names.
- Do NOT connect to public networks.

---

## 3. Allowed Files

**Create (new):**
- `docs/rebaseline/FINAL_PR_09_RELEASE_CLOSURE.md`
- `docs/codex/audits/FINAL_PR_09_RELEASE_CLOSURE_AUDIT.md`
- `docs/codex/audits/FINAL_PR_09_SENIOR_REVIEW.md`
- `docs/codex/reports/FINAL_PR_09_RELEASE_CLOSURE_RETURN_REPORT.md`
- `docs/codex/handoffs/FINAL_PR_09_REPO_COGNITION_SUMMARY.md`
- `registries/final_pr_09_release_closure_registry.json`
- `reports/final_pr_09_release_closure_evidence.json`
- `reports/final_pr_09_release_closure_proof_packet.json`
- `tests/test_final_pr_09_release_closure.py`
- `tools/rebaseline/check_final_pr_09_release_closure.py`

**Update (existing):**
- `odin/cli.py` — add `validate-final-pr-09-release-closure`, `prove-final-pr-09-release-closure`
- `SYSTEM_MAP.json` — add `final_pr_09_release_closure` entry
- `FILE_MANIFEST.json` — add new files
- `registries/prep_final_pr_06_08_plan.v1.json` — mark PR09 as `in_progress` or `complete`

---

## 4. Forbidden Changes

- Do NOT modify: `odin/operational_seed_spine/`, `odin/field_selection_spine/`, `odin/projection_candidate_spine/`
- Do NOT modify: `odin/y_pattern_spine/`, `odin/execution_gate/`, `odin/proof_chain/`
- Do NOT delete any existing file.
- Do NOT introduce new `q_*` named modules, keys, or CLI commands.

---

## 5. Required Release Readiness Matrix

The closure must document status of all final PR surfaces:

| Surface | Validator | CLI OK | Tests Pass | Return Report | Proof Packet |
|---------|-----------|--------|------------|---------------|--------------|
| FINAL-PR-01 Simple Local Hub | check_simple_local_hub.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-02 Model Apps Demo | check_final_pr_02_*.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-03 QIRC Core Dev Mode | check_final_pr_03_*.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-04 Provider Probe Security | check_final_pr_04_*.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-05 Execution Gate Ladder | check_final_pr_05_*.py | ✓ | ✓ | ✓ | ✓ |
| Y Pattern Spine | check_y_pattern_spine.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-06 Operational Seed Spine | check_final_pr_06_*.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-07 Field Selection Spine | check_final_pr_07_*.py | ✓ | ✓ | ✓ | ✓ |
| FINAL-PR-08 Projection Candidate Spine | check_final_pr_08_*.py | ✓ | ✓ | ✓ | ✓ |

---

## 6. Required CLI Commands

```
python -m odin.cli validate-final-pr-09-release-closure
python -m odin.cli prove-final-pr-09-release-closure
```

Both must be wired into `odin/cli.py`.
`validate-final-pr-09-release-closure` must be called from `validate_all()`.

---

## 7. Required Validator

File: `tools/rebaseline/check_final_pr_09_release_closure.py`

Requirements:
- stdlib only
- accepts `--repo-root`, `--out`, optional `--generated-at-utc`
- validates all final PR report files exist
- validates all final PR return reports exist
- validates all final PR proof packets have `candidate_only: true`
- validates all final PR proof packets have non-empty `not_proven` list
- validates release evidence packet exists
- validates release evidence packet NOT claiming production_readiness or security_certification
- writes `reports/final_pr_09_release_closure_evidence.json`

---

## 8. Required Tests

File: `tests/test_final_pr_09_release_closure.py`

Minimum 10 tests covering:
1. All PR01–PR08 report files exist
2. All PR01–PR08 proof packets have `candidate_only: true`
3. All PR01–PR08 proof packets have non-empty `not_proven`
4. Release evidence packet exists and parses
5. Release evidence packet has `claim_boundary`
6. Release evidence packet NOT claiming production_readiness
7. Validator returns ok (no errors)
8. CLI `validate-final-pr-09-release-closure` returns 0
9. validate-all includes release closure validator
10. not_proven lock includes production_readiness, security_certification, live_model_inference

---

## 9. Proof Packet Expectations

```json
{
  "proven": ["all_ladder_validators_pass", "proof_chain_complete", "claim_boundaries_enumerated", "not_proven_lock_complete"],
  "not_proven": ["production_readiness", "security_certification", "live_model_inference", "provider_execution", "app_apply", "external_send_authority", "deployment_proof"],
  "claim_boundary": "release_closure_records_evidence_not_production_certification",
  "candidate_only": true
}
```

---

## 10. Not-Proven List (System-Wide Lock)

The release closure must enumerate all system-wide not-proven items:
- production_readiness
- security_certification
- live_model_inference
- provider_execution_in_production
- app_apply_authority
- external_send_authority
- deployment_proof
- vulnerability_free_claim
- target_host_runtime_proof
- release_approval (not to be claimed by Odin — app owns this)

---

## 11. Senior Reviewer Checklist

- [ ] All PR01–PR08 validators pass before closure begins
- [ ] Release evidence packet exists with `candidate_only: true`
- [ ] Proof packet not_proven includes production_readiness and security_certification
- [ ] No new runtime features introduced unless strictly required
- [ ] No renumbering of merged historical PRs
- [ ] Historical PR names unchanged
- [ ] validate_all() calls validate_final_pr_09_release_closure()
- [ ] Release closure does not claim authority over app release decisions

---

## 12. Acceptance Gates

1. `python -m odin.cli validate-final-pr-09-release-closure` exits 0
2. `python -m odin.cli prove-final-pr-09-release-closure` exits 0
3. `python -m odin.cli validate-all` exits 0
4. `python -m pytest -q tests/test_final_pr_09_release_closure.py -p no:cacheprovider` passes all tests
5. `python -m pytest -q -p no:cacheprovider` full suite passes
6. `reports/final_pr_09_release_closure_evidence.json` exists with valid structure

---

## 13. Claim Boundary

`release_closure_records_evidence_not_production_certification`

This PR does NOT claim:
- production readiness
- security certification
- vulnerability-free status
- deployment approval
- target-host runtime proof
- live model inference
- provider execution
- app apply or external send authority
