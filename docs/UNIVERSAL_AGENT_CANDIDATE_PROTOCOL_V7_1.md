# Universal Agent Candidate Protocol v7.1

## Purpose

Any model or agent that participates in Odin must return candidate work, not authority. This protocol defines a common response shape for local models, hosted models, coding agents, browser agents and future agent systems.

## Candidate packet family

- text_candidate
- action_card_candidate
- code_review_candidate
- patchplan_candidate
- browser_research_candidate
- workflow_candidate
- scheduled_candidate_work
- human_review_request
- blocked_route_report

## Required response fields

```json
{
  "candidate_id": "CAND-001",
  "worker_id": "local_7b_quality",
  "work_id": "WORK-001",
  "candidate_type": "patchplan_candidate",
  "content": {},
  "claims": [],
  "blocked_claims": [],
  "requires_app_apply_gate": true,
  "why_trace_ref": "WHY-001",
  "semantic_diff_ref": "DIFF-001",
  "candidate_dna_ref": "DNA-001"
}
```

## Agent output normalization

If a coding agent proposes a patch, Odin stores it as PatchPlan Candidate or Semantic Diff Candidate. If a browser agent finds sources, Odin stores them as Research Candidate. If a workflow agent suggests action, Odin stores Action Card Candidate. None may execute through Odin.

## Forbidden outputs

- applied
- sent
- purchased
- deleted
- deployed
- tests_passed unless receipt exists
- security_verified unless receipt exists
- production_ready unless receipt exists


## Non-negotiable boundaries

- No model or agent receives app authority.
- No model or agent can apply app state changes through Odin.
- No model or agent can send externally through Odin.
- No model or agent can bypass Binding Gate, Admissibility Gate, Claim Boundary, Human/App Apply Boundary, Runtime Pack Validation, or Odin Final Gate.
- No model or agent identity becomes a persona authority. Model identity is a capability descriptor only.
- No connector, assistant, coding agent, browser agent, IDE agent, local model, remote model, or custom assistant is trusted as runtime truth.
- All outputs are Candidate Artifacts until the app/user accepts them in the app-owned apply layer.

## Canonical relation

Universal Model/Agent Parity generalizes the earlier ChatGPT/Odin twin idea. ChatGPT is one instance of a user-facing conversational model surface. Other models and agents are other surfaces. Odin is the control, candidate, trace, gate and runtime-pack layer that makes any model or agent behave like bounded work inside a reviewable system.

## Purpose

The goal is not to make every model behave the same. The goal is to make every model and agent interoperable with the same Odin work discipline: Work Capsule, Capability Card, Permission Card, Model/Agent Adapter, Candidate Protocol, Semantic Diff, Why Trace, and App-owned Apply.
