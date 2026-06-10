# Senior Review Simulation — v0.8.7 Codex Real PR Ladder


Base: `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`.
## Verdict

The eight-PR ladder is now correctly reframed for the post-v0.8.6 state.
The previous ladder described the full build from architecture. The new ladder describes completion and hardening of a running runtime candidate.

## Strengths

- The actual GitHub PR count remains small: eight PRs.
- Each PR now states what ChatGPT already materialized.
- Codex receives precise completion work rather than open-ended architecture interpretation.
- Host/model/provider claims remain bounded.
- Windows host work is isolated into its own PR.
- Runtime core, provider boundary, handoff/review, narrative/shadow, seeds/patterns, SDK/release gates are separated enough for review.

## Risks

1. Codex may over-edit across PR boundaries.
2. Codex may treat stubs as proof.
3. Codex may collapse provider and authority boundaries.
4. Windows host proof may be claimed from non-Windows runs.
5. Narrative/Shadow/Loki modules may become decorative if not tied to gates and tests.

## Required mitigations

- Every PR must produce a return report.
- Every PR must keep app-owned apply.
- Every PR must keep Odin candidate-only.
- Provider work must distinguish stubs, optional adapters, and actually verified inference.
- Windows PR must distinguish scripts/stubs from host receipts.
- Final release PR must separate implemented, prepared, skipped, and blocked items.

## Final recommendation

Proceed to Codex with REAL-GH-PR-01 first.
