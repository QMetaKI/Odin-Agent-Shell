# Runtime Source Module Map v0.8.0

| Master Architecture Layer | Source Module | Status |
|---|---|---|
| Universal Work Kernel | `odin/runtime/engine.py`, `odin/universal_work/` | executable candidate |
| App Bridge | `odin/apps/caller_manifest.py` | executable candidate |
| QIRC Gold Spine | `odin/qirc/ledger.py` | local digest candidate |
| Seed Packs | `odin/seeds/` | compiler candidate |
| Pattern Mine / Flow Packs | `odin/patterns/`, `odin/flow_packs/` | compiler candidate |
| Work Atom Runtime | `odin/work_atoms/` | executable micro-op candidate |
| Model Routing | `odin/models/model_router.py`, `odin/models/workers.py` | mock-worker candidate |
| Candidates | `odin/candidates/` | executable candidate |
| Why Trace | `odin/why_trace/` | executable candidate |
| Local API | `odin/daemon/local_api.py` | localhost skeleton |
| Odin Hub | `odin/hub/static_hub.py` | static UI skeleton |
| Diagnostics | `odin/diagnostics/support_bundle.py` | local diagnostic candidate |
| Recovery | `odin/recovery/safe_mode.py` | safe-mode plan candidate |

## Boundary

All modules preserve candidate-only behavior. None of these modules grants app apply authority to Odin.
