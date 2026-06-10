# Universal Model / Agent Parity v7.1

## Senior-review decision

The ChatGPT twin metaphor is useful, but it must not stay ChatGPT-specific. Odin must treat ChatGPT, local models, remote models, coding agents, browser agents, voice agents, workflow agents, custom assistants, IDE agents, and future model surfaces as **model/agent endpoints** that can participate only through bounded Odin contracts.

## One-line canon

```text
Any model. Any agent. Same Odin boundary.
```

## What parity means

Parity means every model or agent receives a normalized Odin interface:

```text
Model/Agent Identity
+ Capability Card
+ Permission Card
+ Work Capsule
+ Adapter Boundary
+ Candidate Protocol
+ Why Trace
+ Semantic Diff
+ App Apply Boundary
```

It does **not** mean every model has the same quality. It means every model is forced into the same bounded work discipline.

## Model/agent classes

- local micro model: 1B/2B/3B
- local quality model: 7B/8B/13B/14B
- local heavy model: 22B/32B/MoE/70B-class batch
- hosted conversational model
- coding agent
- browser/research agent
- IDE assistant
- workflow/automation agent
- app-native domain assistant
- human-review assistant surface

## Universal parity pipeline

```text
External/Local Model or Agent
→ Odin Model/Agent Adapter
→ Capability Card Check
→ Permission Card Check
→ Universal Work Binding
→ QIRC / QLI / DFAS / Seed Economy
→ Model Work Avoidance
→ Slot / Worklet / Route
→ Candidate Protocol
→ Semantic Diff / Why Trace
→ App-owned Apply Boundary
```

## Why this improves Odin

It prevents model-specific special-casing from becoming architecture drift. Whether the worker is a tiny local 3B, a strong hosted model, a coding agent, or a future tool-using assistant, Odin sees: capabilities, risk, permission posture, allowed outputs, blocked routes, trace, and candidate-only result.


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


## Required implementation stance

Codex must build this as an adapter-neutral boundary. No provider-specific behavior may bypass the shared model/agent card, permission card, candidate protocol, or why trace. Provider-specific optimizations are allowed only after the universal boundary passes.
