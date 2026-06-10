# Codex Runtime Candidate Handoff v0.8.0

Codex should treat this artifact as a running source candidate, not as a finished Windows product.

## First commands

```text
python -m odin.cli validate-all
python -m pytest -q
python -m odin.cli doctor
python -m odin.cli run-work examples/runtime/universal_work_full.valid.json --seed-pack examples/runtime/app_seed_pack_full.valid.json --pattern-mine examples/runtime/pattern_mine_full.valid.json
```

## Codex priorities

1. Preserve candidate-only/app-owned apply boundary.
2. Harden types and error handling.
3. Replace mock model worker with provider adapters behind the same worker-card contract.
4. Harden local API auth and Windows IPC.
5. Keep all seed/pattern/flow packs declarative.
6. Add host receipts only from actual host runs.

## Stop conditions

Stop before adding auto-apply, network QIRC, executable seed packs, unverifiable model claims, or hidden authority elevation.
