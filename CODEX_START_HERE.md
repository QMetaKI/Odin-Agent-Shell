# Codex Start Here

## Mission

Implement Odin Agent Shell v7.1 from architecture/spec to working local-first runtime in strict phases.

## Current repo-prep version

```text
v0.4.0 CODEX_TASK_LOCK
```

## Build principle

Do not start with a chat UI. Do not start with model providers. Start with contracts.

```text
Schemas → registries → validators → packets → universal work → semantic bus → small-model-power → model routes → APIs → SDKs → Windows shell
```

## Mandatory task-lock documents

1. `docs/codex/CODEX_TASK_LOCK_V0_4_0.md`
2. `docs/codex/IMPLEMENTATION_SEQUENCE_V0_4_0.md`
3. `docs/codex/PR_DEPENDENCY_GRAPH_V0_4_0.md`
4. `docs/codex/TASK_DOD_MATRIX_V0_4_0.md`
5. `docs/codex/CODEX_PROMPT_PACKS_V0_4_0.md`
6. `docs/codex/PR_TASK_INDEX.md`
7. exact task file under `docs/codex/tasks/`

## Phase order

1. `docs/codex/PHASE_0_CANON_LOCK.md`
2. `docs/codex/PHASE_1_UNIVERSAL_CORE.md`
3. `docs/codex/PHASE_2_SEMANTIC_BUS.md`
4. `docs/codex/PHASE_3_SMALL_MODEL_POWER.md`
5. `docs/codex/PHASE_4_MODEL_RUNTIME.md`
6. `docs/codex/PHASE_5_WINDOWS_APP.md`
7. `docs/codex/PHASE_6_APP_SDKS_TEMPLATES.md`

## Task order

Use `registries/codex_task_registry.json` as machine-readable task order.

## Done definition for any task

- schema/registry parity OK
- `python -m odin.cli validate-all` OK
- `python -m pytest -q -p no:cacheprovider` exits 0
- no app LLM runtime introduced
- no direct app mutation by Odin
- no positive unsupported claims
- docs updated if behavior changed

## v0.4.1 Real PR Bundle Overlay

The PR-00 through PR-21 documents remain the internal implementation ladder. For actual future Codex pull requests, use the bundle overlay:

- `docs/codex/CODEX_REAL_PR_BUNDLE_PLAN_V0_4_1.md`
- `docs/codex/REAL_PR_BUNDLE_INDEX_V0_4_1.md`
- `registries/codex_pr_bundle_registry.json`
- `docs/codex/bundles/`

Rule: create real PRs by REAL-PR bundle; complete the mapped internal PR tasks inside each bundle.

# v0.4.2 Codex Note

Before implementation, read:

```text
docs/reviews/SENIOR_REVIEW_SIMULATION_V0_4_2.md
docs/SENIOR_REVIEW_REMEDIATION_PLAN_V0_4_2.md
docs/CODEX_ANTI_DRIFT_POLICY.md
docs/TRACEABILITY_MATRIX_V7_1.md
```

Codex must preserve both task layers:

```text
Internal ladder: PR-00..PR-22
Real bundles: REAL-PR-01..REAL-PR-08
```


## v0.5.0 Shadow Runtime Rule

Before implementing real modules, read `docs/SHADOW_RUNTIME_LOCK_V7_1.md` and `docs/SHADOW_RUNTIME_CODE_NEAR_BOOK_V7_1.md`. PR-23 / REAL-PR-09 define the mechanical bridge from specs to real code.


---

## v0.5.1 FULL_SHADOW_RUNTIME_COVERAGE

This release extends the Shadow Runtime from central spine coverage to full major-subsystem coverage. Every future addition must update the architecture/specs, internal PR ladder, REAL-PR bundles, registries, System Map, tests and FILE_MANIFEST. The Shadow Runtime remains candidate-only, local-only, non-authoritative and non-executing.

New coverage includes Artifact Lenses, Context Distillery, Worklet/Slot/Gaptext, Candidate Tournament, Low-Memory Strict Mode, Thor Bridge, Bounded Code Work, Storage/Trace/Receipt, Local API, App-QIRC Digest Bridge, Model Dojo, Security Redaction, Support Bundle, Windows Runtime and SDK/App Template validation.

## v0.5.2 Shadow Runtime Near-Final Rule

Before implementing real runtime services, Codex must inspect `docs/SHADOW_RUNTIME_NEAR_FINAL_LOCK_V7_1.md` and `odin/shadow_runtime/e2e_orchestrator_shadow.py`.

The near-final Shadow Runtime is the mechanical conversion bridge. Real modules should preserve its sequence and boundaries while replacing pure projections with real validated implementations.

## v0.6.0 Narrative Aorta / Y* Compiler Integration

This repo now integrates the Fairy/Y* Narrative Aorta and Shadow Runtime Compiler Prelude into the v7.1 canon. v7.1 runtime invariants remain unchanged. New work must update the internal PR ladder, real PR bundles, registries, System Map, tests and FILE_MANIFEST.

New internal tasks: PR-26 through PR-37. New real bundles: REAL-PR-12 and REAL-PR-13.



---

# v0.6.1 Addendum — Odin Core / QLI / DFAS / Seed Economy / Maria-Michael Superposition

This addendum preserves the v7.1 architecture and hardens the center. Odin is now explicitly defined as a Y-Core-like authority only for LLM work. It is not app authority. App state, app apply and external sends remain outside Odin authority.

The new centerline consists of:

1. Odin Core Centerline — active center, admissibility, authority boundary and final gate.
2. Odin QLI Master Interface — internal master keyboard for intent, authority posture, ring path, Maria/Michael profile, seed economy and route decisions.
3. DFAS Stability Core — hold/continue/split/ask/block pre-model admissibility.
4. Seed / Archetype Economy — typed activation, decay, conflict resolution, fan-out caps and role mapping.
5. QMath Center Solver — route scoring by stability gain minus token, latency, complexity, privacy, claim and uncertainty costs.
6. Ring Radar / Resonance — ring activation and deviation-triggered compute.
7. Why Trace — explanation of center, route, seeds, roles, gates, blocked alternatives and candidate DNA.
8. Maria/Michael Superposition — default 80/20 care/coherence with compiler/boundary override profiles.

The goal is quality, efficiency and deblackboxing. Odin must decide before the model: whether work is admissible, what center is active, what route is justified, what seeds and roles are active, and why a candidate is returned.

Codex must preserve this: no provider adapter may bypass centerline/admissibility/route-score/final-gate. No seed or archetype role may enter runtime work without typed packet and budget discipline. No Maria/Michael profile may be interpreted as persona simulation.

---

# v0.6.2 ODIN_QIRC_GOLD_SPINE_LOCK

Odin QIRC is now treated as a Gold Spine: a local-only semantic event, precompute, seed, admissibility, ring-radar, model-route and why-trace backbone. It is not a public IRC system and not a network feature. The QIRC Gold Spine makes Odin less black-boxed and reduces model guessing by converting Universal Work into hot windows, seed prewarm, archetype roles, QMath route scores, ring-local activation, candidate assembly and redacted Why Trace.

The added invariant chain is:

```text
Universal Work → QIRC Event → Hot Window → Seed Prewarm → Admissibility → QMath/Ring Radar → Worklet/Slot → Model Route or Hold → Candidate → Why Trace
```

Red lines: no app-state mirror, no public IRC, no external send, no model dispatch before admissibility, no unlimited seed fanout, no unredacted private payloads and no bypass of Odin Final Gate.



## v0.6.3 Bug6 / Q7 / Y-Core / Seed Core Lock

Adds explicit Bug6, Q7, bounded Y-Core posture, operational seed substrate, seed/archetype synthesis, Fairy/Y* seed binding, Shadow Runtime seed weave, Runtime Pack seed profiles, PR-50..PR-55, and REAL-PR-16.


---

# v0.6.4 Senior Review Consolidation — AI-Git Safety Spine

Odin v7.1 is additionally consolidated as an AI-Git safety control plane for local model work. The term does not mean Odin replaces Git. It means Odin applies Git-like safety properties to AI work: candidate branches, semantic diffs, review hooks, why traces, candidate DNA, blocked-route visibility and app-owned apply.

## Consolidated Invariants

- Universal Work remains the ingress contract.
- QIRC Gold Spine remains internal/local by default.
- Odin Core / QLI / DFAS / QMath decide admissibility before model dispatch.
- Bug6 / Children-First and Q7 stability act as pre-selector invariant filters.
- Maria/Michael superposition is an operational safety vector.
- Models remain projection workers.
- Odin returns candidates only.
- Apps own state, apply and external sends.

## AI-Git Mapping

- Candidate Artifact = AI commit candidate.
- Semantic Diff = difference between input and candidate.
- Why Trace = commit message plus route rationale.
- Candidate DNA = provenance/blame surface.
- Thor Handoff = review packet.
- Generated Gates = CI-like hooks.
- Runtime Pack rollback = revert path.

## Autonomy Escalation Gate

Every output must be classified from A0 to A5. Odin may perform A0-A2, may prepare A3 previews, may never perform A4 apply, and must block A5. Any signal of hidden tool use, external send, app-state write, unvalidated pack load or model-controlled code generation blocks or reduces the output to a safe candidate.

## Safety Superposition

The default safety posture is Maria 80 / Michael 20: context and dignity first, boundary always present. Code, compiler, risk and legal flows may increase Michael, while story and human-care flows may increase Maria. Neither pole may be removed.

## Skynet Pattern Boundary

Odin does not claim all AI risk impossible. It specifically blocks the local-tool escalation chain: model -> authority -> tool access -> hidden apply -> loop/network -> self-reinforcing action. It does this through candidate-only output, app-owned apply, local-only QIRC, validated runtime packs, why trace, Bug6/Q7, and autonomy gates.

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

