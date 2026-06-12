# FINAL-PR-02 Model Picker + Connected Apps + Demo Universal Work

**Claim boundary:** final_pr_02_spec_not_runtime_proof_not_production_readiness_claim
**PR:** FINAL-PR-02
**Base:** main after merged FINAL-PR-01 (SHA: 244d7798f2071a944f931a8f550052d4d8feb59b)
**Branch:** claude/final-pr-02-model-apps-demo-ykmn9v

---

## What Was Implemented

FINAL-PR-02 extends the Simple Local Hub (`odin/local_hub`, port 8765) with:

1. **Model Picker UI** — shows None, Mock, Local Candidate options; no model executed
2. **Connected Apps Panel** — Generic, Browser, File placeholder slots; no real apps
3. **Demo Universal Work Flow** — deterministic: input → Handoff Context → UW → Candidate → Response
4. New endpoints: `/models.json`, `/apps.json`, `/demo/universal-work.json`, POST `/demo/universal-work`
5. Proof packet for the demo flow
6. Validator (`validate-final-pr-02-model-apps-demo`) included in `validate-all`
7. 38 tests in `tests/test_final_pr_02_model_apps_demo.py`
8. Hub Surface Decision (8765 vs 8877/8878)
9. Improved Thor Effectiveness Audit with derived backlog
10. Improved Odin Effectiveness Audit with optimization backlog

---

## Model Picker UX

The model picker is **selection/status UI only** in this PR.

Normal-user view:
> "Choose how Odin should prepare work. No model inference runs in this PR."

Options shown:
- **None** — no model, deterministic candidates only
- **Mock** — mock deterministic candidate mode (not executing a real model)
- **Local candidate** — listed but not executed yet (deferred to FINAL-PR-04)

Provider status panel: shows no provider active, no API key in use, no binary running.

**Not executing:**
- Ollama
- llama.cpp
- OpenAI
- Claude
- Any remote model API

---

## Connected Apps UX

Connected apps are **demo/placeholder slots only** in this PR.

Normal-user view:
> "Connected apps are demo slots only. Apps still decide what to apply."

Slots shown:
- **Generic App Slot** — placeholder, not connected
- **Browser Slot** — placeholder, not connected
- **File Slot** — placeholder, not connected
- **App Bridge Status** — demo placeholder, no real bridge runtime

**Not connected:**
- No real external app
- No app state mutation
- No external send

---

## Demo Universal Work UX

The demo Universal Work flow is **deterministic** — no model is called.

Normal-user view:
> "Odin can accept a demo Universal Work request and return a candidate response packet. No model is called. No provider is executed. No app apply."

Flow shown in UI:
```
Raw input → Handoff Context → Universal Work Packet → Candidate Artifact → Response Packet
```

Dev Mode view:
> "Raw demo input → Handoff Context → Universal Work → Candidate Artifact → Response Packet. No provider execution. No model inference. No app apply. No external send."

---

## Handoff Context Path

1. User provides input (or uses default "demo input")
2. Odin compiles a Handoff Context: `{profile: generic, intent: demo_universal_work, forbidden_actions: [...]}`
3. Handoff Context gates the Universal Work Packet

---

## Candidate Artifact Path

1. Universal Work Packet compiled with kind: demo, status: compiled
2. Candidate Artifact generated deterministically (hard-coded, not model output)
3. Candidate Artifact returned to caller for optional apply
4. App decides what to apply — Odin does not apply

---

## Response Packet Path

1. Response Packet status: ok_with_known_gaps
2. Includes `candidate_only: true`, `not_proven: [...]`, `claim_boundary`
3. Not final truth — app owns apply authority

---

## Boundaries

- No model inference
- No provider execution
- No API key use
- No external app integration
- No app apply / app state mutation
- No external send
- No QIRC Core runtime
- No production readiness claim
- No security certification claim

---

## Known Gaps (deferred to later PRs)

| Gap | Deferred to |
|---|---|
| Actual model inference | FINAL-PR-04 |
| Provider probe / live status | FINAL-PR-04 |
| Real app bridge runtime | FINAL-PR-03 or later |
| External app integration | FINAL-PR-03 or later |
| QIRC Core runtime | FINAL-PR-03 |
| Deep activity/trace/receipt viewer | FINAL-PR-03 |
| Hub surface convergence (8765/8877/8878) | FINAL-PR-03 or later |
| Windows service/tray/installer | FINAL-PR-05 or later |

---

## Next PR Handoff to FINAL-PR-03

FINAL-PR-03 should:

1. Start QIRC Core runtime (or first slice of it)
2. Add deep activity/trace/receipt viewer to dev mode
3. Decide hub surface convergence (8765 vs 8877/8878)
4. Add handoff compiler runtime (not just placeholder)
5. Reuse: model picker UI, connected apps slots, demo Universal Work endpoints from FINAL-PR-02
