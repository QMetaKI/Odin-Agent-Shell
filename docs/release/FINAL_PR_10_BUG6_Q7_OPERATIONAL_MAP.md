# FINAL-PR-10 Bug6 and Q7 Operational Map

**claim_boundary:** `final_pr_10_boundary_gated_release_operationalization_not_release_certification`
**candidate_only:** true
**app_owned_apply:** true

---

## Overview

This document maps Bug6 and Q7 to their operational mechanisms in the boundary-gated release system. Bug6 maps to `authority_drift_scanner`; Q7 maps to `boundary_coherence_scanner`.

---

## Bug6 — Authority Drift Scanner

**Formal Name:** `authority_drift_scanner`
**Ring:** Ring 2 (Operational Authority Layer)
**Origin:** Bug6 = Children-First Invariant (BUG6_CHILDREN_FIRST_INVARIANT_V7_1.md)

### What Bug6 Guards Against

Bug6 detects **authority drift** — the condition where a child subsystem, agent, or candidate begins exercising authority that belongs to a parent or the app layer. In tree-structured work graphs, authority must flow downward (app → orchestrator → agent → candidate). Upstream leakage constitutes an invariant violation.

### authority_drift_scanner — Operational Behavior

The scanner inspects candidate packets and work atoms for:

1. **Upstream authority claims** — A candidate claiming to apply state owned by a parent scope.
2. **Ring escalation without receipt** — A child agent claiming Ring 3 or Ring X authority without an explicit escalation receipt in its packet.
3. **Delegation chain breaks** — A subsystem delegating to another subsystem without a proper handoff candidate in the chain.
4. **Apply authority leak** — Any candidate field that implies direct state application (e.g., `apply: true` without `app_owned_apply: true`).

### Scanner Output

The `authority_drift_scanner` returns a structured report:

```
{
  "scanner": "authority_drift_scanner",
  "bug6_violations": [...],
  "drift_detected": bool,
  "candidate_only": true,
  "claim_boundary": "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
}
```

The scanner emits candidates only — it does not remediate drift.

---

## Q7 — Boundary Coherence Scanner

**Formal Name:** `boundary_coherence_scanner`
**Ring:** Ring 2 (Operational Authority Layer)
**Origin:** Q7 = Bug-Free Stability Core (Q7_BUGFREE_STABILITY_V7_1.md)

### What Q7 Guards Against

Q7 detects **boundary incoherence** — the condition where a candidate, seed pack, or agent transitions between subsystems without maintaining a coherent claim boundary declaration. Incoherence manifests as:

- Missing `claim_boundary` field in candidate packets
- Mismatched `claim_boundary` values across a handoff chain
- `candidate_only: false` or missing in any emitted packet
- Proof packets that claim more than their `claim_boundary` permits

### boundary_coherence_scanner — Operational Behavior

The scanner validates:

1. **Claim boundary presence** — Every candidate packet in the pipeline has a non-empty `claim_boundary`.
2. **Boundary chain coherence** — Handoff candidates propagate the same or more restrictive `claim_boundary` as the originating packet.
3. **Candidate flag coherence** — `candidate_only: true` is present and not overridden.
4. **Proof packet honesty** — Every proof packet includes a `not_proven` list; no proof overclaims its boundary.

### Scanner Output

```
{
  "scanner": "boundary_coherence_scanner",
  "q7_violations": [...],
  "coherence_ok": bool,
  "candidate_only": true,
  "claim_boundary": "final_pr_10_boundary_gated_release_operationalization_not_release_certification"
}
```

---

## Bug6 + Q7 Combined Gate

In the release preflight (Ring 3), both scanners run in sequence:

1. `authority_drift_scanner` (Bug6) runs first — detects upstream authority leaks.
2. `boundary_coherence_scanner` (Q7) runs second — detects cross-boundary incoherence.

Both must return clean (no violations) for the preflight gate to pass.

---

## Not Proven

- `production_readiness`
- `live_model_inference`
- `app_state_mutation`
- `external_send_authority`
- `release_certification`
