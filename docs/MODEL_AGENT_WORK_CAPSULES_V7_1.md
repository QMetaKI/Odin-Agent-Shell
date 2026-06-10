# Model / Agent Work Capsules v7.1

## Purpose

Work Capsules are universal project/task state containers for any model or agent. They generalize project/workspace memory without turning Odin into a chat-memory blackbox.

## Capsule contents

Machine fields include `active_workers`, `active_seeds`, `candidate_history`, `permission_cards`, `capability_cards`, and `why_trace_refs`.

- caller manifest
- active capability pack
- active runtime pack
- model/agent capability cards
- permission cards
- active seeds and archetype roles
- QIRC hot window
- centerline packet
- admissibility decision
- semantic diff history
- candidate history
- accepted/rejected route memory
- app-owned apply decisions
- why traces

## Work Capsule vs Chat Project

A conversational project preserves chat continuity. An Odin Work Capsule preserves bounded work continuity. It can be used with ChatGPT-like models, local models, coding agents, or browser agents, but it always returns Candidate Artifacts.

## Storage rules

Raw private payloads are not stored by default. Capsules prefer digests, hashes, summaries, seed profiles, route outcomes, and accepted candidate patterns. Secrets are redacted before trace or support bundle export.


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
