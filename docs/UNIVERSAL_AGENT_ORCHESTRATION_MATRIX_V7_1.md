# Universal Agent Orchestration Matrix v7.1

## Purpose

The orchestration matrix maps worker types to Odin roles, permissions, slots, and outputs.

| Worker type | Best Odin role | Allowed output | Default gate |
|---|---|---|---|
| 3B local model | CheapScout / MirrorCritic | micro candidates | candidate-only |
| 7B/8B local model | QualityScribe | section/review candidates | candidate-only |
| 13B/14B model | Quality Escalation | quality candidates | candidate-only |
| 30B/70B model | Heavy Batch / Final Polish | premium candidates | review required |
| coding agent | PatchPlan Worker | patchplan/review candidate | human/app apply required |
| browser agent | Research Scout | research candidate | source/claim gate |
| workflow agent | Task Planner | action-card candidate | app apply required |
| custom assistant/GPT-like model | Domain Worker | domain candidate | capability card required |

## Universal orchestration rule

Worker selection happens after Pre-LLM Intelligence, QIRC Hot Window, Seed/Archetype Prewarm, DFAS Admissibility, QMath Route Score, and Model Work Avoidance.


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
