# v1.0.0 External Release Receipts

**Receipt status:** external_release_receipts_recorded  
**Version:** v1.0.0  
**Claim boundary:** PR57 records maintainer-provided/publicly checkable release metadata only; it does not certify runtime behavior, security, model quality, deployment readiness, PyPI publication, or asset upload.

## Recorded receipts

| Receipt | Value | Status |
|---|---|---|
| Git tag | `v1.0.0` | documented as the intended external release tag |
| GitHub Release | `v1.0.0` | documented as the intended external GitHub Release name |
| Release URL | not recorded in this repository | optional receipt not claimed by PR57 |
| Tag URL | not recorded in this repository | optional receipt not claimed by PR57 |
| PyPI publication | not claimed | no PyPI receipt is recorded |
| Release assets | not claimed | no uploaded asset receipt is recorded |

## Non-claims

PR57 does not claim:

- production readiness;
- security certification;
- model benchmark results;
- model superiority;
- PyPI publication;
- uploaded release assets;
- host/runtime verification beyond the local validation commands run for this PR.

## Termux compatibility receipt

PR57 also removes the legacy hardcoded `/tmp/lrh_pr_09_packet.json` packet path from `tests/test_lrh_pr_09_trace_viewer.py`. The LRH-PR-09 handoff, guard, check, and proof tests now use pytest-managed portable temporary paths while preserving the same candidate-only packet assertions.
