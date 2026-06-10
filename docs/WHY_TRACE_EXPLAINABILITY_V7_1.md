# Why Trace Explainability v7.1

## Purpose

Why Trace turns Odin into an explainable local LLM orchestration system. It explains route, boundary, seeds, archetypes, scores, decisions and blocked alternatives without exposing secrets or raw private state.

## What Why Trace explains

- why the work was admissible
- why the selected center was chosen
- why the selected model route was sufficient
- why larger models were not used
- why a candidate was blocked or repaired
- why more context was requested
- why a route fell back
- why final output is candidate-only

## Why Trace levels

### internal_debug
Full trace for developer, redacted payloads only.

### app_safe
For app UI or logs, contains reasons and scores but not raw private state.

### user_safe
Small explanation suitable for user-facing surfaces.

## Data sources

- Centerline Packet
- Admissibility Decision
- Seed Activation Packet
- Archetype Role Packet
- QMath Route Score
- Ring Activation Map
- Candidate DNA
- Claim Gate Report

## Example user-safe trace

```text
Odin used the standard local hybrid route because the task required a quality rewrite but did not justify a larger model. A small model compressed and checked the context; the 7B/8B worker produced the draft; a small critic checked boundaries. The result is a candidate and still requires app apply.
```

## Redaction rules

- never include secrets
- never include credentials
- never include raw app databases
- never include blocked sensitive artifacts
- prefer ids, hashes, scores and summaries

## Codex Rule

Every meaningful Response Packet must link a why_trace_id unless privacy policy explicitly suppresses it.
