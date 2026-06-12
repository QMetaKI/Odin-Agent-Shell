# FINAL-PR-02 Hub Surface Decision

**claim_boundary:** hub_surface_decision_not_runtime_proof_not_convergence_authority
**generated_for:** FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work

---

## Observed Surfaces

| Surface | Port | Module | Status | Notes |
|---|---|---|---|---|
| Simple Local Hub | 8765 | `odin/local_hub/server.py` | Active (FINAL-PR-01) | Thin, stdlib-only, candidate-only |
| Local API / daemon | 8877 | `odin/daemon/local_api.py` | Active (REAL-GH-PR-01+) | Full API, FORBIDDEN_ROUTES, SDK bridge |
| Browser Hub | 8878 | `odin/hub/shell.py` + `odin/hub/static/index.html` | Active scaffold | Shell validation, static hub, full panel map |
| Serve-browser-hub | 8878 | `odin/cli.py:serve-browser-hub` | CLI scaffold | Not deeply serving in this PR |

---

## Chosen Approach for FINAL-PR-02

**Keep `odin/local_hub` on port 8765 as the canonical FINAL-PR-02 entry point.**

- Extend it minimally with model picker UI, connected apps UI, and demo Universal Work endpoints.
- Do not merge or refactor the existing 8877 or 8878 surfaces in this PR.
- Do not change `odin/daemon/local_api.py`, `odin/hub/shell.py`, or existing static hub HTML.
- New endpoints added to Simple Local Hub: `/models.json`, `/apps.json`, `/demo/universal-work.json`.
- POST `/demo/universal-work` is deferred — GET demo endpoint is sufficient for this PR.

---

## Why This Is the Smallest Safe Implementation

1. The Simple Local Hub (8765) is already validated, tested, and smoke-proved by FINAL-PR-01.
2. Extending it minimally keeps the change radius small.
3. Merging 8765 with 8877 or 8878 would require touching multiple validated modules and risking regression in existing tests.
4. The demo Universal Work flow is deterministic and does not need the full local API machinery.
5. Token budget: minimal new endpoints, no deep refactor.

---

## Risk of Duplication

**Acknowledged risk:** Three separate hub/API surfaces create UX confusion and maintenance overhead.

- 8765: Normal user entry point (FINAL-PR-01/02)
- 8877: Full local API (daemon, SDK bridge)
- 8878: Browser hub (rich panel map, candidates viewer, trace viewer)

These are currently independent by design — each PR slice adds a new surface rather than converging. This is acceptable for the road-to-100 but must be resolved before FINAL-PR-03 or a convergence PR.

---

## What Is Intentionally Not Touched

- `odin/daemon/local_api.py` — full API has its own validate/prove stack; not touched
- `odin/hub/shell.py` — browser hub has its own validate/prove stack; not touched
- `odin/hub/static/index.html` — static hub HTML; not touched
- Any existing CLI commands that serve/prove the 8877 or 8878 surfaces

---

## What Must Converge Later

Before production or FINAL-PR-05/06, the following must be decided:

1. **Single canonical hub URL for normal users.** Currently a user would not know whether to open 8765, 8877, or 8878.
2. **Merged or delegating server.** The 8765 server could proxy to or embed 8877/8878 panels.
3. **Unified validator.** `validate-all` currently validates all three independently. A unified hub validator would check the combined surface.
4. **Port assignment policy.** 8765, 8877, 8878 are not all IANA-registered for Odin. Need a canonical assignment.

---

## Recommendation for FINAL-PR-03

- Add a `docs/codex/handoffs/FINAL_PR_03_HUB_CONVERGENCE_DECISION.md` that decides:
  - Which port is canonical for normal users
  - Whether 8765 expands into a superset or delegates to 8877
  - Whether QIRC Core (planned for FINAL-PR-03) runs on a new port or extends 8765/8877
- Run a hub convergence audit before implementing FINAL-PR-03 UI changes.

---

## Recommendation for Possible PR-05/PR-06 Split

- **PR-05:** Hub surface merge — unify 8765, 8877, 8878 into a single canonical hub
- **PR-06:** Provider probe — integrate real local provider probing into the unified hub

This split avoids merging provider execution with hub UI changes in the same PR.

---

## Decision Record

```json
{
  "decision": "extend_simple_local_hub_8765_minimal",
  "reason": "smallest_safe_extension_of_validated_surface",
  "surfaces_untouched": ["8877", "8878"],
  "convergence_deferred_to": "FINAL-PR-03",
  "candidate_only": true,
  "claim_boundary": "hub_surface_decision_not_runtime_proof_not_convergence_authority"
}
```
