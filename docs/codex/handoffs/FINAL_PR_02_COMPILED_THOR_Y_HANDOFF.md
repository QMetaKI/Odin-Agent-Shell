# FINAL-PR-02 Compiled Thor/Y Handoff

**claim_boundary:** compiled_handoff_not_runtime_proof_not_app_approval_not_truth

---

> **Required warning:** This handoff is not truth. This handoff is not app approval.
> This handoff does not grant apply/send/tool authority.
> This handoff compiles into Universal Work before implementation.

---

```yaml
compiled_handoff_id: final_pr_02_compiled_thor_y_handoff
source_request: docs/codex/handoffs/FINAL_PR_02_THOR_Y_HANDOFF_REQUEST.md
profile_used: thor + generic + y + mjolnir
repo_cognition_basis: docs/codex/handoffs/FINAL_PR_02_REPO_COGNITION_SUMMARY.md
```

---

## Task Summary

Extend the FINAL-PR-01 Simple Local Hub (`odin/local_hub`, port 8765) with:

1. **Model Picker UI** — shows None, Mock, Local Candidate options; no model is executed
2. **Connected Apps Panel** — demo slots for Generic, Browser, File; no real apps connected
3. **Demo Universal Work Flow** — deterministic: input → Handoff Context → UW Packet → Candidate Artifact → Response Packet

The hub must visibly show Odin accepting and returning candidate work without any model inference, provider execution, app apply, or external send.

---

## Allowed Implementation Scope

```
odin/local_hub/model_picker.py          — new module: model options data
odin/local_hub/connected_apps.py        — new module: connected app slot data
odin/local_hub/demo_universal_work.py   — new module: deterministic demo flow
odin/local_hub/proof_pr02.py            — new module: FINAL-PR-02 proof packet
odin/local_hub/ui.py                    — extend HTML with new sections
odin/local_hub/server.py                — add /models.json, /apps.json, /demo/universal-work.json
odin/local_hub/__init__.py              — expose new symbols
odin/cli.py                             — add validate-final-pr-02-model-apps-demo,
                                          prove-final-pr-02-demo-universal-work
tools/rebaseline/check_final_pr_02_model_apps_demo.py — validator
tests/test_final_pr_02_model_apps_demo.py — 30 minimum tests
docs/ reports/ schemas/ registries/ examples/ — new artifacts
```

---

## Forbidden Scope (hard stops)

```
odin/models/providers/          — do not call any provider
odin/runtime/engine.py          — do not call real Universal Work kernel
odin/daemon/local_api.py        — do not touch (separate surface)
odin/hub/shell.py               — do not touch (separate surface)
API keys / environment credentials — do not read
External network                — do not access
app apply / state mutation      — do not implement
external send                   — do not implement
QIRC Core runtime               — do not start
```

---

## Files to Touch

```
MODIFY: odin/local_hub/ui.py, server.py, __init__.py, cli.py, SYSTEM_MAP.json
CREATE: odin/local_hub/model_picker.py, connected_apps.py, demo_universal_work.py, proof_pr02.py
CREATE: tools/rebaseline/check_final_pr_02_model_apps_demo.py
CREATE: tests/test_final_pr_02_model_apps_demo.py
CREATE: docs/codex/handoffs/FINAL_PR_02_*.md (all 5 handoff docs)
CREATE: docs/rebaseline/FINAL_PR_02_MODEL_APPS_DEMO.md
CREATE: docs/codex/reports/FINAL_PR_02_MODEL_APPS_DEMO_RETURN_REPORT.md
CREATE: docs/codex/audits/FINAL_PR_02_MODEL_APPS_DEMO_AUDIT.md
CREATE: docs/codex/audits/FINAL_PR_02_THOR_EFFECTIVENESS_AUDIT.md
CREATE: docs/codex/audits/FINAL_PR_02_ODIN_EFFECTIVENESS_AUDIT.md
CREATE: reports/final_pr_02_*.json (3 reports)
CREATE: schemas/final_pr_02_demo_universal_work_response_packet.schema.json
CREATE: registries/final_pr_02_model_apps_demo_registry.json
CREATE: examples/final_pr_02/demo_universal_work_response_packet.example.json
```

---

## Files to Avoid

```
All docs/MASTER_* — no changes to master architecture/specs
All registries/codex_* — no changes to task/bundle registries
tests/test_simple_local_hub.py — do not modify (kept intact)
odin/local_hub/proof.py — do not modify (FINAL-PR-01 proof kept intact)
odin/daemon/local_api.py — separate surface
odin/hub/shell.py — separate surface
odin/hub/static/index.html — separate surface
```

---

## Acceptance Gates

1. `validate-final-pr-02-model-apps-demo` passes with 0 errors
2. `prove-final-pr-02-demo-universal-work` emits proof packet with all required fields
3. All 30 focused tests pass in `test_final_pr_02_model_apps_demo.py`
4. `validate-all` passes with 0 errors (no regressions)
5. Full `pytest -q` passes
6. All required UI IDs present in `generate_hub_html()`
7. Demo endpoint returns `candidate_only: true`, `model_execution: false`, `app_apply: false`
8. Hub Surface Decision document exists

---

## Proof Commands

```bash
python -m odin.cli validate-final-pr-02-model-apps-demo
python -m odin.cli prove-final-pr-02-demo-universal-work
python tools/rebaseline/check_final_pr_02_model_apps_demo.py --repo-root . --out reports/final_pr_02_model_apps_demo_report.json --generated-at-utc 2026-01-01T00:00:00Z
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_final_pr_02_model_apps_demo.py -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
```

---

## Candidate Boundaries

```
candidate_only: true
local_only: true
model_execution: false
provider_execution: false
app_apply: false
external_send: false
qirc_core_runtime: false
```

---

## Known Gaps (carried forward to later PRs)

- Actual model inference: deferred (no model binary, no API call)
- Provider probe: deferred to FINAL-PR-04
- Real app bridge runtime: deferred
- External app integration: deferred
- QIRC Core runtime: deferred to FINAL-PR-03
- Deep activity/trace/receipt/dev-mode viewer: deferred to FINAL-PR-03
- Hub surface convergence (8765/8877/8878): deferred to FINAL-PR-03 or later

---

## Return Contract

Claude Code (worker) must return:

1. All 30 tests passing
2. `validate-all: OK` receipt
3. `validate-final-pr-02-model-apps-demo: OK` receipt
4. `prove-final-pr-02-demo-universal-work` proof packet receipt
5. All required UI IDs present in `generate_hub_html()`
6. Demo endpoint returning required fields
7. All required docs/reports/schemas/registries/examples created
8. SYSTEM_MAP and FILE_MANIFEST updated
9. No forbidden claims (no model inference, no provider execution, no app apply, no external send)
10. Return report with Thor audit, Odin audit, senior reviewer simulation, senior code reviewer simulation
