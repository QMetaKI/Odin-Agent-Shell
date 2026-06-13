# Pre-Release Super Audit — Runtime Paths and Smoke

| Path | Kind | Status | Notes |
| --- | --- | --- | --- |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-projection-candidate-spine | cli | pass | local deterministic subprocess; no provider/model execution requested |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-field-selection-spine | cli | pass | local deterministic subprocess; no provider/model execution requested |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-operational-seed-spine | cli | pass | local deterministic subprocess; no provider/model execution requested |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli validate-all | cli | pass | local deterministic subprocess; no provider/model execution requested |
| /root/.pyenv/versions/3.12.13/bin/python -m odin.cli explain-projection-candidate --demo | cli | pass | local deterministic subprocess; no provider/model execution requested |
| PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no | pytest | skipped | lightweight mode skips full test suite by design |
| GET /healthz | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /status.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET / | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /demo/universal-work.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /activity.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /receipts.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /providers/probe.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /execution-gate/status.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| POST /execution-gate/mock | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /final-pr-ladder/scaffold.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /demo/y-route.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /demo/seed-route.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /demo/field-selection.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| GET /demo/projection-candidate.json | endpoint | pass | localhost-only ephemeral Local Hub handler smoke |
| import odin | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.cli | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.local_hub.server | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.qirc_core.bus | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.execution_gate.gateway | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.providers.probe | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.operational_seed_spine.selector | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.field_selection_spine.selector | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.projection_candidate_spine.projection_set | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |
| import odin.proof_chain.registry | import | pass | safe top-level Odin module import smoke via isolated Python subprocess |

## Final validation receipts

| Command | Status | Result |
| --- | --- | --- |
| `python -m odin.cli audit-pre-release-super` | pass | status ok; overall_verdict yellow; release_pr_should_move_to FINAL-PR-11 |
| `python -m odin.cli validate-pre-release-super-audit` | pass | validate-pre-release-super-audit: OK |
| `python -m odin.cli validate-all` | pass | validate-all: OK |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_pre_release_super_audit.py -p no:cacheprovider` | pass | 25 passed in 10.96s; 25 passed in 10.73s; 25 passed in 10.98s after cleanup |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider --tb=no` | pass | 2380 passed, 2 skipped in 315.22s (0:05:15) |

