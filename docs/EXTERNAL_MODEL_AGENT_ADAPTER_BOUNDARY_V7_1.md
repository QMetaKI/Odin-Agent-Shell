# External Model / Agent Adapter Boundary v7.1

## Purpose

This doc defines how external models or agents are attached to Odin without becoming authority.

## Adapter responsibilities

- normalize request into ModelWorkPacket or AgentWorkPacket
- enforce privacy class
- redact secrets
- attach permission card
- apply output contract
- convert raw response to Candidate Artifact
- block direct apply/action claims
- attach why trace and candidate DNA

## Adapter red lines

- no direct tool execution through Odin
- no direct app state mutation
- no raw secret forwarding
- no unbounded browser or file crawl
- no self-modifying runtime pack generation
- no worker-specific bypass of Claim Boundary

## Supported adapter families

- local model provider adapter
- hosted model provider adapter
- coding agent adapter
- browser/research agent adapter
- IDE assistant adapter
- workflow agent adapter
- human-review adapter


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
