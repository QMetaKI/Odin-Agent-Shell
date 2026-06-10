# AI-Git Safety Architecture v7.1

## Purpose

Odin treats AI work like a reviewable versioned process. This does not mean Odin replaces Git. It means Odin borrows the safety logic of Git-like workflows and applies it to model outputs, routes, context, claims, runtime packs and candidates.

## Core Mapping

| Git-like concept | Odin concept |
|---|---|
| Commit | Candidate Artifact / Response Packet |
| Branch | Candidate Route / Candidate Variant |
| Diff | Worklet Delta / PatchPlan Candidate / Semantic Delta |
| Merge | Candidate Tournament / Synthesis Collapse |
| Commit message | Why Trace |
| Blame / provenance | Candidate DNA |
| Hook | Claim Boundary / Final Gate / Bug6 / Q7 Gate |
| Pull request | Thor Handoff / Review Packet |
| CI | Generated Gates / Golden and Negative Tests |
| Revert | Candidate rejection / Runtime Pack rollback |
| Remote | explicit external provider, never default authority |

## AI-Git Spine

```text
Universal Work
-> Branch Candidate Route
-> Semantic Diff / Worklet Delta
-> Candidate Artifact
-> Why Trace
-> Review / Gate
-> App-owned Apply or Reject
```

## Safety Properties

The AI-Git spine provides:

- provenance for every candidate,
- route reason for every model decision,
- blocked-route visibility,
- rejected-claim visibility,
- candidate-only state until the app decides,
- rollback path for runtime packs,
- testable gates,
- traceable human/app review.

## Non-Authority Rule

Odin may prepare a candidate. Odin may not commit it into app reality. The app remains the repository owner of state.

## Semantic Branches

A branch in Odin is not a Git branch. It is a route alternative:

```text
3B micro branch
7B quality branch
hybrid branch
hold branch
ask-context branch
block branch
```

Only candidate branches can be generated. No branch may mutate app state.

## Semantic Diff

A semantic diff captures what changed between:

- input artifact and candidate artifact,
- prior candidate and new candidate,
- context capsule and final packet,
- runtime pack source and compiled pack.

Every high-impact candidate should expose a semantic diff summary.

## Candidate Merge

Candidate merge means:

```text
candidate tournament + critic reports + synthesis collapse
```

It does not mean automatic apply.

## Why this improves LLM work

Models become less dangerous and more useful when their outputs become reviewable candidate branches rather than direct actions. This improves quality, safety, debugging and trust without requiring larger models.

## Required Gates

Every AI-Git flow must pass:

- binding gate,
- claim boundary gate,
- autonomy escalation gate,
- candidate-only gate,
- app-apply boundary gate,
- why-trace completeness check.
