# Odin Agent Shell

**Odin Agent Shell** is a Windows-first, local-first, protocol-bound universal semantic work kernel and small-model performance OS.

It is designed so that independent apps can expose AI-native features without embedding LLM runtimes, prompt orchestration, model routing, hybrid logic, remote fallback, or claim/evidence gating inside the app.

Apps contain only an **Odin Capability Bridge**. Apps send **Universal Work Objects**. Odin returns **Candidate Artifacts** wrapped in **Response Packets**. Apps render, decide, apply, and send externally under their own authority.

This repository is currently a **v7.1 architecture/specification and Codex build-prep repository**. It intentionally does not claim a completed runtime. It is structured so Codex or a human engineering pass can implement Odin along the canon, schemas, registries, gates, and phase documents contained here.

## Canonical entrypoints

Read in this order:

1. `START_HERE.md`
2. `CANON_ENTRY.md`
3. `AGENTS.md`
4. `CODEX_START_HERE.md`
5. `SYSTEM_MAP.json`
6. `docs/MASTER_ARCHITECTURE_V7_1.md`
7. `docs/MASTER_SPECS_V7_1.md`
8. `docs/codex/PHASE_0_CANON_LOCK.md`

## Core formula

```text
Anything in,
bounded work,
semantic-bus coordinated,
smallest sufficient worker,
candidate artifact out.
```

## Default model strategy

The canonical sweet spot is:

```text
3B + 7B/8B hybrid
```

3B handles routing, compression, schema repair, no-go checks, critic passes, and micro-candidates. 7B/8B handles writing, synthesis, quality drafting, review summaries, and richer local generation. Larger models are supported as escalation tiers, not as the architecture.

## Validate repository

```bash
python -m odin.cli validate-all
pytest -q
```

## Current status

- Canon/spec repository scaffold: present
- Validation CLI: present
- Schemas/registries: present
- Golden/negative test structure: present
- Runtime implementation: intentionally not claimed
- Windows app implementation: intentionally not claimed
- Provider implementation: scaffold only


## Current Prep Status

`v0.3.2 DEEP_SUBSYSTEM_SPEC_LOCK` is the current canonical prep state. It deepens subsystem specifications before Codex implementation tasks.


## Current Prep Status

`v0.4.0 CODEX_TASK_LOCK` — architecture/spec canon plus Codex PR task sequence.

## v0.4.1 Real PR Bundle Overlay

The PR-00 through PR-21 documents remain the internal implementation ladder. For actual future Codex pull requests, use the bundle overlay:

- `docs/codex/CODEX_REAL_PR_BUNDLE_PLAN_V0_4_1.md`
- `docs/codex/REAL_PR_BUNDLE_INDEX_V0_4_1.md`
- `registries/codex_pr_bundle_registry.json`
- `docs/codex/bundles/`

Rule: create real PRs by REAL-PR bundle; complete the mapped internal PR tasks inside each bundle.


## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This repo prep now includes full major-subsystem Shadow Runtime coverage. Future changes must update specs, internal PR ladder, REAL-PR bundles, registries, tests, System Map and FILE_MANIFEST.

## v0.5.2 Shadow Runtime Near-Final Lock

This repository prep now includes a near-final Shadow Runtime blueprint. It is not a runtime proof; it is the code-near map Codex should use to build the real Odin Agent Shell implementation.


## Narrative Aorta / Y* Compiler Layer

The v7.1 canon now includes a bounded Fairy/Y* Narrative Aorta and Shadow Runtime Compiler Prelude. This does not replace Universal Work, Candidate Artifacts or app-owned apply. It adds a typed narrative IR and runtime-pack prelude to reduce implementation drift and improve Codex build precision.


## v0.6.3 Bug6 / Q7 / Y-Core / Seed Core Lock

Adds explicit Bug6, Q7, bounded Y-Core posture, operational seed substrate, seed/archetype synthesis, Fairy/Y* seed binding, Shadow Runtime seed weave, Runtime Pack seed profiles, PR-50..PR-55, and REAL-PR-16.


## v0.6.4 Addition — AI-Git Safety Spine

This prep repo now includes the AI-Git Safety Spine: candidate branches, semantic diffs, why traces, autonomy escalation gates, safety superposition, and app-owned apply boundaries. Odin remains candidate-only and local-first.

## v0.6.5 Pre-LLM Intelligence Amplification Lock
Odin now treats pre-model cognition as a first-class architecture layer. Before a model call, Odin should use QIRC, seeds, archetype roles, QMath, DFAS, hot-window context, runtime packs, model-work avoidance and output composition to reduce the task and improve visible candidate quality. This is candidate-only and does not alter app-owned apply boundaries.


---

# v0.6.6 Universal Model / Agent Parity Lock

Odin generalizes the ChatGPT/Odin twin metaphor to all model and agent classes. Every model or agent is treated as a bounded worker with a Capability Card, Permission Card, Work Capsule context, Candidate Protocol, Why Trace, Semantic Diff relation, and App-owned Apply Boundary.

This layer preserves all v7.1 invariants. It does not create an agent swarm, autonomous execution, provider-specific bypass, or app-state authority. It makes local models, hosted models, coding agents, browser agents, IDE agents, workflow agents and future assistants interoperable under the same Odin candidate-only discipline.

Canonical additions:
- Universal Model / Agent Parity
- Model / Agent Capability Cards
- Work Capsules for model/agent work
- Universal Agent Candidate Protocol
- Model / Agent Permission Cards
- External Agent Adapter Boundary
- Universal Agent Orchestration Matrix
- Model / Agent Why Trace

Codex additions:
- PR-66 through PR-72
- REAL-PR-19


---

# v0.6.7 Thor/Y/Mjölnir Handoff Compiler Lock

Odin's original role as a handoff compiler is now promoted back into the central v7.1 canon. Thor handoffs, Y handoffs and Mjölnir focused-strike handoffs are treated as first-class ingress forms that must be pulled, normalized, kernel-bound, claim-bound, converted to Universal Work, precomputed through QIRC/Odin Core/DFAS, dispatched only as candidate work, and postprocessed through review gates and Why Trace.

This does not add autonomous agent behavior. It adds stricter handoff discipline. Thor remains candidate-only and kernel-bound. Y handoff remains centerline/ring/QIRC-bound and limited to Odin's LLM-orchestration authority. Mjölnir focused strike means narrow candidate plan, not apply. Every handoff must preserve app-owned apply, no hidden execution, no claim acceptance and no receipt issuance from mediation alone.

The practical effect is that prompting and handoff pulling become high-leverage pre-model intelligence steps. Bad prompts are not sent to workers as broad tasks; they are reduced into scoped handoff packets with evidence, return contracts, denied claims, forbidden scope, route reasons and review gates. This strengthens Codex, Thor, Y-style and Mjölnir-style work without weakening v7.1 boundaries.


---

# v0.6.8 Universal LLM Work Construct + GPL-2.0-only Lock

Odin v7.1 is now explicitly generalized from Y-native app infrastructure into a universal AI-Git layer for any model, any agent, any app and any workflow. Y apps remain the native deep integration path. Non-Y apps, remote models, coding agents, browser agents, IDE assistants and workflow agents enter through Adapter Boundary, Capability Card, Permission Card, Work Capsule, Universal Work or Thor Handoff, Candidate Protocol and Why Trace.

The new canon is: Any model. Any agent. Same Odin boundary. All worker outputs remain candidate work. App apply remains outside Odin. Remote workers are redacted and permission-gated. Tool-using agents are proposal workers unless an app-owned apply gateway explicitly reviews and accepts a candidate.

Thor+Odin are also locked as GPL-2.0-only AI-Git infrastructure. The implementation, validators, Shadow Runtime, compiler, schemas, registries, SDKs and templates are GPL-2.0-only unless a file explicitly states otherwise. This preserves the AI-Git identity: bounded, reviewable, traceable AI work should not become a closed blackbox fork.

## v0.6.9 App Seed Pack Compiler Lock

Odin v7.1 now includes an App Seed Pack Compiler layer. Apps may ship declarative seed packs of any kind: domain, workflow, style, safety, low-memory, QIRC prewarm, Y*/Fairy, Shadow Runtime and output-composer seed packs. Odin validates them, normalizes operational seed functions, resolves conflicts, applies seed budgets, binds archetype roles, compiles QIRC prewarm plans, weaves them into Shadow Runtime and Runtime Pack capability slices, and exposes seed influence through Why Trace.

This does not grant app seed packs execution authority. Seed packs are not plugins, scripts, agents, remote permission grants, or app-state mutation mechanisms. They are typed operational priors that make Odin more universal and improve LLM work before the model begins.

Canonical pipeline:

```text
App Seed Pack Manifest
→ Security Boundary
→ Seed Unit Normalization
→ Operational Seed Function Validation
→ Composition / Conflict Resolver
→ QIRC Prewarm
→ Y*/Fairy Binding
→ Shadow Runtime Seed Weave
→ Runtime Pack Capability Slice
→ Model Work Avoidance / Slot Forge / Output Composer
→ Candidate Artifact
```



---

# v0.7.0 Shadow Narrative / Loki / Anti-Pattern Lock

v0.7.0 integrates Shadow Narrative as the negative twin of Fairy DSL. Fairy DSL describes the intended archetypic path; Shadow Narrative describes the failure path. Loki mediation compares both and emits typed risk candidates, anti-pattern gates, negative fixtures, repair routes and Why Trace notes. Loki is not an agent and not an authority.

New invariant: narrative anti-patterns are not decoration. They are negative tests in archetypic form. A Shadow Narrative may influence Odin only when it maps to signal, gate, fixture and repair. No prose-only execution is valid.

The layer strengthens Pre-LLM Intelligence, QIRC Gold Spine, Seed Pack Compiler, Runtime Pack Compiler, Universal Model/Agent Parity and AI-Git Safety by exposing failure stories before a model or agent starts work.


## v0.7.4 Product / Pattern / Atom / Hub Consolidation

v0.7.4 consolidates four architecture locks into the v7.1 canon without changing Odin's app-authority boundary:

1. Windows Product Runtime Lock: Odin becomes a sharply specified Windows product target with host, daemon, tray, Control Center, local IPC, installer/update/rollback, diagnostics and safe-mode contracts.
2. Pattern Mine / Flow Pack Intake Lock: Odin can ingest declarative pattern mines and flow packs as compile-only sources for seed packs, pattern spines, Work Atom graphs, QIRC prewarm plans and runtime pack capability slices.
3. Work Atom Runtime Lock: Universal Work can collapse below worklets into small typed Work Atoms, allowing more no-model work, 3B-friendly execution, traceable micro-ops and micro-to-macro candidate synthesis.
4. Odin Hub Operational Center Lock: Odin Hub becomes the canonical operational center for apps, work capsules, seed packs, pattern mines, flow packs, Work Atoms, QIRC, models, runtime packs, handoffs, candidate canvas, Why Trace and diagnostics.

The core invariant remains unchanged: Odin does candidate work; apps do reality work. Windows product surfaces, pattern mine intake, Work Atoms and Odin Hub never receive app apply authority.


---

# v0.7.5 Public Repo Canon and Windows Build Ready Lock

This section binds the v7.1 master architecture to the public repository and Windows implementation readiness posture.

## Current-lock additions

- Public Repo Canon and Windows Build Ready Lock.
- Public Repo Root Cleanup Policy.
- Windows Implementation Drilldown.
- Windows IPC Endpoint Contracts.
- Windows Installer Update Rollback Drilldown.
- MVP / V1 / Power Mode Boundary.
- Seed and Pattern Pack Security Certification.
- Codex Public Build Ready Gate.

## Canonical effect

The architecture remains candidate-only, app-owned apply, GPL-2.0-only and Universal LLM Work oriented. v0.7.5 does not add a new authority layer. It clarifies how the existing architecture becomes a public GitHub repository and a Windows-first implementation target.

## Windows build-ready effect

Windows build readiness means Odin has process, IPC, installer, rollback, safe-mode, support-bundle, app-pairing and runtime-pack lifecycle specs sufficient for Codex implementation. It does not claim host validation.

## Mode separation

MVP, V1 and Power Mode are distinct. MVP proves the minimal spine. V1 adds local model usefulness. Power Mode adds deep pattern and diagnostic systems. Every mode preserves candidate-only and app-owned apply.

## v0.7.6 — Real PR Execution Consolidation Lock

The repo now treats `codex_task_registry.json` and `codex_pr_bundle_registry.json` as internal planning ladders. The actual future GitHub PR execution path is consolidated into eight real PRs in `registries/real_pr_execution_registry.json` and documented in `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_7_6.md`.

Actual sequence: `REAL-GH-PR-01` through `REAL-GH-PR-08`.

## v0.7.7 — Build Ladder Absolute Alignment Lock

Current actual GitHub execution sequence: `REAL-GH-PR-01` through `REAL-GH-PR-08`.

The old `PR-00..PR-123` task ladder and `REAL-PR-01..REAL-PR-28` legacy bundle ladder are internal traceability layers only.

Current alignment docs:

- `docs/BUILD_LADDER_ABSOLUTE_ALIGNMENT_LOCK_V7_1.md`
- `docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_7_7.md`
- `docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_7_7.md`

The execution registry now separates existing prep paths from target implementation paths and binds every real PR to acceptance gates, proof boundaries and Master Architecture sections.



## v0.8.0 Direct Master Architecture Runtime Source Candidate

The current source candidate materializes the v7.1 master architecture beyond prep documentation. It adds executable local source paths for Universal Work, caller manifests, QIRC local ledger, seed packs, pattern mines, flow packs, work atoms, model-worker boundary, candidates, Why Trace, local API, Odin Hub, diagnostics and safe-mode planning.

Canonical command spine:

```text
python -m odin.cli validate-all
python -m odin.cli doctor
python -m odin.cli run-work examples/runtime/universal_work_full.valid.json --seed-pack examples/runtime/app_seed_pack_full.valid.json --pattern-mine examples/runtime/pattern_mine_full.valid.json --caller-manifest examples/runtime/app_caller_manifest.valid.json
python -m odin.cli compile-seed-pack examples/runtime/app_seed_pack_full.valid.json
python -m odin.cli compile-pattern-mine examples/runtime/pattern_mine_full.valid.json
python -m odin.cli build-hub --out .odin_runtime/hub/index.html
python -m odin.cli emit-support-bundle --out .odin_runtime/support
```

Claim boundary: this remains a local runtime source candidate. It does not assert Windows host behavior, live model inference, signed installer behavior, external network operation, or app-side application.


## v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK

Odin now includes a direct runtime release candidate body: runtime store/session/config, App SDK, golden app examples, local API endpoints, static Odin Hub, provider boundary stubs, Windows handoff scripts, support bundle, safe mode plan and release-candidate acceptance commands. This remains candidate-only: no app apply, no host proof, no service/tray/installer proof and no live model inference proof are claimed.
## v0.8.7 Codex Real PR Handoff Ladder Lock

Current Codex execution starts from `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK` and uses the reoptimized eight-PR ladder:

```text
REAL-GH-PR-01..08 = actual Codex/GitHub completion sequence
PR-00..PR-123 = internal micro-task traceability
REAL-PR-01..28 = internal legacy bundle traceability
```

Primary handoff files:

```text
registries/real_pr_execution_registry.json
registries/codex_real_pr_handoff_registry.json
docs/codex/REAL_GITHUB_PR_EXECUTION_PLAN_V0_8_7.md
docs/codex/REAL_GITHUB_PR_EXECUTION_INDEX_V0_8_7.md
docs/codex/CODEX_FINAL_HANDOFF_V0_8_7.md
```

## v0.8.7 Current Codex hardening path

- **Architecture:** Odin Agent Shell v7.1.
- **Current handoff:** `v0.8.7 CODEX_REAL_PR_HANDOFF_LADDER_LOCK`, starting from the `v0.8.6 DIRECT_RUNTIME_RELEASE_CANDIDATE_LOCK` runtime candidate.
- **Current execution mode:** Codex hardening from a running Runtime Candidate; this is not a production-readiness claim.
- **Actual Codex PR path:** `CODEX-PR-01`, `CODEX-PR-02`, `CODEX-PR-03`, `CODEX-PR-04`, `CODEX-PR-05`.
- **Historical traceability retained:** `PR-00..PR-123`, `REAL-PR-01..28`, and `REAL-GH-PR-01..08` remain traceability ladders and are not deleted or treated as proof of completion.

Boundary summary: Odin emits candidates only; app-owned apply remains mandatory; Odin does not mutate caller/app state; Odin does not silently send externally; provider/model output is never promoted to truth.

Proof gaps retained: no production readiness proof; no live model inference proof; no model quality proof; no Windows service/tray/installer proof unless actually tested; no security certification proof; no external send proof; no app-state mutation proof; manual review remains required.

### CODEX-PR-01 acceptance scope

This PR hardens root canon, validation gates, schema/registry loading, runtime skeleton import boundaries, CLI failure messages, and release-candidate proof discipline. It does not implement Runtime Bus expansion, provider execution, QIRC authority, narrative runtime, Windows product runtime, App SDK expansion, app apply, external sends, or production readiness. Remaining work is intentionally deferred to `CODEX-PR-02..05`.

