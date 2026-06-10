# Protocol Boundary Policy

Current handoff: `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK`.
Runtime base: `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK`.
Actual Codex/GitHub PR ladder: `REAL-GH-PR-01..08`.
Internal traceability ladders: `PR-00..PR-123` and `REAL-PR-01..28` only.

Odin protocol surfaces define candidate-only interoperability. Universal Work Objects are inputs to bounded Odin work. Candidate Artifacts and Response Packets are outputs for caller/app review. They are not app-state mutation, external-send, deployment, runtime-proof, or production-readiness receipts.

Odin's implementation is GPL-2.0-only. Thor/Odin packets, schemas and protocol examples define interoperability shapes. Copying repository code, validators, SDKs or templates creates license obligations under the repository license. Independent implementations that interoperate through documented packet formats, CLIs or local APIs are treated by the project as separate implementations unless they copy GPL-covered implementation material.

Protocol invariants:

- Odin does candidate work; callers/apps do reality work.
- Apps own state, apply, storage, external sends, business logic, and domain authority.
- Providers are bounded workers, not authority.
- QIRC / Internal Semantic Bus is trace and receipt infrastructure, not app-state authority.
- No protocol packet may bypass `ODIN_BINDING`, Caller Manifest checks, output contracts, or app-owned apply gates.

This file is a technical policy and not legal advice.
