# Model / Agent Why Trace v7.1

## Purpose

Why Trace must explain not only why Odin chose a route, but why it chose a particular model or agent.

## Required fields

- selected worker
- rejected workers
- capability card reason
- permission card reason
- privacy reason
- cost/latency reason
- quality estimate
- safety reason
- candidate-only status
- human/app apply status

## Example

```json
{
  "selected_worker": "local_3b_micro",
  "reason": "schema repair task; 3B sufficient; 7B quality gain below threshold",
  "rejected_workers": [
    {"worker": "hosted_large", "reason": "remote not allowed"},
    {"worker": "coding_agent", "reason": "no patchplan needed"}
  ],
  "final_gate": "candidate_only_preserved"
}
```

## Entblackboxing value

Users should be able to see why a small local worker was enough, why a large model was not used, why an agent was blocked, or why human/app review is required.


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
