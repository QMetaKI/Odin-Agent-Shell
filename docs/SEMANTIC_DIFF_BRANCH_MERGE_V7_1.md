# Semantic Diff / Branch / Merge v7.1

## Purpose

This document defines the AI-Git mechanics that make Odin outputs reviewable and non-blackbox.

## Semantic Branch

A semantic branch is a bounded route alternative. Examples:

```text
3b_micro_route
7b_quality_route
hybrid_route
hold_route
ask_context_route
block_route
```

Each branch must declare:

- input artifacts,
- active seeds,
- model plan,
- expected output contract,
- risk level,
- blocked claims,
- final gate requirements.

## Semantic Diff

A semantic diff reports what changed and why:

```json
{
  "diff_id": "SDIFF-001",
  "from_artifact": "ART-001",
  "to_candidate": "CAND-001",
  "changed_meaning": ["clarity improved"],
  "preserved_meaning": ["core facts", "tone boundary"],
  "removed_claims": ["unsupported certainty"],
  "risk_delta": "lower"
}
```

## Candidate Merge

Candidate merge is not app apply. It is candidate synthesis:

```text
candidate variants
+ critic reports
+ fit scores
+ claim boundary
-> merged candidate artifact
```

## Merge Gate

A merged candidate must include:

- Candidate DNA,
- Why Trace,
- semantic diff summary,
- rejected variants summary,
- blocked claims summary.

## Codex Rule

Codex must not implement any merge as app mutation. It may only implement candidate synthesis and Response Packet construction.
