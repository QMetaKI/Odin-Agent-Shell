# FINAL-PR-08: Projection Spine + Expression Packet + Shadow Candidate Graph

## Purpose / Objective

Implement neutral projection layers that map a selected seed/field route into human-clear projection, expression packet, machine projection, shadow candidate graph, and materialization bridge. The implementation improves near-code candidate quality, Dev Mode explainability, narrative/expression-to-machine mapping, Shadow Runtime style candidate graphs, and worker prompt precision.

## Base rule

Base: current main after FINAL-PR-07 merge. Do not base on open PR branches. Do not rewrite historical merged PRs.

## Allowed scope

Create the smallest deterministic, local-only projection package. Add docs, neutral registries if needed, tests, validator, CLI hooks, proof packet, SYSTEM_MAP and FILE_MANIFEST updates. Preserve candidate-only outputs.

## Forbidden scope

No provider execution, model inference, API key reads, external network, public QIRC/network/federation, app apply, app state mutation, external send, production readiness claim, security certification claim, hidden authority, religious interpretation, persona injection, source-pattern runtime import, or Q-style new runtime artifact names.

## Files to create

- `odin/projection_spine/__init__.py`
- `odin/projection_spine/expression_packet.py`
- `odin/projection_spine/shadow_candidate_graph.py`
- `odin/projection_spine/materialization_bridge.py`
- `odin/projection_spine/proof.py`
- `tools/rebaseline/check_projection_spine.py`
- `tests/test_final_pr_08_projection_spine.py`
- `reports/final_pr_08_projection_spine_proof_packet.json`

## Required objects

- `ProjectionSpine`
- `ExpressionPacket`
- `MachineProjection`
- `ShadowCandidateGraph`
- `MaterializationBridge`
- `ProjectionReceipt`

## Source concepts allowed in docs/audits only

- Narrative Aorta
- Fairy DSL
- Shadow Runtime
- Q*

New runtime artifacts must use neutral names only.

## CLI commands

- `python -m odin.cli validate-projection-spine`
- `python -m odin.cli explain-projection --demo`
- `python -m odin.cli prove-projection-spine`

## Validator requirement

Create `tools/rebaseline/check_projection_spine.py`. It must verify files, neutral naming, required objects, projection receipt boundaries, candidate-only/local-only/app-owned-apply flags, forbidden scope text, no provider/model execution, no app apply/state/external-send authority, no new forbidden Q-style runtime/schema/registry/CLI artifact names, and proof packet shape.

## Tests requirement

Create `tests/test_final_pr_08_projection_spine.py` covering projection assembly, expression packet shape, machine projection shape, shadow candidate graph edges, materialization bridge candidate-only output, projection receipt, negative boundaries, CLI validator, proof packet generation, and `validate-all` integration.

## Proof packet requirement

Create `reports/final_pr_08_projection_spine_proof_packet.json` via `prove-projection-spine`. It must state `candidate_only: true`, `local_only: true`, `app_owned_apply: true`, no provider/model execution, no network, no app apply/state/external-send, and no truth authority.

## Required invariant

Projection prepares candidate clarity. Projection is not code truth, not model truth, not runtime proof. Shadow Candidate Graph is compile-near candidate structure, not executable runtime.

## Senior review loop

Before finalizing, simulate a senior reviewer and a senior code reviewer. Confirm the implementation is bounded, neutral, deterministic, small, test-covered, and does not add hidden authority or runtime/model/app claims. Apply fixes before the final response.

## Final response format

Return summary, files changed, what remains scaffold, non-claims, and exact tests run. Each test/check command must be prefixed with pass/warn/fail status.
