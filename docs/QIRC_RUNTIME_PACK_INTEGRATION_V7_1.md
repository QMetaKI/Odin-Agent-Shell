# QIRC Runtime Pack Integration v7.1

## Objective

Use QIRC channel/seed/role/policy maps to compile minimal Runtime Packs and Capability Slices.

## Runtime Pack Use

A capability slice should include only the QIRC channels and roles needed for the caller. A wedding studio slice does not need bounded-code or game-state channels. A code review slice does not need wedding speech roles.

## Compile Inputs

Caller Manifest, Resource Profile, Allowed Artifacts, Allowed Verbs, Output Contracts, Seed Budgets, Archetype Roles, Channel Registry and Model Scale Ladder.

## Compile Outputs

Compiled channel registry, event validators, module dispatch map, retention policy, route score table, why-trace fields and negative gates.


## Required Runtime Behavior

The real implementation must keep this component deterministic where possible, typed at the boundary, local-only by default and candidate-only at output. Any future implementation must include positive and negative fixtures, registry entries, system map references and Codex task mapping.

## Failure Behavior

On malformed input, missing trace_id, missing privacy_class, authority escalation, direct apply request, raw secret payload or unbounded event fanout, this component must fail closed and emit a blocked QIRC event or an admissibility hold record.

## Codex Conversion Rule

Codex must build this as a small typed module with no hidden agent autonomy. If a model provider would be required, Codex must instead create a candidate ModelWorkPacket or a hold/split/ask_context route unless the provider stage has already been implemented under the correct PR bundle.

## Required Phrase: compiled channel

Each Runtime Pack must expose a compiled channel map. The compiled channel map is the exact QIRC subset that the capability slice may use.
