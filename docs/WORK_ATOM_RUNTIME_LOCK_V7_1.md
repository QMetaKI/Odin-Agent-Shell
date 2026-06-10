# Work Atom Runtime Lock v7.1

## Purpose
Work Atoms are the smallest meaningful units of Odin AI work. They make small models better, reduce unnecessary model calls, increase explainability and allow Pattern Mines, Seed Packs, QIRC and Runtime Packs to compose high-quality output from tiny verified steps.

## Definition
A Work Atom is a typed, bounded, candidate-only micro-operation with a clear input contract, output contract, allowed worker class, forbidden claims, gate requirements, cost estimate, result status and Why Trace link.

## Work Atom examples
- `claim_check_atom`
- `json_repair_atom`
- `context_compress_atom`
- `boundary_scan_atom`
- `seed_conflict_atom`
- `qmath_score_atom`
- `ring_pressure_atom`
- `slot_forge_atom`
- `candidate_variant_atom`
- `semantic_diff_atom`
- `why_trace_atom`
- `support_bundle_redaction_atom`

## Runtime pipeline
Universal Work -> Pattern/Seed/Context analysis -> Worklet Graph -> Work Atom Graph -> Model Work Avoidance -> no-model/1B/3B/7B/hybrid selection -> atom results -> micro-to-macro candidate synthesis -> Candidate Artifact.

## Budget rules
Work Atoms are not free. Every graph has a budget: max atom count, max loop count, max model atoms, max critic atoms, max token estimate, max latency band. If budget fails, Odin must split work, ask context, downgrade scope or hold.

## Atom status
`planned`, `skipped`, `executed_no_model`, `executed_model`, `blocked`, `deferred`, `merged`, `invalid`, `needs_review`.

## Anti-patterns
- atom hydra: atom graph expands without gain.
- model atom overuse: small no-model atoms replaced by model calls.
- hidden apply atom: atom attempts state mutation.
- untraceable atom: result cannot be tied to input/output contract.
- critic loop: repeated checks without measurable improvement.

## Required DoD
Codex must implement Work Atom schemas, graph fixtures, atom budget gate, no-apply enforcement, micro-to-macro synthesis docs, QIRC event mapping and tests proving that Work Atoms do not mutate app state or bypass Candidate Artifact assembly.
