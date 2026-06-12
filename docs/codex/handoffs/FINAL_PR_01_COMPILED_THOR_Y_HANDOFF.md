# FINAL-PR-01 Compiled Thor/Y Handoff Context

```
compiled_handoff_id: final_pr_01_compiled_thor_y_handoff
source_request: docs/codex/handoffs/FINAL_PR_01_THOR_Y_HANDOFF_REQUEST.md
profile_used: thor (primary), y (secondary), mjolnir (profile-awareness only)
repo_cognition_basis: docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md
```

---

> **Warning:** This handoff is not truth. This handoff is not app approval.
> This handoff does not grant apply/send/tool authority.
> This handoff compiles into Universal Work before implementation.

---

## Formula

```
Handoff orients.
Universal Work bounds.
Odin gates.
QIRC coordinates.
Apps decide.
Claude Code implements candidate patches.
Receipts bind claims.
```

---

## Task Summary

Implement **FINAL-PR-01: Simple Local Hub Start + Normal User Browser UI**.

This is the first final Road-to-100 build slice. It makes Odin locally startable
and understandable by a normal user by:
1. Adding a simple stdlib HTTP server on 127.0.0.1:8765
2. Serving a Browser Hub HTML page with required stable IDs and normal-user copy
3. Adding CLI commands: start-local-hub, status-local-hub, open-hub, validate-simple-local-hub, prove-simple-local-hub
4. Adding a deterministic smoke proof (--once-smoke)
5. Adding a proof packet, validator, tests, and all required docs/artifacts

---

## Implementation Scope

**Allowed:**
- `odin/local_hub/` package: `__init__.py`, `policy.py`, `ui.py`, `server.py`, `proof.py`
- CLI: 5 new commands in `odin/cli.py`
- `validate_simple_local_hub()` added to `validate_all()`
- `tools/rebaseline/check_simple_local_hub.py`
- `tests/test_simple_local_hub.py` (34 tests)
- All handoff/audit/report/schema/registry/example docs
- Updates to `SYSTEM_MAP.json`, `FILE_MANIFEST.json`
- Roadmap docs marking FINAL-PR-01 as implemented

**Forbidden:**
- Provider/model execution
- External network beyond localhost smoke
- Full QIRC Core runtime
- Real app bridge runtime
- App apply, app state mutation, external send
- Public bind (0.0.0.0)
- Windows service/tray/installer
- Runtime/product/security/release overclaims

---

## Files to Touch

```
odin/local_hub/__init__.py          NEW
odin/local_hub/policy.py            NEW
odin/local_hub/ui.py                NEW
odin/local_hub/server.py            NEW
odin/local_hub/proof.py             NEW
odin/cli.py                         UPDATED
tools/rebaseline/check_simple_local_hub.py  NEW
tests/test_simple_local_hub.py      NEW
schemas/final_pr_01_simple_local_hub_proof_packet.schema.json  NEW
registries/final_pr_01_simple_local_hub_registry.json          NEW
examples/final_pr_01/simple_local_hub_proof_packet.example.json NEW
reports/final_pr_01_simple_local_hub_report.json               NEW
reports/final_pr_01_thor_odin_y_effectiveness_audit.json       NEW
docs/rebaseline/FINAL_PR_01_SIMPLE_LOCAL_HUB.md                NEW
docs/codex/audits/FINAL_PR_01_SIMPLE_LOCAL_HUB_AUDIT.md        NEW
docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md NEW
docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md NEW
docs/codex/handoffs/FINAL_PR_01_REPO_COGNITION_SUMMARY.md      NEW
docs/codex/handoffs/FINAL_PR_01_THOR_Y_HANDOFF_REQUEST.md      NEW
docs/codex/handoffs/FINAL_PR_01_COMPILED_THOR_Y_HANDOFF.md     NEW
docs/codex/handoffs/FINAL_PR_01_ODIN_AGENT_OPERATOR_WORK_PACKET.md NEW
docs/codex/handoffs/FINAL_PR_01_Y_MJOLNIR_PROFILE_NOTES.md     NEW
SYSTEM_MAP.json                     UPDATED
FILE_MANIFEST.json                  UPDATED
```

## Files to Avoid

```
odin/hub/shell.py               (existing browser hub — LRH-PR-06+)
odin/hub/static/                (existing static assets)
odin/daemon/local_api.py        (existing local API — LRH-PR-05)
odin/local_runtime/             (existing portable runtime — LRH-PR-03)
Any FINAL-PR-02..05 files
```

---

## Acceptance Gates

1. `python -m odin.cli start-local-hub --once-smoke` → status ok
2. `python -m odin.cli status-local-hub` → clean stopped/running JSON
3. `python -m odin.cli open-hub` → URL JSON with localhost
4. `python -m odin.cli validate-simple-local-hub` → exit 0
5. `python -m odin.cli prove-simple-local-hub` → artifact_kind=odin_simple_local_hub_proof_packet
6. `python -m odin.cli validate-all` → OK
7. `pytest tests/test_simple_local_hub.py` → all pass
8. `pytest -q -p no:cacheprovider` → all pass
9. localhost policy rejects 0.0.0.0
10. HTML contains all 11 required stable IDs
11. proof packet has candidate_only=true, local_only=true, 11 not_proven items
12. All handoff/audit/report/schema/registry/example artifacts exist

---

## Proof Commands

```bash
python -m odin.cli start-local-hub --once-smoke
python -m odin.cli prove-simple-local-hub
python -m odin.cli validate-simple-local-hub
python -m odin.cli validate-all
python tools/rebaseline/check_simple_local_hub.py --repo-root . --out reports/final_pr_01_simple_local_hub_report.json
pytest tests/test_simple_local_hub.py -q -p no:cacheprovider
```

---

## Candidate Boundaries

```
candidate_only: true
local_only: true
app_owned_apply: true
external_send_default: false
claim_boundary: simple_local_hub_local_receipt_not_runtime_completion_not_production
```

---

## Known Gaps

- Model picker: deferred to FINAL-PR-02
- Connected apps runtime: deferred to FINAL-PR-02
- Demo Universal Work: deferred to FINAL-PR-02
- QIRC Core runtime: deferred to FINAL-PR-03
- Deep Handoff Viewer: deferred to FINAL-PR-03
- Activity/trace/receipt/dev-mode deep viewer: deferred to FINAL-PR-03
- File/spool and CLI/agent pipe: deferred to FINAL-PR-04
- Provider probe: deferred to FINAL-PR-04
- Final acceptance cleanup: deferred to FINAL-PR-05

---

## Return Contract

Claude Code must return:
- Committed implementation on branch `claude/final-pr-01-local-hub-ui-sumtsa`
- All acceptance gates passing
- Return report at `docs/codex/reports/FINAL_PR_01_SIMPLE_LOCAL_HUB_RETURN_REPORT.md`
- Thor/Odin/Y effectiveness audit at `docs/codex/audits/FINAL_PR_01_THOR_ODIN_Y_EFFECTIVENESS_AUDIT.md`
- Senior Review and Senior Code Review simulation applied
