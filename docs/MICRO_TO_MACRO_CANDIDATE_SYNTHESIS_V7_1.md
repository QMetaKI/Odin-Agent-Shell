# Micro-to-Macro Candidate Synthesis v7.1

Status: Odin Agent Shell v7.1 integrated lock. This document is specification and shadow-runtime preparation only. It does not claim runtime proof, model proof, host validation, deployment, security audit completion, production readiness, app apply, or external send.

Core invariants preserved: app owns state, app owns apply, Odin returns candidate artifacts, models remain bounded projection workers, QIRC is local/internal, no hot-path runtime generation, no prose-only execution, no unvalidated runtime pack load, and all visible intelligence must remain traceable by Candidate DNA / Why Trace.


## Definition
Micro-to-Macro Synthesis combines many small reliable micro-results into a larger coherent Candidate Artifact.

## Micro Results
- intent label
- active seed list
- no-go result
- context capsule
- route score
- schema check
- style check
- mini rewrite
- candidate action hints
- why trace fragments

## Macro Candidate
A macro candidate is not one model output. It is composed from verified parts:
```text
micro findings + model fragments + critic reports + output contract + app renderer hints
→ user-visible candidate bundle
```

## Synthesis Rules
- Preserve source references.
- Prefer specific verified facts over generic language.
- Include uncertainty when material is incomplete.
- Collapse variants only when fit score justifies it.
- Do not merge contradictory micro-results; route to MirrorCritic or ask context.

## Effect
3B micro-results can make a 7B answer more grounded. No-model results can make a 3B answer feel app-aware. Large models can be reserved for only the macro piece that requires synthesis.

## Contract Field Anchor
The canonical contract field is `micro_results`; each micro_result must preserve its source, confidence, risk, and candidate-only boundary before macro synthesis.
