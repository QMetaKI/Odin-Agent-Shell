# Q7 Bugfree Stability v7.1

Claim boundary: this document defines architecture, contracts, shadow behavior, and Codex build intent only. It does not claim host validation, model inference proof, network operation, deployment, security audit completion, app apply, or full implementation completeness.

## Purpose

Q7 is the stability and buglessness posture for Odin. In neutral public language it is the **Bugfree Stability Vector**. It does not mean a claim that the code has no bugs. It means every Odin route must prefer the path that reduces drift, contradiction, hidden authority, and unbounded complexity.

## Functional meaning

Q7 governs route cleanliness, failure containment, replayability, candidate-only preservation, negative-path discipline, state transition clarity, ring/radar deviation handling, model route minimization, and trace completeness.

## Q7 lifecycle

```text
Ingress
→ Q7 Surface Scan
→ Q7 Drift Check
→ Q7 Center Stability Score
→ Q7 Route Cleanliness Score
→ Q7 Negative Path Check
→ Q7 Candidate Final Gate
→ Q7 Trace Receipt
```

## Required outputs

The canonical packet is `odin_q7_stability_packet`. It contains `work_id`, `route_cleanliness_score`, `drift_risk`, `negative_path_coverage`, `replayability_status`, `candidate_boundary_status`, `decision`, and `repair_hint`.

## Q7 decisions

```text
allow
repair_slot
split_work
hold
block
```

## Q7 and QMath

Q7 modifies route score by penalizing unresolved holes, high drift risk, broad context, ambiguous authority, missing trace, and lack of negative path.

```text
q7_adjusted_score = route_score - drift_penalty - unreplayable_penalty - boundary_penalty
```

## Q7 and QIRC

QIRC emits `#q7.scan`, `#q7.drift`, `#q7.route_cleanliness`, `#q7.negative_path`, and `#q7.replayability`.

## Q7 and Shadow Runtime

Shadow Runtime must not be treated as close enough if Q7 cannot trace the path from contract to shadow object to fixture to test to real target module.

## Codex rule

Codex must add negative tests before expanding risky positive flows. Q7 treats negative path absence as a bug risk, even if the happy path works.

## Red lines

- No hidden fallback to broad model route.
- No untraced candidate artifact.
- No route without negative-path awareness.
- No schema repair that silently changes authority.
- No runtime pack without rollback path.
