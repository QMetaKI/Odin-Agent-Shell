# PR-30 B4 Thor / Odin / Claude Code Audit

**claim_boundary:** audit_findings_are_process_observations_not_runtime_capability_claims
**PR:** PR-30 / B4
**Bundle:** B4 — Minicheck / Critics / Tournament / Candidate DNA / Response Packet / Final Gate Advisory

---

## Thor Command Availability

| Command | Available | Result |
|---------|-----------|--------|
| `thor --help` | YES | Listed all subcommands |
| `thor doctor` | YES | Warning: `.thor/` missing |
| `thor handoff-summary` | YES | Partial output (no .thor/ workspace) |
| `thor pr-section` | YES | Partial output |
| `thor repo cognition` | NO | No `repo` subcommand in Thor 4.1.1 |
| `thor y analyze` | YES (command present) | No .thor/ workspace |
| `thor y compose --dry-run` | YES (command present) | No .thor/ workspace |
| `thor y handoff --dry-run` | YES (command present) | No .thor/ workspace |
| `thor validate` | NO (requires .thor/) | No initialized workspace |
| `thor protocol` | YES | Subcommand present |
| `thor return` | YES | Subcommand present |
| `thor handoff-spine` | YES | Subcommand present |

**Thor-Agent-Kit commit:** e9af7a333e4bcb11f2461696e4ebbcde994b98b1 (same as B3)

### Thor Unavailability Finding

`thor repo cognition` is not available in Thor 4.1.1. This is a known limitation documented in the B3 audit. Odin repo cognition was performed manually by reading canonical docs and registries.

---

## Thor/Y Availability

Thor/Y subcommands (analyze, compose, handoff, etc.) are present in Thor 4.1.1 but require an initialized `.thor/` workspace. Without initialization, they return minimal output without full Y composition. This is consistent with B2 and B3 findings.

**Manually applied:** Thor/Y discipline (candidate-only, claim boundaries, review/receipt cascade) from `docs/v3.5/ARTIFACT_SPECS.md` and `docs/v3.5/SLICE_MATRIX.md`.

---

## Thor Protocol Review / Receipt Mapping

See: `docs/codex/handoffs/PR_30_B4_THOR_PROTOCOL_REVIEW_RECEIPT_MAPPING.md`

Key mappings applied:
- THOR_HANDOFF.kernel_binding → B4 handoff refs, ModelWorkPacket refs, CriticWorkPacket refs
- THOR_RETURN.files_changed / evidence_refs → B4 return report
- THOR_REVIEW.claim_findings → Senior Reviewer + Senior Code Reviewer simulations
- THOR_RECEIPT.accepted/denied/pending → B4 Final Gate Advisory / Receipt Boundary

---

## Odin Work-Kernel Usage

Odin-Agent-Shell provided the canonical work-kernel scaffold:
- AGENTS.md: forbidden actions, candidate_only discipline
- CODEX_START_HERE.md: boundary enforcement
- CLAIM_BOUNDARY.md: claim governance
- registries/v7_1_1_actual_codex_bundle_plan.json: bundle mapping updated for B4
- registries/v7_1_1_road_to_100_ladder.json: canonical ladder preserved

All B4 artifacts respect the Odin work-kernel contract:
- candidate_only: true in all artifacts
- claim_boundary present in all artifacts
- non_claims non-empty in all artifacts
- No hidden authority introduced

---

## Claude-as-Worker Adapter Usage

The Claude Code worker (claude-code) operated under the formal adapter contract:
- `schemas/v7_1_1_odin_claude_worker_adapter.schema.json` (B3 artifact)
- `registries/v7_1_1_odin_claude_worker_adapter_registry.json`

Adapter contract honored:
- Claude Code is external local worker (not app authority)
- No live model execution in B4
- No app state mutation
- No external send
- All outputs are candidate artifacts for review

---

## ModelWorkPacket Consumption

B4 correctly consumes B3 ModelWorkPacket:
- CriticWorkPacket.modelworkpacket_ref references the B3 ModelWorkPacket schema
- CriticWorkPacket.scale_ladder_route_class uses the B3 10-class route system
- Route-to-critic mapping covers all 10 B3 route classes

B3 audit finding B3-AUDIT-003 addressed:
> "B4 should add CriticWorkPacket that references ModelWorkPacket.model_route_ref to select critic tier"
→ ADDRESSED: critic_work_packet_registry.json.route_to_critic_mapping covers all 10 classes

---

## Route-Aware Critic Tiering

The route-aware critic tier mapping is implemented in:
- `registries/v7_1_1_critic_work_packet_registry.json` (route_to_critic_mapping)
- `schemas/v7_1_1_critic_work_packet.schema.json` (critic_tier enum, scale_ladder_route_class enum)

Coverage:
- deterministic_no_model → deterministic_schema_critic / deterministic_contract_critic
- tiny_local_candidate → deterministic_contract_critic / small_model_advisory_critic
- small_model_candidate → small_model_advisory_critic
- small_model_multi_slot_candidate → small_model_advisory_critic
- local_7b_8b_candidate → hybrid_advisory_critic
- hybrid_3b_7b_candidate → hybrid_advisory_critic
- quality_hybrid_candidate → hybrid_advisory_critic
- heavy_local_candidate → human_review_required / hybrid_advisory_critic
- remote_explicit_only → human_review_required
- cannot_safely_complete → cannot_safely_complete

---

## Minicheck Design Impact

Minicheck adds 14 deterministic check kinds covering all major boundary violations:
- claim_boundary_check, forbidden_action_check, final_gate_boundary_check
- receipt_boundary_check, no_runtime_claim_check, no_model_quality_claim_check
- no_external_send_check, no_app_apply_check, route_class_check

B5 implication: Minicheck provides the pre-filter for B5 Storage/Trace/Receipt integration.

---

## Critic Cascade Design Impact

Critic Cascade defines 8 ordered stages with 11 escalation conditions.
The cascade is fully static in B4. B5 provider runtime may add first dynamic stage.

Key escalation conditions for future B5 work:
- `provider_policy_missing` → B5 must add explicit provider policy before runtime integration
- `remote_route_requested` → B5 must require explicit opt-in for remote providers

---

## Tournament Design Impact

Tournament selection uses 10 scoring dimensions, all static in B4.
Tournament does not apply, does not prove correctness, does not bypass human review.

B7+ implication: Tournament scoring weights may be calibrated by real evaluation data.

---

## Candidate DNA Impact

Candidate DNA traces lineage through:
- source_modelworkpacket_ref
- source_context_capsule_ref
- source_gaptext_ref
- source_slot_contract_ref
- source_route_class

Privacy class (public/internal/sensitive/redacted) and content_hash discipline enforced.
B5 must consume candidate_dna_id in storage/trace receipts.

---

## Response Packet Impact

Response Packet introduces the critical distinction:
- claims_made vs claims_not_made
- commands_run vs commands_not_run
- tests_run vs tests_not_run

This discipline enables honest return material that distinguishes what was done from what was not done.

B5 must reference response_packet_id from storage receipts.

---

## Final Gate Advisory Boundary

Final Gate Advisory enforces:
- Named "Advisory" not "Authority" or "Gate"
- is_apply_gate: false (const in schema)
- is_app_authority: false (const in schema)
- Five recommendations: advisory_pass, advisory_warn, advisory_block, human_review_required, cannot_safely_complete

B5 must NOT elevate Final Gate Advisory to Apply Gate.
App-owned Apply Gate remains entirely separate from Odin Final Gate Advisory.

---

## Receipt Boundary Boundary

Receipt Boundary enforces:
- is_absolute_truth: false (const in schema)
- is_runtime_proof: false (const in schema)
- is_security_certification: false (const in schema)
- is_deployment_proof: false (const in schema)
- Three partitions: accepted_claim_refs, denied_claim_refs, pending_claim_refs

B7+ implication: Thor Protocol receipt integration with Odin Receipt Boundary should be evaluated in B7+.

---

## What Was Not Used and Why

| Item | Not Used | Reason |
|------|---------|--------|
| `thor repo cognition` | Not available | No `repo` subcommand in Thor 4.1.1 |
| `thor validate` | Not run | Requires .thor/ workspace |
| `thor y analyze` (full) | Not run | Requires .thor/ workspace |
| Provider SDK imports | Not included | B4 is static-only — no live execution |
| App state mutation | Not included | Forbidden by Odin boundary |
| QIRC server | Not implemented | Not in B4 scope |
| Final Gate as Apply Gate | Not implemented | Hard boundary violation |
| YNode-prep | Not cloned | Network restriction (same as B2/B3) |

---

## Findings for B5 / B7+

### B5 Findings

1. **B5 must consume response_packet_id and candidate_artifact_id in storage/trace/receipt artifacts**
2. **B5 provider runtime must be local-first, explicit-policy-only** — no hidden remote fallback
3. **B5 must integrate provider seam with explicit policy file and receipt log before any remote provider**
4. **B5 Minicheck must validate provider_policy_present before critic cascade entry**
5. **B5 storage receipt must reference candidate_dna_id for lineage traceability**

### B7+ Findings

1. **B7+ should evaluate Thor Protocol receipt integration with Odin Receipt Boundary** — receipt.accepted_claim_refs could map to Thor THOR_RECEIPT.accepted_claim_refs
2. **B7+ should evaluate actual Thor-Odin bridge feasibility** — thor pack --agent claude-code targeting Odin work packets
3. **B7+ post-closure review should verify B4 contracts were correctly implemented** in B5 provider runtime
4. **B7+ tournament scoring weights may be calibrated** by real evaluation data after B5 provider integration

---

## Commands Run (Evidence)

```
# Thor intake
git clone https://github.com/QMetaKI/Thor-Agent-Kit.git /tmp/odin_pr30_b4_external_refs/Thor-Agent-Kit
cd /tmp/odin_pr30_b4_external_refs/Thor-Agent-Kit && git rev-parse HEAD
# → e9af7a333e4bcb11f2461696e4ebbcde994b98b1
python -m pip install -e ".[dev]"  # SUCCESS
python -m thor --help  # SUCCESS
python -m thor doctor  # SUCCESS (warnings only)
python -m thor handoff-summary --task "..." --task-label "Odin B4" --agent claude-code --format markdown  # SUCCESS (partial)
python -m thor pr-section --task "..." --task-label "Odin B4" --agent claude-code  # SUCCESS (partial)

# B4 validator
python tools/v7_1_1/check_b4_minicheck_critics_final_gate.py \
  --repo-root . \
  --out reports/v7_1_1_b4_minicheck_critics_final_gate_report.json \
  --generated-at-utc 2026-01-01T00:00:00Z
# → B4 validator: PASS (0 violations)

# B4 tests
python -m pytest -q tests/test_v7_1_1_b4_minicheck_critics_final_gate.py -p no:cacheprovider
# → 80 passed

# Prior tests
python -m pytest -q tests/test_v7_1_1_operational_coverage_gap_compiler.py tests/test_v7_1_1_canon_boundary_integrity.py tests/test_v7_1_1_b1_app_boundary_universal_work_qirc_spine.py tests/test_v7_1_1_b2_context_lenses_worklets_slot_gaptext.py tests/test_v7_1_1_b3_modelworkpacket_scale_hybrid.py -p no:cacheprovider
# → 182 passed

# validate-all
python -m odin.cli validate-all
# → validate-all: OK
```
