# FINAL-PR-05 Execution Gate + Ladder Scaffold Rebaseline

**claim_boundary:** `final_pr_05_rebaseline_candidate_only_not_production_proof`
**candidate_only:** true
**generated_at:** 2026-06-12T19:00:00Z

## Rebaseline Purpose

Documents the new baseline after FINAL-PR-05 merge. Successor PRs should read this before starting cognition.

## New Surfaces Added

### Execution Gate (`odin/execution_gate/`)

- `policy.py` — `ExecutionGatePolicy` dataclass. Default: mock_execution_allowed=true, all real execution false.
- `gateway.py` — `ExecutionGateway` class. Policy-first dispatch. Emits QIRC events.
- `mock_provider.py` — Deterministic mock execution. No model. No subprocess.
- `local_candidate_policy.py` — `LocalCandidatePolicy` for ollama_candidate and llama_cpp_candidate. Both blocked by default.
- `proof.py` — `build_execution_gate_proof_packet()` builder.

### Proof Chain (`odin/proof_chain/`)

- `registry.py` — `PROOF_CHAIN_REGISTRY` with entries for FINAL-PR-01 through FINAL-PR-05.
- `builder.py` — `build_proof_chain()` returns unified chain with existence checks.

### FINAL-PR Ladder Scaffold (`odin/final_pr_ladder/`)

- `compiler.py` — `LadderCompiler.compile()` → 7-section worker packet scaffold.
- `templates.py` — `WORKER_PACKET_SECTIONS` list.
- `proof.py` — `build_ladder_scaffold_proof()` builder.

### Local Hub Endpoints Added

- `GET /execution-gate/status.json` — execution gate policy
- `POST /execution-gate/mock` — deterministic mock execution
- `GET /execution-gate/proof-chain.json` — proof chain cross-references
- `GET /final-pr-ladder/scaffold.json` — FINAL-PR-06 scaffold

### CLI Commands Added

- `validate-final-pr-05-execution-gate`
- `prove-final-pr-05-execution-gate`
- `prove-final-pr-proof-chain`
- `prove-final-pr-ladder-scaffold [--target FINAL-PR-06]`
- `final-pr-ladder-scaffold`

### UI IDs Added

- `execution-gate-status`
- `mock-execution-panel`
- `mock-execution-result`
- `local-candidate-policy-status`
- `execution-boundary-status`
- `proof-chain-status`
- `final-pr-ladder-scaffold-status`
- `model-execution-warning`

### Runtime Security Smoke Extended

- Scans `odin/execution_gate/` in addition to `odin/providers/` and `odin/runtime_security/`
- Checks `DEFAULT_EXECUTION_GATE_POLICY` for forbidden flag values

## Current Boundary State

| Boundary | State |
|----------|-------|
| Mock execution | ALLOWED (deterministic, no model) |
| Local candidate execution | BLOCKED by default |
| Ollama generate/chat/embed | BLOCKED |
| llama.cpp model run | BLOCKED |
| Remote provider execution | BLOCKED |
| API key reads | BLOCKED |
| External network | BLOCKED |
| App apply | BLOCKED (app-owned) |
| External send | BLOCKED (app-owned) |

## Known Gaps (for FINAL-PR-06)

- Real local model execution requires `LocalCandidateGateToken`
- QIRC execution event viewer not yet in dev mode
- Full prompt compiler not yet implemented (Thor vNext)
- Proof chain not yet extended to PR-06
