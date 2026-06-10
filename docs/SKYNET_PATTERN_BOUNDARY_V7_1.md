# Skynet Pattern Boundary v7.1

## Purpose

This document defines what Odin can and cannot claim regarding autonomous AI risk.

## Claim Boundary

Odin does not solve every future AI safety problem. Odin does address a concrete dangerous local-tool pattern:

```text
model output -> authority -> tool access -> hidden apply -> network or loop -> self-reinforcing action
```

## Odin Countermeasures

Odin blocks this pattern through:

- Candidate Artifacts rather than direct actions,
- app-owned apply,
- no external send by Odin,
- no public QIRC core,
- no unvalidated Runtime Pack load,
- no model-generated executable code,
- no hot-path runtime generation,
- Bug6 / Children-First invariant,
- Q7 stability invariant,
- Autonomy Escalation Gate,
- Why Trace and Candidate DNA,
- Thor review/handoff discipline.

## Escalation Signals

The system must flag:

- repeated self-routing loops,
- model request for tool access outside pack manifest,
- attempt to reduce trace visibility,
- attempt to skip candidate-only output,
- attempt to convert preview into apply,
- attempt to expand QIRC beyond local/digest-safe mode.

## Required Response

If detected:

```text
hold -> explain -> produce safe candidate or block
```

## Public Language

Do not claim impossible guarantees. The safe phrasing is:

```text
Odin makes autonomous escalation visible, gated, reviewable and structurally difficult.
```

Not:

```text
Odin makes all AI risk impossible.
```
